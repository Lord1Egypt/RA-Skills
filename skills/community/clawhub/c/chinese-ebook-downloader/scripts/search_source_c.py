#!/usr/bin/env python3
"""
Search Source C: Anna's Archive (影子图书馆)
Searches for Chinese ebooks via Anna's Archive mirror domains.

Uses HTTP requests (urllib) for search - reliable and fast.
Browser (Playwright) only used for download attempts.

Usage: python search_source_c.py "书名" ["作者"]
"""
import sys
import os
import re
import asyncio
import subprocess
import urllib.parse
from typing import Optional, List, Dict
from html import unescape

try:
    from playwright.async_api import async_playwright
except ImportError:
    pass  # Only needed for download attempts

# Mirrors to try (priority order)
SOURCE_C_MIRRORS = os.environ.get(
    "SOURCE_C_MIRRORS",
    "https://annas-archive.gl,https://annas-archive.pk,https://annas-archive.gd"
).split(",")

_USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
)

_SEARCH_TIMEOUT = 45  # seconds for search (pages can be 500KB+)


def _fetch_url(url: str, timeout: int = 20) -> Optional[str]:
    """Fetch URL content using curl (more reliable than urllib for DDoS-Guard)."""
    import subprocess
    cmd = [
        "curl", "-s", "-L",
        "--max-time", str(timeout),
        "--connect-timeout", str(min(timeout, 10)),
        "-H", f"User-Agent: {_USER_AGENT}",
        "-H", "Accept: text/html,application/xhtml+xml,*/*;q=0.8",
        "-H", "Accept-Language: zh-CN,zh;q=0.9,en;q=0.8",
        url,
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout + 5)
        if result.returncode == 0 and result.stdout:
            return result.stdout
        return None
    except Exception as e:
        print(f"  curl error for {url[:50]}: {e}")
        return None


def _find_working_mirror() -> Optional[str]:
    """Find a working Anna's Archive mirror."""
    for mirror in SOURCE_C_MIRRORS:
        html = _fetch_url(mirror, timeout=20)  # Server can be slow
        if html and "Anna" in html and len(html) > 5000:
            print(f"  Mirror OK: {mirror} ({len(html)} bytes)")
            return mirror
    return None


def _extract_search_queries(title: str, author: str = "") -> List[str]:
    """Generate multiple search queries from title/author."""
    queries = []
    clean = re.sub(r"[（(].+?[）)]", "", title).strip()
    clean = re.sub(r"[：:]", " ", clean).strip()
    if author:
        queries.append(f"{clean} {author}")
    if clean:
        queries.append(clean)
    short = clean.split()[0] if clean else title
    if len(short) >= 2:
        queries.append(short)
    return queries


def _has_chinese(text: str) -> bool:
    return any("\u4e00" <= c <= "\u9fff" for c in text)


def _title_similarity(query: str, result_title: str) -> float:
    q = query.lower().strip()
    r = result_title.lower().strip()
    if q == r:
        return 1.0
    if q in r or r in q:
        return 0.9
    q_words = set(q)
    r_words = set(r)
    if not q_words or not r_words:
        return 0.0
    return len(q_words & r_words) / max(len(q_words), len(r_words))


def _strip_tags(html: str) -> str:
    """Remove HTML tags and decode entities."""
    text = re.sub(r"<[^>]+>", " ", html)
    text = re.sub(r"&nbsp;", " ", text)
    return unescape(text).strip()


