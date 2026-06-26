#!/usr/bin/env python3
"""
Facebook Group Monitor — Scrape new posts from a Facebook group.
Uses Playwright with stealth mode and persistent login session.
Supports screenshot capture per post for LLM vision analysis.

Usage:
    fb-group-monitor.py login                                      # Login (opens browser)
    fb-group-monitor.py scrape <group_url> [--limit N]             # Scrape new posts (with screenshots)
    fb-group-monitor.py scrape <group_url> [--limit N] --no-shots  # Scrape without screenshots
    fb-group-monitor.py status                                     # Check login status
    fb-group-monitor.py clean-shots                                # Remove old screenshots

Output: JSON to stdout (for agent consumption)
"""

import asyncio
import argparse
import hashlib
import io
import json
import os
import sys
import time
import random
from datetime import datetime, timedelta
from pathlib import Path

try:
    from PIL import Image as PILImage
    PILLOW_AVAILABLE = True
except ImportError:
    PILLOW_AVAILABLE = False

# ── Config ──────────────────────────────────────────────────────────────────
SCRIPT_DIR = Path(__file__).parent
BROWSER_DATA = SCRIPT_DIR / ".browser-data"
SEEN_FILE = SCRIPT_DIR / ".seen-posts.json"
# SCREENSHOTS_DIR được override bởi --shots-dir argument.
# Mặc định lưu trong script dir (fallback), nhưng agent NÊN truyền workspace path
# để OpenClaw image tool có thể đọc được (chỉ cho phép đọc trong workspace).
DEFAULT_SCREENSHOTS_DIR = SCRIPT_DIR / "screenshots"

MAX_SCREENSHOTS = 100       # Tối đa giữ N ảnh
SCREENSHOT_TTL_HOURS = 48   # Xóa ảnh cũ hơn N giờ
FEED_SCROLL_SHOTS = 3       # Số viewport screenshots để stitch thành feed strip

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
)

BROWSER_ARGS = [
    "--disable-blink-features=AutomationControlled",
    "--no-sandbox",
    "--disable-dev-shm-usage",
]

# JS để extract data từ 1 post element
EXTRACT_POST_JS = """(el) => {
    const fullText = el.textContent || '';
    if (fullText.length < 30) return null;

    // --- Author ---
    let author = '';
    const profileLinks = el.querySelectorAll(
        'a[href*="/user/"], a[href*="/profile.php"], a[href*="facebook.com/"][role="link"]'
    );
    for (const pl of profileLinks) {
        const name = pl.textContent?.trim();
        if (name && name.length > 1 && name.length < 60 && !/^\\d/.test(name)) {
            author = name;
            break;
        }
    }

    // --- Post text ---
    const dirAutos = el.querySelectorAll('div[dir="auto"]');
    const textParts = [];
    for (const d of dirAutos) {
        const t = d.textContent?.trim();
        if (t && t.length > 10 && t !== author) {
            textParts.push(t);
        }
    }
    textParts.sort((a, b) => b.length - a.length);
    const text = textParts.length > 0 ? textParts[0].substring(0, 2000) : '';

    // --- Post URL ---
    let postUrl = '';

    // Helper: check if a resolved href looks like a post permalink (not comment/photo/profile)
    const isPostLink = (h) => {
        if (!h) return false;
        if (!h.includes('facebook.com')) return false;
        const bad = ['comment_id', '/photo/', '/photos/', '/profile.php', '/user/', 'refsrc=', 'action='];
        if (bad.some(b => h.includes(b))) return false;
        return h.includes('/posts/') || h.includes('/permalink/') || h.includes('story_fbid');
    };

    // Pass 1: primary selectors (specific patterns in href attribute)
    const postLinks = el.querySelectorAll(
        'a[href*="/posts/"], a[href*="/permalink/"], a[href*="story_fbid"]'
    );
    for (const pl of postLinks) {
        const href = pl.getAttribute('href') || '';
        if (href && !href.includes('comment_id')) {
            postUrl = pl.href;
            break;
        }
    }

    // Pass 2: fallback — scan ALL anchors, filter by resolved href
    if (!postUrl) {
        for (const a of el.querySelectorAll('a[href]')) {
            if (isPostLink(a.href)) {
                postUrl = a.href;
                break;
            }
        }
    }

    // Pass 3: timestamp link fallback — Facebook timestamp always links to post permalink
    // Timestamp <a> tags typically have aria-label with relative time or wrap a <abbr>/<time>
    if (!postUrl) {
        const timeSelectors = [
            'a[aria-label*="giờ"]', 'a[aria-label*="phút"]', 'a[aria-label*="ngày"]',
            'a[aria-label*="tuần"]', 'a[aria-label*="tháng"]',
            'a[aria-label*="hour"]', 'a[aria-label*="minute"]', 'a[aria-label*="day"]',
            'a[aria-label*="week"]', 'a[aria-label*="month"]',
            'a abbr[title]',
        ];
        for (const sel of timeSelectors) {
            const el2 = sel.endsWith(']') && sel.includes(' ')
                ? el.querySelector(sel)?.closest('a')
                : el.querySelector(sel);
            if (el2 && isPostLink(el2.href)) {
                postUrl = el2.href;
                break;
            }
        }
    }

    // Pass 4: construct URL from photo link's "set" param (post ID hidden inside)
    // Facebook embeds post ID in photo links: /photo/?fbid=X&set=pcb.POSTID or set=gm.POSTID
    if (!postUrl) {
        for (const a of el.querySelectorAll('a[href*="/photo/"]')) {
            const photoHref = a.href || '';
            const setMatch = photoHref.match(/[?&]set=(?:pcb|gm|pb|g)\.(\d+)/);
            if (setMatch) {
                // Extract group ID from any user link in the element
                const groupLink = el.querySelector('a[href*="/groups/"][href*="/user/"]');
                if (groupLink) {
                    const grpMatch = groupLink.href.match(/\/groups\/(\d+)\//);
                    if (grpMatch) {
                        postUrl = 'https://www.facebook.com/groups/' + grpMatch[1] + '/posts/' + setMatch[1] + '/';
                        break;
                    }
                }
            }
        }
    }

    if (postUrl) {
        try {
            const u = new URL(postUrl);
            u.search = '';
            postUrl = u.toString();
        } catch(e) {}
    }

    // --- Images ---
    const imgEls = el.querySelectorAll('img[src*="scontent"]');
    const imageCount = imgEls.length;

    if (!author && text.length < 20) return null;

    return {
        author: author || 'Unknown',
        text: text,
        url: postUrl,
        images: imageCount,
    };
}"""


