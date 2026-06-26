#!/usr/bin/env python3
"""Fetch a paywall article by extracting Chrome cookies and using them in Playwright.

Supports two browser modes:
1. **CDP mode** (--cdp, recommended for Cloudflare-protected or login-required sites):
   Connects to the user's real Chrome browser via Chrome DevTools Protocol (CDP)
   on port 9222. This completely bypasses Google's anti-automation detection and
   Cloudflare's bot detection because it IS the user's real Chrome — with full
   login state (cookies, localStorage, etc.).
   Requires Chrome to be running with --remote-debugging-port=9222.
   Automatically detects and waits for Cloudflare JS challenges.

2. **Cookie injection mode** (default):
   Reads cookies from Chrome's cookie database and injects them into a fresh
   Playwright browser context. Works for most sites but Google login pages
   and Cloudflare-protected sites may detect the automation and block it.

Image handling:
   Downloaded images are automatically inspected for format mismatches
   (e.g. WebP served as .png, SVG served as .png) and converted to real
   PNG for maximum compatibility with PDF generators and document editors.

Usage:
    # CDP mode (for OpenAI, LinkedIn, Cloudflare-protected sites)
    python fetch_article.py fetch <URL> --output-dir <dir> --cdp

    # Cookie injection mode (default, for Substack etc.)
    python fetch_article.py fetch <URL> --output-dir <dir>
"""
from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
import os
import platform
import re
import shutil
import socket
import sqlite3
import subprocess
import sys
import tempfile
import urllib.parse
from pathlib import Path

# CDP debugging port for connecting to real Chrome
CDP_PORT = 9222

# Substack session persistence
SUBSTACK_STORAGE_DIR = Path.home() / ".substack"
SUBSTACK_STORAGE_PATH = SUBSTACK_STORAGE_DIR / "storage_state.json"


# ── CDP helper functions ──────────────────────────────────────────────

def _find_chrome_executable() -> str | None:
    """Find the Chrome/Chromium executable on the current system."""
    if platform.system() == "Darwin":
        candidates = [
            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            "/Applications/Chromium.app/Contents/MacOS/Chromium",
        ]
    elif platform.system() == "Windows":
        candidates = [
            os.path.expandvars(r"%ProgramFiles%\Google\Chrome\Application\chrome.exe"),
            os.path.expandvars(r"%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe"),
            os.path.expandvars(r"%LocalAppData%\Google\Chrome\Application\chrome.exe"),
        ]
    else:
        candidates = ["/usr/bin/google-chrome", "/usr/bin/chromium"]
        found = shutil.which("google-chrome") or shutil.which("chromium")
        if found:
            candidates.insert(0, found)
    for path in candidates:
        if os.path.isfile(path):
            return path
    return None


def _get_chrome_user_data_dir() -> str:
    """Return the user's default Chrome profile directory."""
    if platform.system() == "Darwin":
        default_dir = Path.home() / "Library" / "Application Support" / "Google" / "Chrome"
    elif platform.system() == "Windows":
        default_dir = Path(os.environ.get("LOCALAPPDATA", "")) / "Google" / "Chrome" / "User Data"
    else:
        default_dir = Path.home() / ".config" / "google-chrome"
    if default_dir.exists():
        return str(default_dir)
    fallback = Path.home() / ".fetch_article" / "chrome_user_data"
    fallback.mkdir(parents=True, exist_ok=True)
    return str(fallback)


def _is_chrome_running() -> bool:
    """Check if Chrome is currently running."""
    try:
        if platform.system() == "Darwin":
            result = subprocess.run(["pgrep", "-f", "Google Chrome"], capture_output=True, timeout=5)
            return result.returncode == 0
        elif platform.system() == "Windows":
            result = subprocess.run(["tasklist", "/FI", "IMAGENAME eq chrome.exe"], capture_output=True, text=True, timeout=5)
            return "chrome.exe" in result.stdout
        else:
            result = subprocess.run(["pgrep", "-f", "chrome"], capture_output=True, timeout=5)
            return result.returncode == 0
    except Exception:
        return False


_chrome_process: subprocess.Popen | None = None


async def _ensure_chrome_cdp(port: int = CDP_PORT) -> bool:
    """Ensure Chrome is running with CDP enabled on the given port.

    macOS Chrome REQUIRES a non-default --user-data-dir for CDP to work.
    Using the default dir will silently skip the CDP port. We always use
    a dedicated CDP profile directory (~/.fetch_article/chrome_cdp_profile).

    If Chrome is already listening on the port, returns True immediately.
    Otherwise, launches Chrome with --remote-debugging-port.
    """
    global _chrome_process

    # Check if port is already in use
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.settimeout(1)
        sock.connect(("127.0.0.1", port))
        sock.close()
        print(f"✅ Chrome 已在端口 {port} 运行，直接连接")
        return True
    except (ConnectionRefusedError, OSError):
        pass
    finally:
        sock.close()

    # Need to launch Chrome with CDP
    chrome_path = _find_chrome_executable()
    if not chrome_path:
        print("❌ 未找到系统 Chrome 浏览器")
        return False

    # Always use a dedicated CDP profile directory (NOT the default Chrome dir).
    # macOS Chrome refuses to open the CDP port when using the default
    # user-data-dir.
    # However, we copy cookies from the real profile to the CDP profile
    # to preserve login state.
    cdp_profile_dir = str(Path.home() / ".fetch_article" / "chrome_cdp_profile")
    os.makedirs(cdp_profile_dir, exist_ok=True)

    # Copy cookies from the real Chrome profile to CDP profile if available
    real_chrome_dir = _get_chrome_user_data_dir()
    real_cookies = Path(real_chrome_dir) / "Default" / "Cookies"
    cdp_cookies = Path(cdp_profile_dir) / "Default" / "Cookies"
    if real_cookies.exists():
        os.makedirs(str(cdp_cookies.parent), exist_ok=True)
        try:
            shutil.copy2(str(real_cookies), str(cdp_cookies))
            print(f"🍪 已同步真实 Chrome 的 cookies 到 CDP profile")
        except Exception as e:
            print(f"⚠️  Cookies 同步失败: {e}")

    cmd = [
        chrome_path,
        f"--remote-debugging-port={port}",
        f"--user-data-dir={cdp_profile_dir}",
        "--no-first-run",
        "--no-default-browser-check",
        "--disable-default-apps",
        "--disable-popup-blocking",
        "--disable-translate",
        "--window-size=1440,900",
    ]

    # Auto-detect proxy
    proxy = (
        os.environ.get("https_proxy") or os.environ.get("HTTPS_PROXY")
        or os.environ.get("http_proxy") or os.environ.get("HTTP_PROXY")
    )
    if not proxy and platform.system() == "Darwin":
        for proxy_cmd in ["getsecurewebproxy", "getwebproxy"]:
            try:
                result = subprocess.run(
                    ["networksetup", f"-{proxy_cmd}", "Wi-Fi"],
                    capture_output=True, text=True, timeout=5,
                )
                enabled = server = port_str = ""
                for line in result.stdout.splitlines():
                    if line.startswith("Enabled: Yes"):
                        enabled = True
                    elif line.startswith("Server:"):
                        server = line.split(":", 1)[1].strip()
                    elif line.startswith("Port:"):
                        port_str = line.split(":", 1)[1].strip()
                if enabled and server and port_str:
                    proxy = f"http://{server}:{port_str}"
                    break
            except Exception:
                pass
    if proxy:
        cmd.append(f"--proxy-server={proxy}")
        print(f"🌐 使用代理: {proxy}")

    print(f"🚀 启动 Chrome CDP (profile: {cdp_profile_dir})")
    _chrome_process = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)

    # Wait for CDP port
    for _ in range(30):
        await asyncio.sleep(1)
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            sock.connect(("127.0.0.1", port))
            sock.close()
            print(f"✅ Chrome CDP 就绪 (port {port})")
            return True
        except (ConnectionRefusedError, OSError):
            pass
        finally:
            sock.close()

    # Read stderr for clues
    if _chrome_process and _chrome_process.poll() is not None:
        stderr_out = _chrome_process.stderr.read().decode(errors="replace") if _chrome_process.stderr else ""
        if stderr_out:
            print(f"❌ Chrome 启动失败:\n{stderr_out[:500]}")

    print("❌ Chrome CDP 启动超时（30s 内端口未就绪）")
    return False