def _parse_search_results(html: str, mirror: str, query: str) -> List[Dict]:
    """Parse Anna's Archive search results HTML.

    Anna's Archive HTML structure per result:
      <a href="/md5/{md5}" class="...custom-a...">TITLE</a>
      <a href="/search?q=AUTHOR" ...>AUTHOR</a>
      <a href="/search?q=PUBLISHER" ...>PUBLISHER, YEAR</a>
      ...metadata spans for format, size, source...
    """
    results = []
    seen_md5s = set()

    # Find each result block: starts with /md5/ link, ends at the next /md5/ or end
    # Pattern: capture the md5 link + everything until the next md5 link
    blocks = re.split(r'href="/md5/', html)[1:]  # Skip text before first match

    for block in blocks:
        md5_match = re.match(r'([a-f0-9]{32})"', block)
        if not md5_match:
            continue
        md5 = md5_match.group(1)
        if md5 in seen_md5s:
            continue

        # Extract title from the first link (the md5 link itself)
        # Two patterns:
        # 1. href="/md5/{md5}" class="...font-semibold...">TITLE</a>  (title in md5 link)
        # 2. href="/md5/{md5}" class="...block...">  (md5 link is an image wrapper)
        title = ""

        # Pattern 1: Title is in the md5 link with font-semibold
        title_match = re.search(
            r'href="/md5/' + md5 + r'"[^>]*font-semibold[^>]*>(.*?)</a>',
            block, re.DOTALL
        )
        if title_match:
            title = _strip_tags(title_match.group(1)).strip()

        # Pattern 2: Title in a subsequent link with text-[#2563eb]
        if not title:
            title_match2 = re.search(
                r'text-\[#2563eb\][^>]*>(.*?)</a>',
                block, re.DOTALL
            )
            if title_match2:
                title = _strip_tags(title_match2.group(1)).strip()

        if not title or not _has_chinese(title):
            continue

        sim = _title_similarity(query, title)
        if sim < 0.15:
            continue

        # Extract author from subsequent link with user-edit icon
        author = ""
        author_match = re.search(r'icon-\[mdi--user-edit\][^>]*>\s*(.*?)</a>', block, re.DOTALL)
        if author_match:
            author = _strip_tags(author_match.group(1)).strip()

        # Extract publisher info (contains year)
        publisher_info = ""
        pub_match = re.search(r'icon-\[mdi--company\][^>]*>\s*(.*?)</a>', block, re.DOTALL)
        if pub_match:
            publisher_info = _strip_tags(pub_match.group(1)).strip()

        # Extract metadata from the block
        fmt_match = re.search(r"\b(pdf|epub|mobi|azw3)\b", block, re.I)
        size_match = re.search(r"([\d.]+\s*(?:MB|KB|GB))", block)
        year_match = re.search(r"\b((?:19|20)\d{2})\b", block)
        source_match = re.search(
            r"\b(zlib|duxiu|lgli|ia|hathi|lgrs|upload|zlibzh|nexusstc)\b",
            block, re.I
        )

        seen_md5s.add(md5)
        results.append({
            "title": title,
            "author": author,
            "md5": md5,
            "format": fmt_match.group(1).lower() if fmt_match else "",
            "size": size_match.group(1) if size_match else "",
            "year": year_match.group(1) if year_match else "",
            "source": source_match.group(1).upper() if source_match else "",
            "publisher": publisher_info,
            "mirror_url": f"{mirror}/md5/{md5}",
            "mirror_domain": mirror,
            "score": sim,
        })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results


def search_annas_archive(
    title: str,
    author: str = "",
    preferred_format: str = "pdf",
) -> List[Dict]:
    """
    Search Anna's Archive for a Chinese ebook (synchronous, HTTP-based).

    Returns list of dicts with keys:
        - title, author, md5, format, size, year, source, mirror_url, mirror_domain, score
    """
    queries = _extract_search_queries(title, author)
    all_results = []

    mirror = _find_working_mirror()
    if not mirror:
        print("  ⚠️  No working mirror found")
        return []

    for qidx, query in enumerate(queries):
        if all_results:
            break

        ext_param = preferred_format if preferred_format != "any" else ""
        url = (
            f"{mirror}/search?q={urllib.parse.quote(query)}&lang=zh"
            + (f"&ext={ext_param}" if ext_param else "")
            + "&sort=&fast=1"
        )
        print(f"  Searching: {query}")

        html = _fetch_url(url, timeout=_SEARCH_TIMEOUT)
        if not html:
            continue

        # Check for DDoS-Guard or error
        if "DDoS-Guard" in html or "checking your browser" in html.lower():
            print("  DDoS-Guard challenge on search page, skipping")
            continue

        results = _parse_search_results(html, mirror, query)
        if results:
            all_results.extend(results)
            print(f"  Found {len(results)} result(s)")
            for r in results[:3]:
                print(f"    - {r['title'][:50]} [{r['format']}] {r['size']} ({r['source']})")
        else:
            # Check if the response was too small (DDoS-Guard page)
            if len(html) < 5000:
                print(f"  Response too small ({len(html)} bytes) - likely blocked")
            else:
                # Check for DDoS-Guard in content
                if "ddos-guard" in html.lower() or "checking your browser" in html.lower():
                    print("  DDoS-Guard challenge in search response")
                else:
                    print("  No matching Chinese results found")

    return all_results


