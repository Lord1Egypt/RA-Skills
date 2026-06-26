#!/usr/bin/env python3
"""
B站扫码登录工具（bilibili-api-python v17+）
登录成功后保存 cookie 到本地文件
"""

import asyncio
import argparse
import json
import sys
import time
from pathlib import Path

from bilibili_api import Credential
from bilibili_api.login_v2 import QrCodeLogin, QrCodeLoginEvents

COOKIE_PATH = Path.home() / ".openclaw/workspace/.bilibili_cookies.json"


async def check_cookie():
    """检查现有 cookie 是否有效"""
    if not COOKIE_PATH.exists():
        print("[INFO] 未找到 cookie 文件")
        return False

    try:
        data = json.loads(COOKIE_PATH.read_text())
        cred = Credential(
            sessdata=data.get("sessdata", ""),
            bili_jct=data.get("bili_jct", ""),
            buvid3=data.get("buvid3", ""),
            dedeuserid=data.get("dedeuserid", ""),
            ac_time_value=data.get("ac_time_value", ""),
        )
        if await cred.check_valid():
            print("[OK] Cookie 有效")
            print(f"  用户ID: {data.get('dedeuserid', '未知')}")
            return True
        else:
            print("[WARN] Cookie 已过期，请重新登录")
            return False
    except Exception as e:
        print(f"[ERROR] Cookie 检查失败: {e}")
        return False


def save_credential(credential: Credential):
    """保存 credential 到文件"""
    data = {
        "sessdata": credential.sessdata or "",
        "bili_jct": credential.bili_jct or "",
        "buvid3": credential.buvid3 or "",
        "dedeuserid": credential.dedeuserid or "",
        "ac_time_value": credential.ac_time_value or "",
    }
    COOKIE_PATH.parent.mkdir(parents=True, exist_ok=True)
    COOKIE_PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False))
    COOKIE_PATH.chmod(0o600)
    print(f"[OK] Cookie 已保存到: {COOKIE_PATH}")


async def do_login():
    """执行扫码登录"""
    print("=" * 40)
    print("B站扫码登录")
    print("=" * 40)
    print()

    qr = QrCodeLogin()
    await qr.generate_qrcode()

    # 终端显示二维码
    try:
        terminal_str = qr.get_qrcode_terminal()
        print(terminal_str)
    except Exception:
        print("[WARN] 无法在终端显示二维码")

    # 同时保存为图片
    try:
        pic = qr.get_qrcode_picture()
        qr_path = Path("/tmp/openclaw/bilibili_login_qr.png")
        qr_path.parent.mkdir(parents=True, exist_ok=True)
        # Picture 对象可能是 PIL Image 或有 content 属性
        if hasattr(pic, 'save'):
            pic.save(str(qr_path))
        elif hasattr(pic, 'content'):
            qr_path.write_bytes(pic.content)
        elif hasattr(pic, 'img'):
            pic.img.save(str(qr_path))
        else:
            qr_path.write_bytes(bytes(pic))
        print(f"\n[INFO] 二维码图片已保存: {qr_path}")
    except Exception as e:
        print(f"[WARN] 二维码图片保存失败: {e}")

    print("\n请用 B 站 App 扫描上方二维码...")
    print("等待扫码中（超时 120 秒）...\n")

    start = time.time()
    last_state = None
    while time.time() - start < 120:
        state = await qr.check_state()

        if state != last_state:
            if state == QrCodeLoginEvents.SCAN:
                print("[INFO] 已扫码，请在手机上确认...")
            elif state == QrCodeLoginEvents.CONF:
                print("[INFO] 已确认，正在获取凭证...")
            elif state == QrCodeLoginEvents.DONE:
                credential = qr.get_credential()
                save_credential(credential)
                print("[OK] 登录成功！")
                return True
            elif state == QrCodeLoginEvents.TIMEOUT:
                print("[ERROR] 二维码已过期")
                return False
            last_state = state

        await asyncio.sleep(2)

    print("[ERROR] 等待超时")
    return False


async def main():
    parser = argparse.ArgumentParser(description="B站登录工具")
    parser.add_argument("--check", action="store_true", help="检查现有 cookie 是否有效")
    args = parser.parse_args()

    if args.check:
        valid = await check_cookie()
        sys.exit(0 if valid else 1)
    else:
        success = await do_login()
        sys.exit(0 if success else 1)


if __name__ == "__main__":
    asyncio.run(main())
