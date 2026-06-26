"""
cookie_login.py — B 站扫码登录获取 Cookie

用法：
    python cookie_login.py [--output <cookie保存路径>]

功能：
    1. 生成 B 站官方登录二维码
    2. 在终端显示 ASCII 二维码（如安装了 qrcode 库）或打印登录链接
    3. 等待用户手机扫码确认
    4. 自动提取并保存 Cookie 到文件

依赖：
    pip install requests
    pip install qrcode  (可选，用于终端显示二维码)
"""

import argparse
import os
import sys
import time

try:
    import requests
except ImportError:
    print("❌ 缺少 requests 库，请运行: pip install requests", file=sys.stderr)
    sys.exit(1)

try:
    import qrcode
except ImportError:
    qrcode = None


def print_qr_in_terminal(url):
    """在终端打印 ASCII 二维码。"""
    if qrcode is None:
        print("\n⚠️  未安装 qrcode 库，无法显示终端二维码")
        print(f"   请手动打开链接完成扫码: {url}")
        print("   安装 qrcode 可获得更好体验: pip install qrcode")
        return

    qr = qrcode.QRCode(border=1)
    qr.add_data(url)
    qr.make(fit=True)
    print("\n请使用 B 站 App 扫码登录：\n")
    qr.print_ascii(invert=True)
    print()


def login_by_qrcode(output_file="cookie.txt", wait_seconds=180):
    """
    通过 B 站官方二维码接口登录，获取 Cookie。

    返回: (success: bool, cookie_path: str or None)
    """
    session = requests.Session()
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/131.0.0.0 Safari/537.36"
        ),
        "Referer": "https://passport.bilibili.com/login",
    }

    # 申请二维码
    print("\n正在申请登录二维码...")
    try:
        resp = session.get(
            "https://passport.bilibili.com/x/passport-login/web/qrcode/generate",
            headers=headers,
            timeout=15,
        ).json()
    except Exception as e:
        print(f"❌ 网络请求失败: {e}", file=sys.stderr)
        return False, None

    if resp.get("code") != 0:
        print(f"❌ 二维码生成失败: {resp}", file=sys.stderr)
        return False, None

    qr_url = resp["data"]["url"]
    qrcode_key = resp["data"]["qrcode_key"]

    # 显示二维码
    print_qr_in_terminal(qr_url)
    print(f"📱 扫码登录链接: {qr_url}")
    print("\n两种登录方式选一种：")
    print("  1️⃣  用 B 站 App 扫上方的二维码（推荐）")
    print("  2️⃣  或复制上方链接到浏览器手动登录")
    print("\n等待扫码/登录确认...")

    # 轮询登录状态
    poll_url = "https://passport.bilibili.com/x/passport-login/web/qrcode/poll"
    start_time = time.time()
    last_status = None

    while time.time() - start_time < wait_seconds:
        try:
            poll_resp = session.get(
                poll_url,
                params={"qrcode_key": qrcode_key},
                headers=headers,
                timeout=15,
            ).json()
        except Exception:
            time.sleep(2)
            continue

        if poll_resp.get("code") != 0:
            print(f"❌ 轮询失败: {poll_resp}", file=sys.stderr)
            return False, None

        status_code = poll_resp.get("data", {}).get("code")

        if status_code != last_status:
            if status_code == 86101:
                print("状态: 未扫码")
            elif status_code == 86090:
                print("状态: 已扫码，请在手机上确认")
            elif status_code == 86038:
                print("状态: 二维码已过期")
                return False, None
            last_status = status_code

        if status_code == 0:
            print("✅ 扫码登录成功，正在提取 Cookie...")
            # 访问确认 URL 以获取完整 cookie
            success_url = poll_resp.get("data", {}).get("url", "")
            if success_url:
                try:
                    session.get(success_url, headers=headers, timeout=15, allow_redirects=True)
                except Exception:
                    pass
            break

        time.sleep(2)
    else:
        print("❌ 等待超时，请重试", file=sys.stderr)
        return False, None

    # 提取并保存 Cookie
    sessdata = None
    bili_jct = None
    for cookie in session.cookies:
        if cookie.name == "SESSDATA" and not sessdata:
            sessdata = cookie.value
        elif cookie.name == "bili_jct" and not bili_jct:
            bili_jct = cookie.value

    if not sessdata or not bili_jct:
        print("❌ 未能提取必要的 Cookie（SESSDATA/bili_jct）", file=sys.stderr)
        print("   请重试并在扫码后确认授权", file=sys.stderr)
        return False, None

    # 保存到文件
    cookie_string = f"SESSDATA={sessdata}; bili_jct={bili_jct}"
    abs_path = os.path.abspath(output_file)
    with open(abs_path, "w", encoding="utf-8") as f:
        f.write(cookie_string)

    print(f"\n{'=' * 50}")
    print("✅ Cookie 获取成功！")
    print(f"{'=' * 50}")
    print(f"已保存到: {abs_path}")
    return True, abs_path


def main():
    parser = argparse.ArgumentParser(description="B 站扫码登录获取 Cookie")
    parser.add_argument(
        "--output", default="cookie.txt",
        help="Cookie 保存路径（默认: ./cookie.txt）"
    )
    args = parser.parse_args()

    print("=" * 50)
    print("B 站 Cookie 获取工具")
    print("=" * 50)
    print("\n步骤：")
    print("1. 打开手机 B 站 App")
    print("2. 扫描下方二维码")
    print("3. 在手机上确认登录")
    print("4. 脚本将自动检测并获取 Cookie")
    print("-" * 50)

    success, path = login_by_qrcode(output_file=args.output)
    if success:
        print("\n现在可以获取视频字幕了！")
    else:
        print("\n登录失败，请重试。")
        sys.exit(1)


if __name__ == "__main__":
    main()
