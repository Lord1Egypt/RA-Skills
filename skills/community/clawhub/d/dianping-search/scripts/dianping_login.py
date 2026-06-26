#!/usr/bin/env python3
"""Dianping session helper — manage auth cookies for dianping.com.

Usage:
    python3 dianping_login.py --set-cookies DPER DPLET  # Set cookies directly
    python3 dianping_login.py --status                  # Check login status
    python3 dianping_login.py --export                  # Export current cookies
    python3 dianping_login.py --search <keyword>        # Quick search test

Auth requires only two cookies: dper + dplet.
Config stored in ~/.dianping/cookies.json
Zero dependencies — uses curl for HTTP (pre-installed on macOS/Linux).
"""

import sys
import json
import re
import subprocess
from pathlib import Path

CONFIG_DIR = Path.home() / ".dianping"
COOKIES_FILE = CONFIG_DIR / "cookies.json"
HOME_URL = "https://www.dianping.com"
DOMAIN = ".dianping.com"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) "
      "AppleWebKit/605.1.15 (KHTML, like Gecko) "
      "Version/17.0 Safari/605.1.15")





def _parse_cookie_input(*args) -> tuple:
    """Parse flexible cookie input formats. Supports:
    - Two separate args: DPER_VALUE DPLET_VALUE
    - Key=value pairs: dper=xxx dplet=yyy
    - Semicolon string: "dper=xxx; dplet=yyy"
    - Single string with both: "dper=xxx;dplet=yyy"
    """
    text = " ".join(args).strip().strip('"').strip("'")

    # Try parsing as "key=value; key=value" string
    pairs = {}
    for part in text.replace(";", " ").split():
        part = part.strip()
        if "=" in part:
            k, v = part.split("=", 1)
            pairs[k.strip().lower()] = v.strip()

    if "dper" in pairs and "dplet" in pairs:
        return pairs["dper"], pairs["dplet"]

    # Fallback: treat as two positional values (dper first, dplet second)
    values = [a.strip().strip('"').strip("'") for a in args if a.strip()]
    # Strip "dper=" or "dplet=" prefixes if present
    cleaned = []
    for v in values:
        if v.lower().startswith("dper="):
            cleaned.append(v[5:])
        elif v.lower().startswith("dplet="):
            cleaned.append(v[6:])
        else:
            cleaned.append(v)

    if len(cleaned) >= 2:
        return cleaned[0], cleaned[1]

    raise ValueError(
        "无法解析 cookies。支持的格式:\n"
        '  --set-cookies DPER_VALUE DPLET_VALUE\n'
        '  --set-cookies "dper=xxx; dplet=yyy"\n'
        '  --set-cookies dper=xxx dplet=yyy'
    )


def _load_cookies() -> dict:
    """Load cookies as {name: value} dict from config file."""
    if COOKIES_FILE.exists():
        raw = json.loads(COOKIES_FILE.read_text())
        if isinstance(raw, list):
            return {c["name"]: c["value"] for c in raw}
        return raw
    return {}


