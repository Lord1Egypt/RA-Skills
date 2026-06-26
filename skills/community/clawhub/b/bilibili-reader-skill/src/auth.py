"""B站登录 — Playwright 自动化浏览器登录"""

from pathlib import Path
from typing import Optional


def login_via_browser(save_to_env: bool = True) -> Optional[dict[str, str]]:
    """通过 Playwright 打开浏览器，用户扫码后自动提取 Cookie

    Args:
        save_to_env: 是否自动保存到 .env 文件

    Returns:
        成功返回 {"SESSDATA": "...", "bili_jct": "...", "buvid3": "..."}, 失败返回 None
    """
    print("=" * 50)
    print("B站登录")
    print("=" * 50)

    # 检查 playwright 是否安装
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("\n需要安装 playwright：")
        print("  pip install playwright")
        print("  playwright install chromium")
        return None

    print("\n正在打开浏览器...")
    print("请在浏览器中完成以下操作：")
    print("  1. 如果未登录 → 用B站APP扫码登录")
    print("  2. 如果已登录 → 程序会自动提取 Cookie")
    print()

    cookies = {}

    try:
        with sync_playwright() as p:
            # 启动浏览器（非无头模式，用户可以看到界面）
            browser = p.chromium.launch(headless=False)
            context = browser.new_context()
            page = context.new_page()

            # 访问 B站首页
            page.goto("https://www.bilibili.com", wait_until="domcontentloaded")

            # 等待用户登录（检测 SESSDATA cookie 出现）
            print("等待登录中...（请在浏览器中扫码或确认登录）")

            max_wait = 180  # 最多等 3 分钟
            waited = 0
            while waited < max_wait:
                # 获取当前 cookies
                all_cookies = context.cookies()
                cookie_dict = {c["name"]: c["value"] for c in all_cookies}

                has_sessdata = "SESSDATA" in cookie_dict
                has_jct = "bili_jct" in cookie_dict
                has_buvid = "buvid3" in cookie_dict

                if has_sessdata and has_jct:
                    # 找到了关键 cookie
                    cookies["SESSDATA"] = cookie_dict["SESSDATA"]
                    cookies["bili_jct"] = cookie_dict["bili_jct"]
                    cookies["buvid3"] = cookie_dict.get("buvid3", "")
                    break

                # 每 2 秒检查一次
                page.wait_for_timeout(2000)
                waited += 2

                # 如果页面跳转到了登录页，提示用户
                if "passport.bilibili.com" in page.url:
                    if waited == 2:  # 只打印一次
                        print("  检测到登录页面，请扫码登录...")

            browser.close()

    except Exception as e:
        print(f"\n浏览器操作出错: {e}")
        return None

    if not cookies.get("SESSDATA"):
        print("\n等待超时或未检测到登录状态")
        print("请确认已在浏览器中成功登录 B站")
        return None

    # 显示结果
    print(f"\n登录成功!")
    for k, v in cookies.items():
        print(f"  {k}: {v[:20]}...")

    if save_to_env:
        _save_to_env(cookies)
        print(f"\nCookie已保存到 .env 文件")

    return cookies


def _save_to_env(cookies: dict[str, str]):
    """将Cookie保存到 .env 文件"""
    env_path = Path(__file__).parent.parent / ".env"

    # 读取现有内容
    existing = {}
    if env_path.exists():
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if "=" in line and not line.startswith("#"):
                    key, _, value = line.partition("=")
                    existing[key.strip()] = value.strip()

    # 更新Cookie
    existing["BILIBILI_SESSDATA"] = cookies.get("SESSDATA", "")
    existing["BILIBILI_BILI_JCT"] = cookies.get("bili_jct", "")
    existing["BILIBILI_BUVID3"] = cookies.get("buvid3", "")

    # 写回
    with open(env_path, "w", encoding="utf-8") as f:
        for key, value in existing.items():
            f.write(f"{key}={value}\n")


if __name__ == "__main__":
    login_via_browser()