# ── Helpers ─────────────────────────────────────────────────────────────────
def result_json(success, action, **kwargs):
    data = {"success": success, "action": action, **kwargs}
    print(json.dumps(data, ensure_ascii=False, indent=2))
    sys.exit(0 if success else 1)


def load_seen_posts():
    if SEEN_FILE.exists():
        try:
            return set(json.loads(SEEN_FILE.read_text()))
        except Exception:
            return set()
    return set()


def save_seen_posts(seen):
    SEEN_FILE.write_text(json.dumps(list(seen), ensure_ascii=False))


def post_hash(text, author):
    content = f"{author}:{text[:200]}"
    return hashlib.md5(content.encode()).hexdigest()


def cleanup_screenshots(shots_dir: Path):
    """Xóa screenshots cũ hơn TTL hoặc vượt MAX_SCREENSHOTS."""
    cutoff = datetime.now() - timedelta(hours=SCREENSHOT_TTL_HOURS)
    files = sorted(shots_dir.glob("*.jpg"), key=lambda f: f.stat().st_mtime)

    removed = 0
    for f in files:
        mtime = datetime.fromtimestamp(f.stat().st_mtime)
        if mtime < cutoff:
            f.unlink()
            removed += 1

    files = sorted(shots_dir.glob("*.jpg"), key=lambda f: f.stat().st_mtime)
    while len(files) > MAX_SCREENSHOTS:
        files[0].unlink()
        files = files[1:]
        removed += 1

    return removed


async def create_browser_context(p, headless=True):
    try:
        from playwright_stealth import stealth_async
    except ImportError:
        stealth_async = None

    context = await p.chromium.launch_persistent_context(
        user_data_dir=str(BROWSER_DATA),
        headless=headless,
        viewport={"width": 1280, "height": 900},
        user_agent=USER_AGENT,
        args=BROWSER_ARGS,
        ignore_default_args=["--enable-automation"],
        locale="vi-VN",
        timezone_id="Asia/Ho_Chi_Minh",
    )

    if stealth_async:
        for page in context.pages:
            await stealth_async(page)

    return context, stealth_async


# ── Commands ────────────────────────────────────────────────────────────────
async def cmd_login(args):
    from playwright.async_api import async_playwright

    print("Mở browser để đăng nhập Facebook...")
    print("Sau khi đăng nhập xong, nhấn Enter ở terminal này.")

    async with async_playwright() as p:
        context, stealth_fn = await create_browser_context(p, headless=False)
        page = context.pages[0] if context.pages else await context.new_page()
        if stealth_fn:
            await stealth_fn(page)
        await page.goto("https://www.facebook.com/", wait_until="domcontentloaded")
        input("\n✅ Đăng nhập xong? Nhấn Enter để lưu session...")
        await context.close()

    result_json(True, "login", message="Đã lưu session Facebook.")