def _save_cookies(dper: str, dplet: str):
    """Save cookies to config file."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    data = {"dper": dper, "dplet": dplet}
    COOKIES_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False))


class _CurlResult:
    """Minimal response object from curl."""
    def __init__(self, text, status_code, url):
        self.text = text
        self.status_code = status_code
        self.url = url


def _http_get(url: str, cookies: dict = None) -> _CurlResult:
    """Make an HTTP GET via curl with auth cookies."""
    if cookies is None:
        cookies = _load_cookies()
    cookie_str = "; ".join(f"{k}={v}" for k, v in cookies.items()) if cookies else ""
    cmd = [
        "curl", "-s", "-L", "-w", "\n%{http_code}\n%{url_effective}",
        "-b", cookie_str,
        "-H", f"User-Agent: {UA}",
        "-H", "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "-H", "Accept-Language: zh-CN,zh;q=0.9",
        "-H", "Referer: https://www.dianping.com/",
        "--max-time", "15",
        url,
    ]
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=20)
        lines = p.stdout.rsplit("\n", 2)
        if len(lines) >= 3:
            body, status, final_url = lines[-3], lines[-2].strip(), lines[-1].strip()
        else:
            body, status, final_url = p.stdout, "0", url
        return _CurlResult(body, int(status or 0), final_url)
    except Exception as e:
        return _CurlResult("", 0, url)


def set_cookies(*args):
    """Set auth cookies directly."""
    try:
        dper, dplet = _parse_cookie_input(*args)
    except ValueError as e:
        print(f"❌ {e}")
        return
    _save_cookies(dper, dplet)
    print(f"✅ Cookies 已保存到 {COOKIES_FILE}")
    print(f"   dper  = {dper[:20]}...({len(dper)} chars)")
    print(f"   dplet = {dplet}")


def check_status():
    """Check if saved cookies are valid (pure HTTP)."""
    cookies = _load_cookies()
    if not cookies or "dper" not in cookies:
        print("❌ 未找到 cookies，请先设置: --set-cookies DPER DPLET")
        return False

    print("🔍 正在检查登录状态...")
    r = _http_get(HOME_URL, cookies)
    logged_in = (
        r.status_code == 200
        and "login" not in r.url
        and "account" not in r.url
    )
    if logged_in:
        # Extract page title
        m = re.search(r"<title>(.*?)</title>", r.text)
        title = m.group(1) if m else "大众点评"
        print(f"✅ 已登录 — {title}")
    else:
        print("❌ session 已过期，请更新 cookies: --set-cookies DPER DPLET")
    return logged_in


def export_cookies():
    """Print current saved cookies."""
    cookies = _load_cookies()
    if not cookies:
        print("❌ 未找到 cookies")
        return
    for k, v in cookies.items():
        print(f"{k}={v}")


def renew():
    """Guide user to renew expired cookies via system browser."""
    import webbrowser

    print("🔑 Cookie 续期指引")
    print("=" * 50)
    print()
    print("步骤 1: 正在用系统浏览器打开大众点评登录页...")
    webbrowser.open("https://account.dianping.com/pclogin")
    print()
    print("步骤 2: 请在浏览器中扫码或手机验证码登录")
    print()
    print("步骤 3: 登录成功后，按 F12 打开开发者工具")
    print("        → Application (应用) → Cookies → .dianping.com")
    print("        → 找到 dper 和 dplet 两行，复制它们的值")
    print()
    print("步骤 4: 粘贴到下面（格式: dper=xxx; dplet=yyy）")
    print("        或直接按回车取消:")
    print()
    user_input = input("  > ").strip()
    if not user_input:
        print("已取消")
        return
    try:
        dper, dplet = _parse_cookie_input(user_input)
        _save_cookies(dper, dplet)
        print(f"\n✅ Cookies 已更新！")
        print(f"   dper  = {dper[:20]}...({len(dper)} chars)")
        print(f"   dplet = {dplet}")
        # Verify
        check_status()
    except ValueError as e:
        print(f"❌ {e}")


def search(keyword: str, city_id: int = 2):
    """Quick search test via pure HTTP."""
    cookies = _load_cookies()
    if not cookies or "dper" not in cookies:
        print("❌ 未找到 cookies，请先设置")
        return

    from urllib.parse import quote
    url = f"https://www.dianping.com/search/keyword/{city_id}/0_{quote(keyword)}"
    r = _http_get(url, cookies)

    if r.status_code != 200 or "login" in r.url:
        print(f"❌ 请求失败 (status={r.status_code}, url={r.url})")
        return

    # Extract shop names from HTML
    shops = re.findall(r'class="tit"[^>]*>[\s\S]*?<h4>(.*?)</h4>', r.text)
    if not shops:
        shops = re.findall(r'<h4>(.*?)</h4>', r.text)
    # Clean HTML tags
    shops = [re.sub(r'<[^>]+>', '', s).strip() for s in shops]

    print(f"🔍 搜索「{keyword}」找到 {len(shops)} 家店:")
    for i, name in enumerate(shops[:10], 1):
        print(f"  {i}. {name}")


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        print(f"用法: python3 {sys.argv[0]} <command>")
        print("  --set-cookies DPER DPLET   设置登录 cookies")
        print("  --renew                    续期/重新获取 cookies（打开浏览器引导）")
        print("  --status                   检查登录状态")
        print("  --export                   导出当前 cookies")
        print("  --search <关键词>          快速搜索测试")
    elif args[0] == "--set-cookies" and len(args) >= 2:
        set_cookies(*args[1:])
    elif args[0] == "--renew":
        renew()
    elif args[0] == "--status":
        check_status()
    elif args[0] == "--export":
        export_cookies()
    elif args[0] == "--search" and len(args) >= 2:
        search(args[1], int(args[2]) if len(args) > 2 else 2)
    else:
        print(f"用法: python3 {sys.argv[0]} [--set-cookies | --renew | --status | --export | --search]")