async def _create_cdp_context(playwright):
    """Connect to real Chrome via CDP and return (browser, context, page).
    
    Falls back to Playwright's bundled Chromium with Chrome cookie injection
    if CDP connection fails (e.g., Chrome 147+ removed setDownloadBehavior).
    """
    # Try CDP first
    launched = await _ensure_chrome_cdp(CDP_PORT)
    if launched:
        try:
            browser = await playwright.chromium.connect_over_cdp(f"http://127.0.0.1:{CDP_PORT}")
            if browser.contexts:
                context = browser.contexts[0]
                print("🔗 已连接到真实 Chrome（复用已有上下文）")
            else:
                context = await browser.new_context(viewport={"width": 1440, "height": 900})
                print("🔗 已连接到真实 Chrome（新建上下文）")
            page = await context.new_page()
            return browser, context, page
        except Exception as e:
            print(f"⚠️  CDP 连接失败: {str(e)[:100]}")
            print("🔄 回退到 Playwright Chromium + Chrome Cookie 注入模式...")

    # Fallback: use Playwright's bundled Chromium with cookie injection
    browser = await playwright.chromium.launch(
        headless=False,
        args=[
            "--disable-blink-features=AutomationControlled",
            "--no-first-run",
            "--no-default-browser-check",
        ],
    )
    context = await browser.new_context(viewport={"width": 1440, "height": 900})
    
    # Inject cookies from real Chrome for common Substack domains
    for domain in ["substack.com", "creatoreconomy.so", "sachinrekhi.com", "speedrun.substack.com"]:
        try:
            cookies = get_chrome_cookies_for_domain(domain)
            if cookies:
                await context.add_cookies(cookies)
                print(f"🍪 已注入 {domain} 的 {len(cookies)} 个 cookies")
        except Exception:
            pass
    
    page = await context.new_page()
    print("🔗 已启动 Playwright Chromium（Cookie 注入回退模式）")
    return browser, context, page


# ── Cookie extraction functions ───────────────────────────────────────

def get_chrome_cookies_for_domain(domain: str) -> list[dict]:
    """Extract cookies for a domain from Chrome's cookie database.
    
    On macOS, Chrome encrypts cookies with the Keychain.
    We use a simpler approach: copy the Cookies db and read what we can,
    or use the `security` command to decrypt.
    """
    chrome_dir = Path.home() / "Library/Application Support/Google/Chrome/Default"
    cookies_db = chrome_dir / "Cookies"

    if not cookies_db.exists():
        print(f"❌ Chrome Cookies 数据库不存在: {cookies_db}")
        return []

    # Copy the database (Chrome locks it while running)
    tmp_db = Path(tempfile.mktemp(suffix=".db"))
    shutil.copy2(cookies_db, tmp_db)

    try:
        conn = sqlite3.connect(str(tmp_db))
        cursor = conn.cursor()

        # Query cookies for the domain
        cursor.execute(
            """SELECT host_key, name, path, encrypted_value, value, 
                      is_secure, is_httponly, expires_utc, samesite
               FROM cookies 
               WHERE host_key LIKE ? OR host_key LIKE ?""",
            (f"%{domain}%", f"%.{domain}%"),
        )

        rows = cursor.fetchall()
        conn.close()

        if not rows:
            print(f"⚠️  未找到 {domain} 的 cookies")
            return []

        # On macOS, cookies are encrypted. We need to decrypt them.
        # Get the Chrome Safe Storage key from Keychain
        try:
            result = subprocess.run(
                [
                    "security",
                    "find-generic-password",
                    "-s",
                    "Chrome Safe Storage",
                    "-w",
                ],
                capture_output=True,
                text=True,
            )
            safe_storage_key = result.stdout.strip()
        except Exception:
            safe_storage_key = None

        cookies = []
        if safe_storage_key:
            # Decrypt cookies using the safe storage key
            import hashlib as hl

            # Derive the key using PBKDF2
            from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
            from cryptography.hazmat.primitives import hashes
            from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA1(),
                length=16,
                salt=b"saltysalt",
                iterations=1003,
            )
            derived_key = kdf.derive(safe_storage_key.encode("utf-8"))

            for row in rows:
                host_key, name, path, encrypted_value, value, is_secure, is_httponly, expires_utc, samesite = row

                if value:
                    # Unencrypted cookie
                    cookie_value = value
                elif encrypted_value and encrypted_value[:3] == b"v10":
                    # Decrypt v10 encrypted cookie
                    try:
                        iv = b" " * 16
                        cipher = Cipher(algorithms.AES(derived_key), modes.CBC(iv))
                        decryptor = cipher.decryptor()
                        decrypted = decryptor.update(encrypted_value[3:]) + decryptor.finalize()
                        # Remove PKCS7 padding
                        padding_len = decrypted[-1]
                        cookie_value = decrypted[:-padding_len].decode("utf-8")
                    except Exception as e:
                        continue
                else:
                    continue

                # Convert Chrome timestamp to Unix (Chrome uses microseconds since 1601-01-01)
                if expires_utc > 0:
                    expires = (expires_utc / 1_000_000) - 11644473600
                else:
                    expires = -1

                same_site_map = {0: "None", 1: "Lax", 2: "Strict", -1: "None"}
                
                cookies.append({
                    "name": name,
                    "value": cookie_value,
                    "domain": host_key,
                    "path": path,
                    "secure": bool(is_secure),
                    "httpOnly": bool(is_httponly),
                    "sameSite": same_site_map.get(samesite, "None"),
                    "expires": expires if expires > 0 else -1,
                })

        print(f"🍪 提取到 {len(cookies)} 个 {domain} cookies")
        return cookies

    finally:
        tmp_db.unlink(missing_ok=True)


def _is_substack_site(url: str) -> bool:
    """Check if the URL belongs to a Substack-hosted site."""
    parsed = urllib.parse.urlparse(url)
    hostname = parsed.hostname or ""
    # Known Substack domains
    substack_domains = [
        "substack.com",
        "lennysnewsletter.com",
        "www.lennysnewsletter.com",
        "creatoreconomy.so",
        "sachinrekhi.com",
        "www.sachinrekhi.com",
        "speedrun.substack.com",
    ]
    # Check direct match or *.substack.com pattern
    for d in substack_domains:
        if hostname == d or hostname.endswith(f".{d}"):
            return True
    if "substack.com" in hostname:
        return True
    return False


def _is_wechat_article(url: str) -> bool:
    """Check if the URL is a WeChat Official Account (微信公众号) article."""
    parsed = urllib.parse.urlparse(url)
    hostname = parsed.hostname or ""
    return hostname in ("mp.weixin.qq.com", "weixin.qq.com")


def _is_dedao_article(url: str) -> bool:
    """Check if the URL is a Dedao (得到) article."""
    parsed = urllib.parse.urlparse(url)
    hostname = parsed.hostname or ""
    return "dedao.cn" in hostname


def _is_webflow_blog(url: str) -> bool:
    """Check if the URL is a Webflow-based blog (claude.com, anthropic.com).

    These sites use `.u-rich-text-blog` or `.w-richtext` containers,
    which are NOT matched by the generic content selectors. Requires
    site-specific selector handling.
    """
    parsed = urllib.parse.urlparse(url)
    hostname = parsed.hostname or ""
    return any(d in hostname for d in ("claude.com", "anthropic.com"))


# Known Cloudflare-protected domains that typically require CDP mode
_CLOUDFLARE_DOMAINS = {
    "openai.com",
    "platform.openai.com",
    "chatgpt.com",
}


def _is_cloudflare_likely(url: str) -> bool:
    """Check if the URL belongs to a site known to use Cloudflare protection.

    These sites will typically fail with cookie-injection mode and need CDP.
    """
    parsed = urllib.parse.urlparse(url)
    hostname = parsed.hostname or ""
    for cf_domain in _CLOUDFLARE_DOMAINS:
        if hostname == cf_domain or hostname.endswith(f".{cf_domain}"):
            return True
    return False