async def cmd_status(args):
    from playwright.async_api import async_playwright

    async with async_playwright() as p:
        context, stealth_fn = await create_browser_context(p, headless=True)
        page = context.pages[0] if context.pages else await context.new_page()
        if stealth_fn:
            await stealth_fn(page)

        await page.goto("https://www.facebook.com/", wait_until="domcontentloaded")
        await page.wait_for_timeout(3000)

        logged_in = False
        if "login" in page.url or "checkpoint" in page.url:
            logged_in = False
        else:
            profile_link = await page.query_selector(
                '[aria-label="Your profile"], [aria-label="Trang cá nhân của bạn"]'
            )
            nav_menu = await page.query_selector('[role="navigation"]')
            logged_in = profile_link is not None or nav_menu is not None

        await context.close()

        if logged_in:
            result_json(True, "status", message="Session active — đã đăng nhập Facebook.")
        else:
            result_json(False, "status", error="Chưa đăng nhập. Chạy: fb-group-monitor.py login")


async def cmd_clean_shots(args):
    shots_dir = Path(args.shots_dir).expanduser()
    shots_dir.mkdir(parents=True, exist_ok=True)
    removed = cleanup_screenshots(shots_dir)
    remaining = len(list(shots_dir.glob("*.jpg")))
    result_json(True, "clean-shots",
                shots_dir=str(shots_dir),
                removed=removed,
                remaining=remaining,
                message=f"Đã xóa {removed} ảnh cũ. Còn lại {remaining} ảnh.")


async def capture_feed_strip(page, shots_dir, group_id, n_shots=FEED_SCROLL_SHOTS):
    """Capture N viewport screenshots cropped to the feed column, stitch into 1 image.

    Scroll back to top first, then capture one frame per viewport-height scroll.
    Frames are stitched vertically into a single JPEG for LLM vision analysis.
    Returns the file path string on success, or None on failure.
    """
    if not PILLOW_AVAILABLE:
        return None
    try:
        # Get feed column x/width for cropping (removes navbar & right sidebar noise)
        # Also get navbar height to skip it on first frame (navbar is sticky/fixed)
        feed_box = await page.evaluate("""() => {
            const feed = document.querySelector('[role="feed"]');
            const nav = document.querySelector('[role="banner"], header, [data-pagelet="NavBar"]');
            if (!feed) return null;
            const feedRect = feed.getBoundingClientRect();
            const navH = nav ? Math.round(nav.getBoundingClientRect().height) : 56;
            return {
                x: Math.max(0, Math.round(feedRect.left)),
                width: Math.round(feedRect.width),
                navH: navH
            };
        }""")
        vp = page.viewport_size or {"width": 1280, "height": 900}
        vp_h = vp["height"]
        if feed_box and feed_box["width"] > 100:
            clip_x = feed_box["x"]
            clip_w = min(feed_box["width"], vp["width"] - feed_box["x"])
            nav_h = feed_box.get("navH", 56)
        else:
            clip_x, clip_w, nav_h = 0, vp["width"], 56

        # Scroll to top so screenshots start from newest posts
        await page.evaluate("window.scrollTo(0, 0)")
        await page.wait_for_timeout(800)

        frames = []
        for i in range(n_shots):
            # Skip navbar on every frame (it's fixed/sticky, always at top of viewport)
            clip_y = nav_h
            clip_h = vp_h - nav_h
            buf = await page.screenshot(
                type="jpeg",
                quality=85,
                clip={"x": clip_x, "y": clip_y, "width": clip_w, "height": clip_h},
            )
            frames.append(buf)
            if i < n_shots - 1:
                await page.evaluate(f"window.scrollBy(0, {vp_h})")
                await page.wait_for_timeout(random.randint(1000, 1800))

        # Stitch frames vertically
        images = [PILImage.open(io.BytesIO(b)) for b in frames]
        total_h = sum(img.height for img in images)
        max_w = max(img.width for img in images)
        stitched = PILImage.new("RGB", (max_w, total_h), (255, 255, 255))
        y = 0
        for img in images:
            stitched.paste(img, (0, y))
            y += img.height

        out_buf = io.BytesIO()
        stitched.save(out_buf, format="JPEG", quality=82, optimize=True)
        out_path = shots_dir / f"feed_{group_id}_{int(time.time())}.jpg"
        out_path.write_bytes(out_buf.getvalue())
        return str(out_path)
    except Exception:
        return None