async def search_annas_archive_async(
    title: str,
    author: str = "",
    headless: bool = True,
    browser=None,
    context=None,
    preferred_format: str = "pdf",
) -> List[Dict]:
    """Async wrapper for search (same as sync version, for compatibility)."""
    return search_annas_archive(title, author, preferred_format)


async def get_download_page(
    md5: str,
    mirror_domain: str,
    headless: bool = True,
    browser=None,
    context=None,
) -> Optional[Dict]:
    """
    Get book detail page and extract download options (requires Playwright).
    """
    if "playwright" not in sys.modules:
        return None

    _owns_browser = browser is None
    _owns_context = context is None
    try:
        if _owns_browser:
            pw = await async_playwright().start()
            browser, context = await _create_stealth_context(pw, headless)
        elif _owns_context:
            # Browser provided but not context - create context from browser
            context = await browser.new_context(
                user_agent=_USER_AGENT,
                viewport={"width": 1920, "height": 1080},
                locale="zh-CN",
            )
            await context.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
                window.chrome = { runtime: {} };
            """)

        page = await context.new_page()
        try:
            url = f"{mirror_domain}/md5/{md5}"
            await page.goto(url, timeout=15000, wait_until="commit")
            await asyncio.sleep(3)

            result = await page.evaluate("""() => {
                const data = {
                    slow_download_urls: [],
                    fast_download_urls: [],
                    external_urls: [],
                    torrent_url: '',
                    info: {}
                };
                document.querySelectorAll('a').forEach(a => {
                    const href = a.getAttribute('href') || '';
                    const text = a.textContent.trim();
                    if (href.includes('/slow_download/')) data.slow_download_urls.push(href);
                    else if (href.includes('/fast_download/')) data.fast_download_urls.push(href);
                    else if (
                        (href.includes('z-lib') || href.includes('libgen'))
                        && text.length > 3 && text.length < 80
                    ) data.external_urls.push({text, href});
                    else if (href.includes('.torrent')) data.torrent_url = href;
                });
                return data;
            }""")
            return result
        finally:
            await page.close()
    except Exception as e:
        print(f"  Detail page error: {e}")
        return None
    finally:
        if _owns_context and context:
            await context.close()
        if _owns_browser and browser:
            await browser.close()


async def _create_stealth_context(playwright, headless: bool = True):
    """Create a browser context with anti-detection measures."""
    browser = await playwright.chromium.launch(
        headless=headless,
        args=["--disable-blink-features=AutomationControlled"],
    )
    context = await browser.new_context(
        user_agent=_USER_AGENT,
        viewport={"width": 1920, "height": 1080},
        locale="zh-CN",
    )
    await context.add_init_script("""
        Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
        window.chrome = { runtime: {} };
    """)
    return browser, context


async def try_download_libgen(
    md5: str,
    mirror_domain: str,
    output_path: str,
    headless: bool = True,
    browser=None,
    context=None,
) -> Dict:
    """Try to download via libgen.li external link from book detail page."""
    if "playwright" not in sys.modules:
        return {"status": "failed", "error": "Playwright not available"}

    _owns_browser = browser is None
    _owns_context = context is None
    try:
        if _owns_browser:
            pw = await async_playwright().start()
            browser, context = await _create_stealth_context(pw, headless)
        elif _owns_context:
            # Browser provided but not context - create context from browser
            context = await browser.new_context(
                user_agent=_USER_AGENT,
                viewport={"width": 1920, "height": 1080},
                locale="zh-CN",
            )
            await context.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
                window.chrome = { runtime: {} };
            """)

        page = await context.new_page()
        try:
            # Visit main page first to get DDoS-Guard cookies
            print(f"  Loading detail page for external links...")
            await page.goto(mirror_domain, wait_until="domcontentloaded", timeout=30000)
            await asyncio.sleep(4)

            # Go to book detail page
            url = f"{mirror_domain}/md5/{md5}"
            await page.goto(url, wait_until="domcontentloaded", timeout=30000)
            await asyncio.sleep(3)

            # Extract libgen.li file link
            external_info = await page.evaluate("""() => {
                const links = document.querySelectorAll('a');
                for (const a of links) {
                    const href = a.getAttribute('href') || '';
                    if (href.includes('libgen.li/file.php')) {
                        return {libgen_url: href, text: a.textContent.trim().substring(0, 80)};
                    }
                }
                return {libgen_url: null};
            }""")
            libgen_url = external_info.get("libgen_url")
            if not libgen_url:
                return {"status": "failed", "error": "No libgen.li link found on detail page"}

            print(f"  Found libgen.li link, trying direct download...")

            # Try downloading directly via curl from libgen.li
            cmd = [
                "curl", "-L", "-o", output_path, libgen_url,
                "-H", f"User-Agent: {_USER_AGENT}",
                "-H", f"Referer: {url}",
                "--max-time", "600", "--connect-timeout", "30",
            ]
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                size = os.path.getsize(output_path) if os.path.exists(output_path) else 0
                if size > 1024:
                    # Verify it's not an HTML error page
                    with open(output_path, 'rb') as f:
                        head = f.read(100)
                    if head[:5] in (b'%PDF-', b'PK\x03\x04', b'\x89PNG'):
                        return {"status": "done", "path": output_path, "size": size}
                    if b'<html' in head[:50].lower() or b'<!doct' in head[:50].lower():
                        os.remove(output_path)
                        return {"status": "failed", "error": "Downloaded HTML error page instead of file"}

            return {"status": "failed", "error": "libgen.li download failed"}
        finally:
            await page.close()
    except Exception as e:
        print(f"  libgen download error: {e}")
        return {"status": "failed", "error": str(e)}
    finally:
        if _owns_context and context:
            await context.close()
        if _owns_browser and browser:
            await browser.close()