async def _check_substack_login(page) -> dict:
    """Check Substack login status by examining the page header.
    
    Returns:
        dict with keys:
        - logged_in (bool): True if user avatar is found (not "sign in" button)
        - has_paywall (bool): True if paywall is detected
        - content_length (int): length of visible article content
        - detail (str): human-readable status
    """
    result = await page.evaluate("""() => {
        // --- Login detection ---
        // Logged-in: top-right shows user avatar image inside a button/link
        // Not logged-in: shows "Sign in" button/link
        const signInBtn = document.querySelector(
            'a[href*="sign-in"], a[href*="signin"], a[href*="/login"], ' +
            '[data-testid="sign-in-button"], .login-button'
        );
        // Broader text search for "sign in" in the header area
        let hasSignInText = false;
        const headerLinks = document.querySelectorAll('header a, nav a, .navbar a, .pencraft a, button');
        for (const link of headerLinks) {
            const text = (link.innerText || '').trim().toLowerCase();
            if (text === 'sign in' || text === 'login' || text === 'log in') {
                hasSignInText = true;
                break;
            }
        }
        
        // Check for user avatar (indicates logged in)
        const avatarImg = document.querySelector(
            '.user-indicator img, .navbar-right img[class*="avatar"], ' +
            'header img.user-icon, button img[class*="avatar"], ' +
            '.pencraft img[class*="profile"], img.navbar-profile-image, ' +
            '.substack-account img'
        );
        // Also check for profile dropdown button (common in Substack)
        const profileBtn = document.querySelector(
            'button[aria-label*="profile"], button[aria-label*="account"], ' +
            'button[aria-label*="menu"], .profile-button'
        );
        
        // Broader avatar check: any small circular img in header/nav area
        let hasAvatarInHeader = false;
        const headerImgs = document.querySelectorAll('header img, nav img, .navbar img, .pencraft img');
        for (const img of headerImgs) {
            const w = img.naturalWidth || img.width || 0;
            const h = img.naturalHeight || img.height || 0;
            const src = img.src || '';
            // Avatar images are typically small and square-ish, from substackcdn
            if (src.includes('substackcdn') && w > 0 && w <= 100 && h > 0 && h <= 100) {
                hasAvatarInHeader = true;
                break;
            }
            // Or any small image that looks like a profile pic
            if (w > 16 && w <= 60 && h > 16 && h <= 60 && !src.includes('logo') && !src.includes('icon')) {
                hasAvatarInHeader = true;
                break;
            }
        }
        
        const loggedIn = (!!avatarImg || !!profileBtn || hasAvatarInHeader) && !signInBtn && !hasSignInText;
        
        // --- Paywall detection ---
        const paywallEl = document.querySelector('[data-testid="paywall"], .paywall, .paywall-title');
        const body = document.body.innerText;
        const hasPaywall = !!paywallEl ||
            body.includes('This post is for paid subscribers') ||
            body.includes('This post is for paying subscribers') ||
            body.includes('Subscribe to read') ||
            body.includes('Upgrade to paid');
        
        // --- Content length ---
        const contentEl = document.querySelector('.available-content, .post-content, article .body, article');
        const contentLength = contentEl ? contentEl.innerText.length : 0;
        
        return {
            loggedIn,
            hasSignIn: !!signInBtn || hasSignInText,
            hasAvatar: !!avatarImg || !!profileBtn || hasAvatarInHeader,
            hasPaywall,
            contentLength,
        };
    }""")
    
    if result["loggedIn"]:
        detail = f"✅ 已登录（检测到用户头像），内容 {result['contentLength']} 字符"
        if result["hasPaywall"]:
            detail += "，但仍检测到付费墙（可能需要付费订阅）"
    elif result["hasSignIn"]:
        detail = "❌ 未登录（检测到 Sign in 按钮）"
    else:
        detail = f"⚠️  登录状态不确定（无头像也无登录按钮），内容 {result['contentLength']} 字符"
    
    return {
        "logged_in": result["loggedIn"],
        "has_paywall": result["hasPaywall"],
        "content_length": result["contentLength"],
        "detail": detail,
    }


async def _guide_substack_login(page, browser, context, url: str) -> tuple:
    """Guide user through Substack login process.
    
    Closes the headless browser and reopens in visible mode for login.
    Returns (new_browser, new_context, new_page) after successful login.
    """
    print("\n" + "=" * 60)
    print("🔐 Substack 登录引导")
    print("=" * 60)
    print("检测到您尚未登录 Substack。需要登录才能查看付费文章全文。")
    print("")
    print("即将打开可见浏览器窗口，请完成以下操作：")
    print("  1. 在浏览器中点击右上角 'Sign in' 登录您的 Substack 账号")
    print("  2. 确保登录的账号有该文章的付费订阅权限")
    print("  3. 登录成功后，页面右上角应显示您的头像（而非 'Sign in' 按钮）")
    print("  4. 回到终端，输入 'y' 确认登录成功")
    print("")
    print("⚠️  重要：请等待登录完全成功后再确认！")
    print("=" * 60)
    
    # Close headless browser and reopen in visible mode
    await browser.close()
    
    from playwright.async_api import async_playwright
    pw = await async_playwright().__aenter__()
    new_browser = await pw.chromium.launch(headless=False)
    new_context = await new_browser.new_context(
        viewport={"width": 1280, "height": 900},
        user_agent=(
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/131.0.0.0 Safari/537.36"
        ),
    )
    new_page = await new_context.new_page()
    
    print("\n📥 正在打开页面...")
    try:
        await new_page.goto(url, wait_until="networkidle", timeout=60000)
    except Exception as e:
        print(f"⚠️  页面加载超时，继续: {e}")
        await new_page.wait_for_timeout(5000)
    
    # Wait for user confirmation
    max_attempts = 5
    for attempt in range(max_attempts):
        try:
            user_input = await asyncio.get_event_loop().run_in_executor(
                None, lambda: input("\n⏳ 登录完成后请输入 'y' 确认（输入 'q' 取消）: ")
            )
        except (EOFError, KeyboardInterrupt):
            print("\n⚠️  stdin 不可用，等待 30 秒后自动检测...")
            await new_page.wait_for_timeout(30000)
            user_input = "y"
        
        user_input = user_input.strip().lower()
        if user_input == "q":
            print("❌ 用户取消登录，将尝试抓取当前可见内容")
            break
        
        if user_input == "y":
            # Reload the target page to check login status
            print("🔄 正在重新加载页面并验证登录状态...")
            try:
                await new_page.goto(url, wait_until="networkidle", timeout=60000)
            except Exception:
                await new_page.wait_for_timeout(5000)
            await new_page.wait_for_timeout(3000)
            
            login_status = await _check_substack_login(new_page)
            print(f"   {login_status['detail']}")
            
            if login_status["logged_in"]:
                print("✅ 登录验证通过！正在保存登录态...")
                # Save storage state for future sessions
                SUBSTACK_STORAGE_DIR.mkdir(parents=True, exist_ok=True)
                await new_context.storage_state(path=str(SUBSTACK_STORAGE_PATH))
                print(f"💾 登录态已缓存到 {SUBSTACK_STORAGE_PATH}")
                break
            else:
                remaining = max_attempts - attempt - 1
                if remaining > 0:
                    print(f"⚠️  登录验证未通过。请确认已在浏览器中成功登录（还有 {remaining} 次确认机会）")
                else:
                    print("⚠️  多次验证未通过，将尝试抓取当前可见内容")
        else:
            print("请输入 'y' 确认登录成功，或 'q' 取消")
    
    return new_browser, new_context, new_page, pw