async def cmd_scrape(args):
    from playwright.async_api import async_playwright

    group_url = args.group_url
    limit = args.limit
    take_screenshots = not args.no_shots
    shots_dir = Path(args.shots_dir).expanduser()
    shots_dir.mkdir(parents=True, exist_ok=True)

    if not group_url.startswith("http"):
        group_url = f"https://www.facebook.com/groups/{group_url}"

    if take_screenshots:
        cleanup_screenshots(shots_dir)

    async with async_playwright() as p:
        context, stealth_fn = await create_browser_context(p, headless=True)
        page = context.pages[0] if context.pages else await context.new_page()
        if stealth_fn:
            await stealth_fn(page)

        try:
            await page.goto(group_url, wait_until="domcontentloaded")
            await page.wait_for_timeout(random.randint(2000, 4000))

            if "login" in page.url:
                await context.close()
                result_json(False, "scrape",
                            error="Chưa đăng nhập Facebook. Chạy: fb-group-monitor.py login")

            title = await page.title()
            if any(kw in title.lower() for kw in ["security check", "checkpoint", "log in"]):
                await context.close()
                result_json(False, "scrape", error=f"Facebook yêu cầu xác minh: {title}")

            group_name = title.replace(" | Facebook", "").strip()

            await page.wait_for_timeout(5000)

            # Scroll để load thêm posts
            for _ in range(4):
                await page.evaluate("window.scrollBy(0, 1000)")
                await page.wait_for_timeout(random.randint(1500, 2500))

            # Lấy element handles của từng post trong feed
            feed_children = await page.query_selector_all('[role="feed"] > *')

            posts_data = []
            for child in feed_children:
                if len(posts_data) >= limit:
                    break

                try:
                    data = await child.evaluate(EXTRACT_POST_JS)
                except Exception:
                    continue

                if not data or not data.get("text"):
                    continue

                posts_data.append(data)

            # ── Feed strip screenshot (1 stitched image covers full feed) ──
            feed_screenshot = None
            if take_screenshots:
                group_id = hashlib.md5(group_url.encode()).hexdigest()[:8]
                feed_screenshot = await capture_feed_strip(page, shots_dir, group_id)

            await context.close()

            if not posts_data:
                result_json(True, "scrape",
                            group_name=group_name,
                            group_url=group_url,
                            posts=[],
                            new_count=0,
                            message="Không tìm thấy bài post nào. Có thể cần kiểm tra selectors.")
                return

            # Lọc bài mới
            seen = load_seen_posts()
            new_posts = []
            for post in posts_data:
                pid = post_hash(post.get("text", ""), post.get("author", ""))
                if pid not in seen:
                    new_posts.append(post)
                    seen.add(pid)

            if len(seen) > 500:
                seen = set(list(seen)[-500:])
            save_seen_posts(seen)

            result_json(
                True, "scrape",
                group_name=group_name,
                group_url=group_url,
                total_scraped=len(posts_data),
                new_count=len(new_posts),
                feed_screenshot=feed_screenshot,
                posts=new_posts,
                message=(
                    f"Tìm thấy {len(new_posts)} bài mới / {len(posts_data)} bài tổng cộng. "
                    + (f"Feed screenshot: {feed_screenshot}" if feed_screenshot else "Không có ảnh.")
                )
            )

        except Exception as e:
            try:
                await context.close()
            except Exception:
                pass
            result_json(False, "scrape", error=str(e))


# ── CLI ─────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="Facebook Group Monitor — scrape posts + screenshots từ FB groups",
        epilog="""Examples:
  %(prog)s login
  %(prog)s status
  %(prog)s scrape https://facebook.com/groups/12345
  %(prog)s scrape https://facebook.com/groups/12345 --limit 5
  %(prog)s scrape https://facebook.com/groups/12345 --no-shots
  %(prog)s clean-shots
""",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="cmd")
    sub.required = True

    sub.add_parser("login", help="Đăng nhập Facebook (mở browser)")
    sub.add_parser("status", help="Kiểm tra session")

    clean_p = sub.add_parser("clean-shots", help="Xóa screenshots cũ")
    clean_p.add_argument(
        "--shots-dir",
        default=str(DEFAULT_SCREENSHOTS_DIR),
        help="Thư mục chứa screenshots (default: script_dir/screenshots)"
    )

    scrape_p = sub.add_parser("scrape", help="Scrape bài mới từ group")
    scrape_p.add_argument("group_url", help="URL hoặc ID của Facebook group")
    scrape_p.add_argument("--limit", type=int, default=10, help="Số bài tối đa (default: 10)")
    scrape_p.add_argument("--no-shots", action="store_true",
                          help="Không chụp ảnh (nhanh hơn, dùng khi chỉ cần text)")
    scrape_p.add_argument(
        "--shots-dir",
        default=str(DEFAULT_SCREENSHOTS_DIR),
        help="Thư mục lưu screenshots — NÊN trỏ vào workspace để image tool đọc được. "
             "VD: ~/.openclaw/workspace-daily-digest/temp-screenshots"
    )

    args = parser.parse_args()

    cmd_map = {
        "login": cmd_login,
        "status": cmd_status,
        "scrape": cmd_scrape,
        "clean-shots": cmd_clean_shots,
    }

    asyncio.run(cmd_map[args.cmd](args))


if __name__ == "__main__":
    main()