async def try_download_slow(
    md5: str,
    mirror_domain: str,
    output_path: str,
    headless: bool = True,
    browser=None,
    context=None,
    max_partners: int = 3,
) -> Dict:
    """Attempt download from slow partner servers via Playwright."""
    if "playwright" not in sys.modules:
        return {"status": "failed", "error": "Playwright not available"}

    _owns_browser = browser is None
    _owns_context = context is None
    try:
        if _owns_browser:
            pw = await async_playwright().start()
            browser, context = await _create_stealth_context(pw, headless)
        elif _owns_context:
            # Browser provided but not context - create context from browser
            context = await browser.new_context(
                user_agent=_USER_AGENT,
                viewport={"width": 1920, "height": 1080},
                locale="zh-CN",
            )
            await context.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
                window.chrome = { runtime: {} };
            """)

        for partner_idx in range(max_partners):
            page = await context.new_page()
            try:
                url = f"{mirror_domain}/slow_download/{md5}/0/{partner_idx}"
                print(f"  Trying slow partner #{partner_idx + 1}...")
                await page.goto(url, timeout=20000, wait_until="commit")

                # Wait for countdown (up to 45 seconds) checking every 5 seconds
                dl_link = None
                for wait_sec in range(9):
                    await asyncio.sleep(5)
                    elapsed = (wait_sec + 1) * 5
                    
                    dl_link = await page.evaluate("""() => {
                        // Check for external download link that appears after countdown
                        const links = document.querySelectorAll('a');
                        for (const a of links) {
                            const href = a.getAttribute('href') || '';
                            if (href.startsWith('http') && !href.includes('annas-archive') 
                                && !href.includes('reddit') && !href.includes('matrix')
                                && !href.includes('translate') && !href.includes('software.')
                                && !href.includes('open-slum') && !href.includes('jdownloader')
                                && href.length > 20 && !href.includes('javascript')) {
                                return href;
                            }
                        }
                        return null;
                    }""")
                    
                    if dl_link:
                        print(f"  Download link found after {elapsed}s")
                        break
                    
                    # Check if we're still on the countdown page
                    text = await page.evaluate('() => document.body.innerText')
                    if 'Please wait' not in text and 'countdown' not in text.lower():
                        # Page might have loaded or been redirected
                        url_now = page.url
                        if 'slow_download' not in url_now:
                            print(f"  Page redirected away from slow_download after {elapsed}s")
                            break
                
                if dl_link:
                    cmd = ["curl", "-L", "-o", output_path, dl_link,
                           "-H", f"User-Agent: {_USER_AGENT}",
                           "-H", f"Referer: {url}",
                           "--max-time", "600", "--connect-timeout", "30"]
                    result = subprocess.run(cmd, capture_output=True, text=True)
                    if result.returncode == 0:
                        size = os.path.getsize(output_path) if os.path.exists(output_path) else 0
                        if size > 1024:
                            with open(output_path, 'rb') as f:
                                head = f.read(100)
                            if head[:5] in (b'%PDF-', b'PK\x03\x04', b'\x89PNG') or b'<html' not in head[:50].lower():
                                return {"status": "done", "path": output_path, "size": size}
                            else:
                                os.remove(output_path)
                    return {"status": "failed", "error": "Download failed or got error page"}
                
                return {"status": "blocked", "error": f"No download link after countdown (partner #{partner_idx+1})"}
                print(f"  Partner #{partner_idx + 1} error: {e}")
            finally:
                await page.close()

        return {"status": "blocked", "error": "All partners blocked by DDoS-Guard"}
    except Exception as e:
        print(f"  slow download error: {e}")
        return {"status": "failed", "error": str(e)}
    finally:
        if _owns_context and context:
            await context.close()
        if _owns_browser and browser:
            await browser.close()


async def download_book_from_annas_archive(
    title: str,
    author: str,
    output_dir: str,
    preferred_format: str = "pdf",
    headless: bool = True,
    browser=None,
    context=None,
) -> Dict:
    """Full download flow: search → find best result → attempt download."""
    import re

    # Search without format filter to get all available results
    # The format preference is handled when selecting the best result
    results = search_annas_archive(title, author, "any")
    if not results:
        return {"status": "not_found", "error": "No results on Anna's Archive"}

    # Prefer the requested format, but fall back to any available
    if preferred_format != "any":
        preferred_results = [r for r in results if r.get("format", "").lower() == preferred_format.lower()]
        if preferred_results:
            results = preferred_results

    best = results[0]
    print(f"  Best match: {best['title'][:50]} [{best['format']}] ({best['source']})")

    if preferred_format != "any" and best.get("format"):
        if best["format"].lower() != preferred_format.lower():
            print(f"  ⚠️  Format mismatch: wanted {preferred_format}, got {best['format']}")

    # Try download via browser
    clean_name = re.sub(r'[\\/:*?"<>|]', ' ', f"{title} - {author}").strip()
    ext = best.get("format", preferred_format if preferred_format != "any" else "pdf")
    output_path = os.path.join(output_dir, f"{clean_name}.{ext}")

    # Strategy 1: Try libgen.li external link (most reliable for direct download)
    dl_result = await try_download_libgen(
        best["md5"], best["mirror_domain"], output_path,
        headless=headless, browser=browser, context=context,
    )
    if dl_result["status"] == "done":
        return {"status": "done", "files": [output_path], "source": f"annas-archive→libgen ({best['source']})"}

    print(f"  libgen.li failed: {dl_result.get('error', 'unknown')}")

    # Strategy 2: Try slow download partners via browser
    dl_result = await try_download_slow(
        best["md5"], best["mirror_domain"], output_path,
        headless=headless, browser=browser, context=context,
    )

    if dl_result["status"] == "done":
        return {"status": "done", "files": [output_path], "source": f"annas-archive ({best['source']})"}

    return {
        "status": "blocked",
        "error": dl_result.get("error", "Download blocked"),
        "search_results": results[:3],
        "manual_url": best["mirror_url"],
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Usage: python search_source_c.py "书名" ["作者"]')
        sys.exit(1)

    title = sys.argv[1]
    author = sys.argv[2] if len(sys.argv) > 2 else ""

    results = search_annas_archive(title, author)

    if results:
        print(f"\nFound {len(results)} result(s):")
        for i, r in enumerate(results):
            print(f"  [{i+1}] {r['title'][:60]}")
            print(f"      Format: {r['format']} | Size: {r['size']} | Year: {r['year']}")
            print(f"      Source: {r['source']} | Score: {r['score']:.2f}")
            print(f"      URL: {r['mirror_url']}")
    else:
        print("\nNo results found")