async def _wait_for_cloudflare(page, max_wait: int = 30) -> bool:
    """Detect and wait for Cloudflare challenge/interstitial pages to resolve.

    Cloudflare JS challenges typically show a "Just a moment..." title or
    a turnstile CAPTCHA widget.  When the user's real Chrome is connected
    via CDP, the challenge usually auto-resolves in 5-15 seconds.

    Returns True if a challenge was detected (and hopefully resolved).
    """
    for attempt in range(max_wait // 2):
        is_cf = await page.evaluate("""() => {
            const title = document.title.toLowerCase();
            // Cloudflare interstitial titles
            if (title.includes('just a moment') ||
                title.includes('attention required') ||
                title.includes('checking your browser') ||
                title.includes('请稍候')) return true;
            // Cloudflare-specific elements
            if (document.querySelector('#challenge-running, #challenge-stage, .cf-turnstile, #cf-challenge-running'))
                return true;
            // Very short body text (likely a challenge, not real content)
            const bodyLen = (document.body && document.body.innerText) ? document.body.innerText.length : 0;
            if (bodyLen < 200 && (title === '' || title.includes('moment'))) return true;
            return false;
        }""")
        if not is_cf:
            if attempt > 0:
                print(f"✅ Cloudflare challenge 已通过（等待 {attempt * 2}s）")
            return attempt > 0
        if attempt == 0:
            print("🛡️  检测到 Cloudflare challenge，等待自动验证...")
        await page.wait_for_timeout(2000)

    print("⚠️  Cloudflare challenge 等待超时，尝试继续提取内容")
    return True


def _convert_image_format(img_path: Path) -> bool:
    """Detect real image format and convert WebP/SVG to PNG if necessary.

    Many sites (e.g. OpenAI) serve WebP images but the URL path ends with
    .png/.jpg, causing PyMuPDF and other tools to fail.  This function
    inspects the actual file header and converts if needed.

    Returns True if conversion was performed.
    """
    if not img_path.exists():
        return False

    # Read first few bytes to detect format
    with open(img_path, "rb") as f:
        header = f.read(32)

    is_webp = header[:4] == b"RIFF" and header[8:12] == b"WEBP"
    is_svg = header.lstrip()[:5] in (b"<?xml", b"<svg ", b"<svg\n") or b"<svg" in header[:200]

    if not is_webp and not is_svg:
        return False

    if is_webp:
        try:
            from PIL import Image
            img = Image.open(str(img_path))
            tmp_path = img_path.with_suffix(".converted.png")
            img.save(str(tmp_path), "PNG")
            os.replace(str(tmp_path), str(img_path))
            return True
        except ImportError:
            # Fallback: try sips on macOS
            if platform.system() == "Darwin":
                try:
                    tmp_path = str(img_path) + ".converted.png"
                    subprocess.run(
                        ["sips", "-s", "format", "png", str(img_path), "--out", tmp_path],
                        capture_output=True, timeout=30,
                    )
                    if os.path.isfile(tmp_path):
                        os.replace(tmp_path, str(img_path))
                        return True
                except Exception:
                    pass
        except Exception:
            pass

    if is_svg:
        # Try rendering SVG via Playwright (headless)
        try:
            import asyncio as _aio
            from playwright.async_api import async_playwright as _ap

            async def _render():
                svg_text = img_path.read_text(encoding="utf-8", errors="replace")
                html = (
                    "<!DOCTYPE html><html><head>"
                    "<style>body{margin:0;padding:0;background:white;}</style>"
                    f"</head><body>{svg_text}</body></html>"
                )
                async with _ap() as pw:
                    br = await pw.chromium.launch(headless=True)
                    pg = await br.new_page(viewport={"width": 1600, "height": 1200})
                    await pg.set_content(html)
                    await pg.wait_for_timeout(800)
                    el = await pg.query_selector("svg")
                    if el:
                        tmp = str(img_path) + ".converted.png"
                        await el.screenshot(path=tmp)
                        os.replace(tmp, str(img_path))
                    await br.close()

            _aio.get_event_loop().run_until_complete(_render())
            return True
        except Exception:
            pass

    return False


async def _scroll_page(page, is_wechat: bool = False, is_dedao: bool = False):
    """Scroll the page to trigger lazy-loaded content.
    
    For WeChat articles, uses a more thorough scrolling strategy to ensure
    all lazy-loaded images (data-src → src) are triggered.
    For Dedao (SPA), waits longer for JS rendering.
    """
    if is_wechat:
        # WeChat uses IntersectionObserver for lazy-loading images.
        # We need slower, more thorough scrolling to trigger all images.
        await page.evaluate("""async () => {
            const delay = ms => new Promise(r => setTimeout(r, ms));
            const height = document.body.scrollHeight;
            // Scroll slowly in smaller increments to trigger IntersectionObserver
            for (let i = 0; i < height; i += 300) {
                window.scrollTo(0, i);
                await delay(200);
            }
            // Scroll to bottom and wait for any remaining images
            window.scrollTo(0, document.body.scrollHeight);
            await delay(1000);
            
            // Force trigger: for any img with data-src but no real src, copy data-src to src
            const lazyImgs = document.querySelectorAll('#js_content img[data-src]');
            for (const img of lazyImgs) {
                if (!img.src || img.src === '' || img.src.includes('data:image/') || img.src.endsWith('/0')) {
                    img.src = img.getAttribute('data-src');
                }
            }
            await delay(500);
            
            window.scrollTo(0, 0);
        }""")
        await page.wait_for_timeout(3000)
    else:
        await page.evaluate("""async () => {
            const delay = ms => new Promise(r => setTimeout(r, ms));
            const height = document.body.scrollHeight;
            for (let i = 0; i < height; i += 500) {
                window.scrollTo(0, i);
                await delay(100);
            }
            window.scrollTo(0, 0);
        }""")
        await page.wait_for_timeout(2000)


async def _extract_and_save(page, url: str, output_path: Path, images_dir: Path, is_wechat: bool = False, is_dedao: bool = False, is_webflow: bool = False) -> str:
    """Extract article content, download images, convert to Markdown, and save.
    
    This is the shared extraction logic used by both CDP mode and cookie-injection mode.
    Returns the path to the saved article.md.
    """
    # Take a screenshot for debugging
    try:
        await page.screenshot(path="/tmp/article_fetch_debug.png", full_page=False)
        print("📸 调试截图: /tmp/article_fetch_debug.png")
    except Exception:
        pass

    # Extract article content
    print("📝 正在提取文章内容...")
    article_data = await page.evaluate("""(args) => {
        const isWechat = args.isWechat;
        const isDedao = args.isDedao;
        const isWebflow = args.isWebflow;

        // Remove style/script tags first (Webflow embeds <style> inside content containers)
        if (isWebflow) {
            document.querySelectorAll('.u-rich-text-blog style, .u-rich-text-blog script, .w-richtext style, .w-richtext script').forEach(el => el.remove());
        }

        // Site-specific selectors (priority order)
        const selectors = isWechat
            ? ['#js_content', '.rich_media_content', 'article']
            : isDedao
                ? ['.iget-articles', 'article']
                : isWebflow
                    ? ['.u-rich-text-blog', '.w-richtext', 'article', 'main']
                    : [
                        '.available-content', '.post-content', 'article .body',
                        'article', '.entry-content', '[class*="body"]'
                    ];
        
        let articleEl = null;
        let maxLen = 0;
        for (const sel of selectors) {
            const el = document.querySelector(sel);
            if (el) {
                const len = el.innerText.length;
                if (len > maxLen) { maxLen = len; articleEl = el; }
            }
        }
        
        if (!articleEl) {
            return { title: document.title, subtitle: '', author: '', date: '', content: document.body.innerText, html: document.body.innerHTML };
        }

        // === 标题提取（多策略，优先级递减） ===
        let title = '';
        if (isWechat) {
            // WeChat: title is in #activity-name or h1.rich_media_title
            const wcTitleSelectors = ['#activity-name', 'h1.rich_media_title', 'h1'];
            for (const sel of wcTitleSelectors) {
                const el = document.querySelector(sel);
                if (el) {
                    const t = el.innerText.trim();
                    if (t && t.length > 1) { title = t; break; }
                }
            }
        }
        if (!title) {
            const titleSelectors = [
                'h1.post-title', 'h1[class*="post-title"]', 'h1[class*="post"]',
                'article h1', '.pencraft h1',
                '[class*="title"] h1', '[class*="header"] h1',
                'h1'
            ];
            for (const sel of titleSelectors) {
                const els = document.querySelectorAll(sel);
                for (const el of els) {
                    const t = el.innerText.trim();
                    if (t && t.length > 3) { title = t; break; }
                }
                if (title) break;
            }
        }
        // 回退到 meta 标签
        if (!title) {
            const ogTitle = document.querySelector('meta[property="og:title"]');
            if (ogTitle) title = ogTitle.getAttribute('content') || '';
        }
        if (!title) {
            const metaTitle = document.querySelector('meta[name="title"]');
            if (metaTitle) title = metaTitle.getAttribute('content') || '';
        }
        if (!title) title = document.title;
        // 清理标题：去掉网站后缀（如 " - Cursor" " | Substack"）
        title = title.replace(/\\s*[-|–—]\\s*(Cursor|Substack|Medium|LinkedIn|Notion|Ghost).*$/i, '').trim();

        const subtitleEl = document.querySelector('h3.subtitle, .subtitle, [class*="subtitle"]');
        const subtitle = subtitleEl ? subtitleEl.innerText.trim() : '';

        // === 作者提取（增强选择器） ===
        let author = '';
        if (isWechat) {
            // WeChat: author/account name is in #js_name or .rich_media_meta_nickname
            const wcAuthorSelectors = ['#js_name', 'a#js_name', '.rich_media_meta_nickname .rich_media_meta_text'];
            for (const sel of wcAuthorSelectors) {
                const el = document.querySelector(sel);
                if (el) {
                    const t = el.innerText.trim();
                    if (t && t.length > 0) { author = t; break; }
                }
            }
        }
        if (!author) {
            const authorSelectors = [
                '.author-name', '.byline a', '[data-testid="author-name"]',
                'a[class*="author"]', '.pencraft a[href*="@"]',
                'a[data-testid="post-ufi-author-link"]',
                '[rel="author"]', '.author', 'meta[name="author"]'
            ];
            for (const sel of authorSelectors) {
                const el = document.querySelector(sel);
                if (el) {
                    // meta 标签取 content 属性
                    const t = (el.tagName === 'META' ? el.getAttribute('content') : el.innerText || '').trim();
                    if (t && t.length > 1) { author = t; break; }
                }
            }
        }
        // 回退到 og:article:author
        if (!author) {
            const ogAuthor = document.querySelector('meta[property="article:author"], meta[property="og:article:author"]');
            if (ogAuthor) author = ogAuthor.getAttribute('content') || '';
        }

        // === 日期提取 ===
        let date = '';
        if (isWechat) {
            // WeChat: publish time is in #publish_time
            const wcDateEl = document.querySelector('#publish_time');
            if (wcDateEl) date = wcDateEl.innerText.trim();
        }
        if (!date) {
            const dateEl = document.querySelector('time, .post-date, [class*="date"]');
            date = dateEl ? (dateEl.getAttribute('datetime') || dateEl.innerText.trim()) : '';
        }

        return { 
            title, subtitle, author, date, 
            content: articleEl.innerText, 
            html: articleEl.innerHTML 
        };
    }""", {"isWechat": is_wechat, "isDedao": is_dedao, "isWebflow": is_webflow})

    title = article_data.get("title", "Untitled")
    print(f"📖 文章标题: {title}")
    print(f"📏 正文长度: {len(article_data.get('content', ''))} 字符")

    # Extract and download images
    print("🖼️  正在下载图片...")
    image_elements = await page.evaluate("""(args) => {
        const isWechat = args.isWechat;
        const isDedao = args.isDedao;
        let articleEl = null;
        if (isWechat) {
            // WeChat: use #js_content directly
            articleEl = document.querySelector('#js_content') || document.querySelector('.rich_media_content');
        }
        if (!articleEl) {
            // X.com / Twitter 帖子内容选择器
            const xSelectors = ['[data-testid="tweetText"]', '.tweet-text', '[aria-label="Tweet text"]'];
            for (const sel of xSelectors) {
                const el = document.querySelector(sel);
                if (el && el.innerText.length > 0) {
                    articleEl = el;
                    break;
                }
            }
        }
        if (!articleEl) {
            const selectors = ['.iget-articles', '.available-content', '.post-content', 'article .body', 'article'];
            let maxLen = 0;
            for (const sel of selectors) {
                const el = document.querySelector(sel);
                if (el) {
                    const len = el.innerText.length;
                    if (len > maxLen) { maxLen = len; articleEl = el; }
                }
            }
        }
        if (!articleEl) articleEl = document.body;
        
        // X.com / Twitter: need to extract images from the whole page (not just article area)
        const isXcom = window.location.href.includes('x.com') || window.location.href.includes('twitter.com');
        
        let imgs;
        if (isXcom) {
            // For X.com, get images from the tweet container and the whole page (for embedded media)
            const tweetEl = document.querySelector('[data-testid="tweet"]') || document.querySelector('article');
            if (tweetEl) {
                imgs = tweetEl.querySelectorAll('img');
            }
            // Also get images from the main timeline area for embedded media
            if (!imgs || imgs.length === 0) {
                const timelineImgs = document.querySelectorAll('[data-testid="tweetPhoto"], [data-testid="cardEntity"] img, [data-testid="previewPhoto"] img');
                imgs = timelineImgs;
            }
        } else {
            imgs = articleEl.querySelectorAll('img');
        }
        
        return Array.from(imgs).map((img, i) => ({
            // For WeChat, prefer data-src (original high-res URL) over src (which may be a placeholder)
            src: (isWechat ? (img.getAttribute('data-src') || img.src) : (img.src || img.getAttribute('data-src'))) || '',  // isWechat from closure
            alt: img.alt || '',
            width: img.naturalWidth || img.width || 0,
            height: img.naturalHeight || img.height || 0,
            index: i
        })).filter(x => {
            if (!x.src || x.src.startsWith('data:image/svg')) return false;
            if (x.src.includes('pixel') || x.src.includes('tracking')) return false;
            // For X.com, include larger images (not just avatars/profile pics)
            if (isXcom) {
                // Include images larger than 100x100 (filter out small avatars)
                if (x.width > 0 && x.width < 100 && x.height > 0 && x.height < 100) return false;
            } else {
                // Original filter for other sites
                if (x.width > 0 && x.width < 50 && x.height > 0 && x.height < 50) return false;
            }
            return true;
        });
    }""", {"isWechat": is_wechat, "isDedao": is_dedao, "isWebflow": is_webflow})

    image_map = {}
    for i, img_info in enumerate(image_elements):
        src = img_info["src"]
        if not src or src.startswith("data:"):
            continue

        ext = ".png"
        parsed_img = urllib.parse.urlparse(src)
        path_ext = Path(parsed_img.path).suffix.lower()
        if path_ext in (".jpg", ".jpeg", ".png", ".gif", ".webp"):
            ext = path_ext
        else:
            # WeChat images use ?wx_fmt=png/jpeg/gif format
            query_params = urllib.parse.parse_qs(parsed_img.query)
            wx_fmt = query_params.get("wx_fmt", query_params.get("tp", [None]))[0]
            if wx_fmt:
                wx_fmt = wx_fmt.lower()
                fmt_map = {"png": ".png", "jpeg": ".jpeg", "jpg": ".jpg", "gif": ".gif", "webp": ".webp"}
                ext = fmt_map.get(wx_fmt, ".png")

        url_hash = hashlib.md5(src.encode()).hexdigest()[:8]
        filename = f"img_{i+1:02d}_{url_hash}{ext}"
        local_path = images_dir / filename

        try:
            response = await page.request.get(src)
            if response.ok:
                content_bytes = await response.body()
                if len(content_bytes) > 500:
                    local_path.write_bytes(content_bytes)
                    # Auto-convert WebP/SVG to PNG for compatibility
                    converted = _convert_image_format(local_path)
                    fmt_note = " (→PNG)" if converted else ""
                    image_map[src] = f"images/{filename}"
                    print(f"  ✅ 图片 {i+1}/{len(image_elements)}: {filename} ({len(content_bytes)//1024}KB){fmt_note}")
        except Exception as e:
            print(f"  ⚠️  图片下载异常: {str(e)[:60]}")

    # Convert HTML to Markdown
    print("📝 正在转换为 Markdown...")
    markdown = await page.evaluate("""(args) => {
        const imageMap = args.imageMap;
        const extractedTitle = args.title;
        const isWechat = args.isWechat;
        const isDedao = args.isDedao;
        const isWebflow = args.isWebflow;
        
        let articleEl = null;
        if (isWechat) {
            articleEl = document.querySelector('#js_content') || document.querySelector('.rich_media_content');
        }
        if (isWebflow && !articleEl) {
            articleEl = document.querySelector('.u-rich-text-blog') || document.querySelector('.w-richtext');
        }
        if (!articleEl) {
            const selectors = ['.iget-articles', '.available-content', '.post-content', 'article .body', 'article'];
            let maxLen = 0;
            for (const sel of selectors) {
                const el = document.querySelector(sel);
                if (el) {
                    const len = el.innerText.length;
                    if (len > maxLen) { maxLen = len; articleEl = el; }
                }
            }
        }
        if (!articleEl) return '';

        let skippedFirstH1 = false;

        function processNode(node, listDepth) {
            if (node.nodeType === Node.TEXT_NODE) {
                return node.textContent || '';
            }
            if (node.nodeType !== Node.ELEMENT_NODE) return '';

            const tag = node.tagName.toLowerCase();
            
            if (['button', 'form', 'nav', 'footer', 'script', 'style', 'noscript'].includes(tag)) return '';
            if (node.style && node.style.display === 'none') return '';
            
            if (node.className && typeof node.className === 'string' && (
                node.className.includes('subscription') || 
                node.className.includes('paywall') ||
                node.className.includes('footer')
            )) return '';

            const children = () => {
                let s = '';
                for (const c of node.childNodes) s += processNode(c, listDepth);
                return s;
            };

            switch (tag) {
                case 'h1': {
                    // 跳过正文中与已提取标题重复的第一个 h1
                    const h1Text = node.innerText.trim();
                    if (!skippedFirstH1 && extractedTitle && h1Text === extractedTitle) {
                        skippedFirstH1 = true;
                        return '';
                    }
                    return '\\n# ' + h1Text + '\\n\\n';
                }
                case 'h2': return '\\n## ' + node.innerText.trim() + '\\n\\n';
                case 'h3': return '\\n### ' + node.innerText.trim() + '\\n\\n';
                case 'h4': return '\\n#### ' + node.innerText.trim() + '\\n\\n';
                case 'h5': return '\\n##### ' + node.innerText.trim() + '\\n\\n';
                case 'p': {
                    const t = children().trim();
                    return t ? t + '\\n\\n' : '';
                }
                case 'blockquote': {
                    const lines = children().trim().split('\\n').filter(l => l.trim());
                    return lines.map(l => '> ' + l.trim()).join('\\n') + '\\n\\n';
                }
                case 'ul': {
                    let s = '';
                    for (const li of node.querySelectorAll(':scope > li')) {
                        const indent = '  '.repeat(listDepth);
                        s += indent + '- ' + processNode(li, listDepth + 1).trim() + '\\n';
                    }
                    return s + '\\n';
                }
                case 'ol': {
                    let s = '', idx = 1;
                    for (const li of node.querySelectorAll(':scope > li')) {
                        const indent = '  '.repeat(listDepth);
                        s += indent + idx + '. ' + processNode(li, listDepth + 1).trim() + '\\n';
                        idx++;
                    }
                    return s + '\\n';
                }
                case 'strong': case 'b':
                    return '**' + (node.innerText || '') + '**';
                case 'em': case 'i':
                    return '*' + (node.innerText || '') + '*';
                case 'code':
                    return '`' + (node.innerText || '') + '`';
                case 'pre': {
                    const code = node.querySelector('code');
                    const text = code ? code.innerText : node.innerText;
                    return '\\n```\\n' + text + '\\n```\\n\\n';
                }
                case 'a': {
                    const href = node.getAttribute('href') || '';
                    const text = node.innerText.trim();
                    if (text && href && !href.startsWith('javascript:')) {
                        return '[' + text + '](' + href + ')';
                    }
                    return text;
                }
                case 'img': {
                    const src = node.src || node.getAttribute('data-src') || '';
                    const dataSrc = node.getAttribute('data-src') || '';
                    const alt = node.alt || '';
                    if (!src || src.includes('data:image/svg')) return '';
                    // Try matching imageMap with both src and data-src (WeChat uses data-src as key)
                    const localPath = imageMap[src] || imageMap[dataSrc] || src;
                    return '\\n![' + alt + '](' + localPath + ')\\n\\n';
                }
                case 'figure': {
                    const img = node.querySelector('img');
                    const caption = node.querySelector('figcaption');
                    if (img) {
                        const src = img.src || img.getAttribute('data-src') || '';
                        const alt = img.alt || (caption ? caption.innerText.trim() : '');
                        if (!src || src.includes('data:image/svg')) return '';
                        const localPath = imageMap[src] || src;
                        let s = '\\n![' + alt + '](' + localPath + ')\\n';
                        if (caption) s += '*' + caption.innerText.trim() + '*\\n';
                        return s + '\\n';
                    }
                    return children();
                }
                case 'br': return '\\n';
                case 'hr': return '\\n---\\n\\n';
                case 'table': {
                    const rows = node.querySelectorAll('tr');
                    let s = '\\n';
                    rows.forEach((row, ri) => {
                        const cells = row.querySelectorAll('td, th');
                        const texts = Array.from(cells).map(c => c.innerText.trim().replace(/\\n/g, ' '));
                        s += '| ' + texts.join(' | ') + ' |\\n';
                        if (ri === 0) s += '| ' + texts.map(() => '---').join(' | ') + ' |\\n';
                    });
                    return s + '\\n';
                }
                default:
                    return children();
            }
        }

        return processNode(articleEl, 0);
    }""", {"imageMap": image_map, "title": title, "isWechat": is_wechat, "isWebflow": is_webflow})

    # Build final document
    import datetime as _dt
    md_content = f"# {title}\n\n"
    if article_data.get("subtitle"):
        md_content += f"*{article_data['subtitle']}*\n\n"
    meta_parts = []
    if article_data.get("author"):
        meta_parts.append(f"作者: {article_data['author']}")
    if article_data.get("date"):
        meta_parts.append(f"日期: {article_data['date']}")
    if meta_parts:
        md_content += f"> {' | '.join(meta_parts)}\n\n"
    md_content += f"> 原文链接: {url}\n\n---\n\n"
    md_content += markdown
    md_content = re.sub(r"\n{4,}", "\n\n\n", md_content)

    md_path = output_path / "article.md"
    md_path.write_text(md_content, encoding="utf-8")

    article_meta = {
        "url": url,
        "title": title,
        "subtitle": article_data.get("subtitle", ""),
        "author": article_data.get("author", ""),
        "date": article_data.get("date", ""),
        "content_length": len(article_data.get("content", "")),
        "image_count": len(image_map),
        "images": list(image_map.values()),
        "fetched_at": _dt.datetime.now().isoformat(),
    }
    meta_path = output_path / "article_meta.json"
    meta_path.write_text(json.dumps(article_meta, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"📋 元信息已保存: {meta_path}")

    print(f"\n✅ 文章已保存: {md_path}")
    print(f"   标题: {title}")
    print(f"   正文: {len(article_data.get('content', ''))} 字符")
    print(f"   图片: {len(image_map)} 张")

    return str(md_path)


async def fetch_article(
    url: str,
    output_dir: str,
    headless: bool = True,
    use_cdp: bool = False,
):
    """Fetch article content and images.
    
    Two modes:
    - CDP mode (use_cdp=True): Connects to real Chrome via CDP port 9222,
      bypassing Cloudflare and Google anti-automation detection.
      Best for OpenAI, LinkedIn, Google-auth sites.
    - Cookie injection mode (default): Reads Chrome cookies and injects into Playwright.
    
    Cloudflare-protected sites (openai.com, etc.) are automatically detected
    and will auto-upgrade to CDP mode with a warning.
    """
    from playwright.async_api import async_playwright

    output_path = Path(output_dir).resolve()
    output_path.mkdir(parents=True, exist_ok=True)
    images_dir = output_path / "images"
    images_dir.mkdir(exist_ok=True)

    # Parse the URL domain
    parsed = urllib.parse.urlparse(url)
    domain = parsed.hostname
    base_domain = ".".join(domain.split(".")[-2:])
    is_substack = _is_substack_site(url)
    is_wechat = _is_wechat_article(url)
    is_dedao = _is_dedao_article(url)
    is_webflow = _is_webflow_blog(url)

    # Auto-upgrade to CDP mode for Cloudflare-protected sites
    if not use_cdp and _is_cloudflare_likely(url):
        print(f"🛡️  {domain} 使用 Cloudflare 保护，自动切换到 CDP 模式")
        use_cdp = True

    # Auto-upgrade to CDP mode for Substack sites (avoid automation detection)
    if not use_cdp and is_substack:
        print(f"📰 检测到 Substack 站点，自动切换到 CDP 模式（避免自动化检测）")
        use_cdp = True

    pw_manager = None

    # ══════════════════════════════════════════════════════════════════
    # CDP mode: connect to real Chrome browser
    # ══════════════════════════════════════════════════════════════════
    if use_cdp:
        print("🔗 使用 CDP 模式连接真实 Chrome...")
        async with async_playwright() as p:
            browser, context, page = await _create_cdp_context(p)

            # Try to find existing tab with the target URL/domain, avoid re-navigation
            target_page = None
            target_url_lower = url.lower()
            for ctx in browser.contexts:
                for p2 in ctx.pages:
                    page_url = p2.url or ""
                    if target_url_lower in page_url.lower() or "dedao.cn" in page_url.lower():
                        target_page = p2
                        print(f"📄 复用已打开的标签页: {page_url[:80]}")
                        break
                if target_page:
                    break

            if target_page:
                page = target_page
            else:
                print(f"📥 正在加载页面: {url}")
                try:
                    await page.goto(url, wait_until="networkidle", timeout=60000)
                except Exception as e:
                    print(f"⚠️  页面加载超时，继续: {e}")
                    await page.wait_for_timeout(5000)

            # Wait for Cloudflare challenge if detected
            await _wait_for_cloudflare(page)

            await page.wait_for_timeout(3000)

            # === Substack login check in CDP mode ===
            if is_substack:
                print("🔍 Substack 登录态校验...")
                login_status = await _check_substack_login(page)
                print(f"   {login_status['detail']}")

                if not login_status["logged_in"]:
                    print("\n" + "=" * 60)
                    print("🔐 Substack 未登录！请在 Chrome 浏览器中完成以下操作：")
                    print(f"   1. 在 Chrome 中打开: {url}")
                    print("   2. 点击右上角 'Sign in' 登录你的 Substack 账号")
                    print("   3. 确认登录成功（右上角显示头像）")
                    print("   4. 回到终端输入 'y' 继续")
                    print("=" * 60)

                    max_attempts = 5
                    for attempt in range(max_attempts):
                        try:
                            user_input = await asyncio.get_event_loop().run_in_executor(
                                None, lambda: input("\n⏳ 登录完成后输入 'y' 继续（'q' 取消）: ")
                            )
                        except (EOFError, KeyboardInterrupt):
                            print("\n⚠️  stdin 不可用，等待 30 秒后自动检测...")
                            await page.wait_for_timeout(30000)
                            user_input = "y"

                        if user_input.strip().lower() == "q":
                            print("⚠️  跳过登录，将抓取当前可见内容")
                            break

                        if user_input.strip().lower() == "y":
                            print("🔄 重新加载页面并验证...")
                            try:
                                await page.goto(url, wait_until="networkidle", timeout=60000)
                            except Exception:
                                await page.wait_for_timeout(5000)
                            await page.wait_for_timeout(3000)

                            login_status = await _check_substack_login(page)
                            print(f"   {login_status['detail']}")
                            if login_status["logged_in"]:
                                print("✅ 登录验证通过！")
                                break
                            else:
                                remaining = max_attempts - attempt - 1
                                if remaining > 0:
                                    print(f"⚠️  验证未通过（还有 {remaining} 次机会）")
                                else:
                                    print("⚠️  多次验证未通过，将抓取当前可见内容")
                else:
                    # Logged in — check if paywall still blocks full content
                    if login_status["has_paywall"]:
                        print("⚠️  已登录但仍检测到付费墙（可能需要付费订阅此频道）")

            # Scroll to load lazy content
            await _scroll_page(page, is_wechat=is_wechat, is_dedao=is_dedao)

            # Extract content
            result = await _extract_and_save(page, url, output_path, images_dir, is_wechat=is_wechat, is_dedao=is_dedao, is_webflow=is_webflow)

            # Close the tab we opened (don't close the browser — it's the user's Chrome)
            await page.close()
            return result

    # ══════════════════════════════════════════════════════════════════
    # Cookie injection mode (original behavior)
    # ══════════════════════════════════════════════════════════════════

    # Extract cookies from Chrome for relevant domains
    all_cookies = []
    has_substack_storage = is_substack and SUBSTACK_STORAGE_PATH.exists()
    
    if has_substack_storage:
        print(f"💾 检测到 Substack 登录态缓存: {SUBSTACK_STORAGE_PATH}")
    else:
        cookie_domains = [base_domain]
        if is_substack:
            cookie_domains.append("substack.com")
        for d in cookie_domains:
            cookies = get_chrome_cookies_for_domain(d)
            all_cookies.extend(cookies)

    no_cookies = not all_cookies and not has_substack_storage
    if no_cookies and not is_substack and not is_wechat:
        print("⚠️  未找到 Chrome cookies，将打开浏览器窗口供手动登录")
        headless = False

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=headless)
        
        context_kwargs = {
            "viewport": {"width": 1280, "height": 900},
            "user_agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/131.0.0.0 Safari/537.36"
            ),
        }
        if has_substack_storage:
            context_kwargs["storage_state"] = str(SUBSTACK_STORAGE_PATH)
        
        context = await browser.new_context(**context_kwargs)

        if all_cookies and not has_substack_storage:
            print(f"🍪 注入 {len(all_cookies)} 个 cookies...")
            for cookie in all_cookies:
                try:
                    cookie_data = {
                        "name": cookie["name"],
                        "value": cookie["value"],
                        "path": cookie.get("path", "/"),
                        "secure": cookie.get("secure", False),
                        "httpOnly": cookie.get("httpOnly", False),
                        "sameSite": cookie.get("sameSite", "None"),
                    }
                    cookie_domain = cookie.get("domain", "")
                    if cookie_domain.startswith("."):
                        cookie_data["domain"] = cookie_domain
                    else:
                        cookie_data["url"] = f"https://{cookie_domain}"
                    if cookie.get("expires", -1) > 0:
                        cookie_data["expires"] = cookie["expires"]
                    await context.add_cookies([cookie_data])
                except Exception:
                    pass

        page = await context.new_page()

        print("📥 正在加载页面...")
        try:
            await page.goto(url, wait_until="networkidle", timeout=60000)
        except Exception as e:
            print(f"⚠️  页面加载超时，继续尝试: {e}")
            await page.wait_for_timeout(5000)

        # Wait for Cloudflare challenge if detected
        await _wait_for_cloudflare(page)

        # === WeChat article: no login needed, just wait for content ===
        if is_wechat:
            print("🔍 检测到微信公众号文章，无需登录，等待内容加载...")
            await page.wait_for_timeout(3000)
        # === Substack-specific login detection ===
        elif is_substack:
            print("🔍 检测到 Substack 站点，正在检查登录状态...")
            await page.wait_for_timeout(2000)
            login_status = await _check_substack_login(page)
            print(f"   {login_status['detail']}")
            
            if not login_status["logged_in"]:
                if has_substack_storage:
                    print("⚠️  缓存的登录态已过期，需要重新登录")
                    SUBSTACK_STORAGE_PATH.unlink(missing_ok=True)
                browser_new, context, page, pw_manager = await _guide_substack_login(
                    page, browser, context, url
                )
                browser = browser_new
            else:
                if has_substack_storage:
                    await context.storage_state(path=str(SUBSTACK_STORAGE_PATH))
                    print("💾 登录态缓存已刷新")
        
        # === Generic (non-Substack, non-WeChat) login fallback ===
        elif no_cookies and not is_wechat:
            print("\n" + "=" * 60)
            print("🔐 请在浏览器中完成以下操作：")
            print("   1. 登录你的账号（确保有该文章的阅读权限）")
            print("   2. 确认页面已显示完整文章内容（无付费墙）")
            print("   3. 回到终端，按回车键继续抓取")
            print("=" * 60)
            
            try:
                await asyncio.get_event_loop().run_in_executor(
                    None, lambda: input("\n⏳ 登录完成后按 回车键 继续...")
                )
            except (EOFError, KeyboardInterrupt):
                print("\n⚠️  stdin 不可用，等待 15 秒后继续...")
                await page.wait_for_timeout(15000)
            
            print("\n🔄 收到确认信号，正在重新加载页面...")
            try:
                await page.goto(url, wait_until="networkidle", timeout=60000)
            except Exception as e:
                print(f"⚠️  页面重新加载超时，继续尝试: {e}")
                await page.wait_for_timeout(5000)
            
            await page.wait_for_timeout(3000)
            
            paywall_status = await page.evaluate("""() => {
                const paywallEl = document.querySelector('[data-testid="paywall"], .paywall');
                const body = document.body.innerText;
                const hasPaywall = !!paywallEl ||
                                  body.includes('This post is for paid subscribers') ||
                                  body.includes('Subscribe to read');
                const contentEl = document.querySelector('article') || document.querySelector('.available-content');
                const contentLength = contentEl ? contentEl.innerText.length : 0;
                return { hasPaywall, contentLength };
            }""")
            
            if paywall_status["hasPaywall"]:
                print(f"⚠️  仍检测到付费墙（内容 {paywall_status['contentLength']} 字符），将提取当前可见内容")
            else:
                print(f"✅ 未检测到付费墙，内容 {paywall_status['contentLength']} 字符，继续抓取...")

        await page.wait_for_timeout(3000)

        # Scroll to load lazy content
        await _scroll_page(page, is_wechat=is_wechat, is_dedao=is_dedao)

        # Check if paywall is still blocking
        paywall_check = await page.evaluate("""() => {
            const body = document.body.innerText;
            const paywallEl = document.querySelector('[data-testid="paywall"], .paywall');
            const hasPaywall = !!paywallEl ||
                              body.includes('Subscribe to read') || 
                              body.includes('This post is for paying subscribers') ||
                              body.includes('This post is for paid subscribers') ||
                              body.includes('Upgrade to paid');
            const contentLength = document.querySelector('.available-content, article, .post-content, .body')?.innerText?.length || 0;
            return { hasPaywall, contentLength };
        }""")

        print(f"📊 内容长度: {paywall_check['contentLength']} 字符, 付费墙: {paywall_check['hasPaywall']}")

        if paywall_check["hasPaywall"] and paywall_check["contentLength"] < 2000:
            print("⚠️  仍被付费墙拦截，但会继续提取可见内容")

        # Extract content and save
        result = await _extract_and_save(page, url, output_path, images_dir, is_wechat=is_wechat, is_dedao=is_dedao, is_webflow=is_webflow)

        await browser.close()
        if pw_manager:
            await pw_manager.stop()
        return result


async def substack_login():
    """Standalone Substack login — opens browser, guides login, saves session."""
    from playwright.async_api import async_playwright
    
    print("🔐 Substack 登录")
    print("=" * 60)
    
    if SUBSTACK_STORAGE_PATH.exists():
        print(f"💾 发现已有登录态缓存: {SUBSTACK_STORAGE_PATH}")
        print("   正在验证缓存是否有效...")
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                storage_state=str(SUBSTACK_STORAGE_PATH),
                viewport={"width": 1280, "height": 900},
                user_agent=(
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/131.0.0.0 Safari/537.36"
                ),
            )
            page = await context.new_page()
            try:
                await page.goto("https://substack.com", wait_until="networkidle", timeout=30000)
            except Exception:
                await page.wait_for_timeout(5000)
            await page.wait_for_timeout(2000)
            login_status = await _check_substack_login(page)
            await browser.close()
            
            if login_status["logged_in"]:
                print(f"   ✅ 缓存有效，已登录！无需重新登录。")
                return
            else:
                print(f"   ⚠️  缓存已过期，需要重新登录")
                SUBSTACK_STORAGE_PATH.unlink(missing_ok=True)
    
    print("\n即将打开浏览器，请完成 Substack 登录：")
    print("  1. 点击 'Sign in' 登录您的账号")
    print("  2. 登录成功后页面右上角应显示您的头像")
    print("  3. 回到终端输入 'y' 确认")
    print("=" * 60)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(
            viewport={"width": 1280, "height": 900},
            user_agent=(
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/131.0.0.0 Safari/537.36"
            ),
        )
        page = await context.new_page()
        await page.goto("https://substack.com/sign-in", wait_until="networkidle", timeout=60000)
        
        for attempt in range(5):
            try:
                user_input = await asyncio.get_event_loop().run_in_executor(
                    None, lambda: input("\n⏳ 登录完成后请输入 'y' 确认: ")
                )
            except (EOFError, KeyboardInterrupt):
                break
            
            if user_input.strip().lower() == "y":
                # Navigate to a Substack page to verify login
                try:
                    await page.goto("https://substack.com", wait_until="networkidle", timeout=30000)
                except Exception:
                    await page.wait_for_timeout(5000)
                await page.wait_for_timeout(2000)
                
                login_status = await _check_substack_login(page)
                print(f"   {login_status['detail']}")
                
                if login_status["logged_in"]:
                    SUBSTACK_STORAGE_DIR.mkdir(parents=True, exist_ok=True)
                    await context.storage_state(path=str(SUBSTACK_STORAGE_PATH))
                    print(f"💾 登录态已缓存到 {SUBSTACK_STORAGE_PATH}")
                    print("✅ 后续抓取 Substack 文章时将自动使用此登录态，无需重复登录！")
                    await browser.close()
                    return
                else:
                    remaining = 4 - attempt
                    if remaining > 0:
                        print(f"⚠️  验证未通过，请确认已登录（还有 {remaining} 次机会）")
            elif user_input.strip().lower() == "q":
                break
        
        await browser.close()
        print("❌ 登录未完成")


def main():
    parser = argparse.ArgumentParser(description="使用 Chrome cookies 抓取付费文章")
    subparsers = parser.add_subparsers(dest="command")
    
    # Default: fetch article (also works without subcommand for backward compat)
    fetch_parser = subparsers.add_parser("fetch", help="抓取文章内容")
    fetch_parser.add_argument("url", help="文章 URL")
    fetch_parser.add_argument("--output-dir", "-o", required=True, help="输出目录")
    fetch_parser.add_argument("--headless", action="store_true", default=True, help="无头模式（默认）")
    fetch_parser.add_argument("--no-headless", action="store_true", help="显示浏览器窗口")
    fetch_parser.add_argument("--cdp", action="store_true", help="使用 CDP 模式连接真实 Chrome（适用于 Cloudflare 保护站点如 OpenAI、需要 Google 登录的站点如 LinkedIn）")
    
    # Login subcommand
    subparsers.add_parser("login", help="登录 Substack 并缓存登录态到 ~/.substack/storage_state.json")
    
    args, remaining = parser.parse_known_args()
    
    if args.command == "login":
        asyncio.run(substack_login())
    elif args.command == "fetch":
        headless = not args.no_headless
        result = asyncio.run(fetch_article(url=args.url, output_dir=args.output_dir, headless=headless, use_cdp=args.cdp))
        if result:
            print(f"\n🎉 完成!")
        else:
            print("\n❌ 抓取失败")
            sys.exit(1)
    else:
        # Backward compatibility: treat positional args as URL + --output-dir
        # Re-parse with the old interface
        compat_parser = argparse.ArgumentParser()
        compat_parser.add_argument("url", help="文章 URL")
        compat_parser.add_argument("--output-dir", "-o", required=True, help="输出目录")
        compat_parser.add_argument("--headless", action="store_true", default=True)
        compat_parser.add_argument("--no-headless", action="store_true")
        compat_args = compat_parser.parse_args()
        headless = not compat_args.no_headless
        result = asyncio.run(fetch_article(url=compat_args.url, output_dir=compat_args.output_dir, headless=headless))
        if result:
            print(f"\n🎉 完成!")
        else:
            print("\n❌ 抓取失败")
            sys.exit(1)


if __name__ == "__main__":
    main()
