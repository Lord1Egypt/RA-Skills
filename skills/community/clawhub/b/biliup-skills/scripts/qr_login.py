#!/usr/bin/env python3
"""
biliup 登录辅助脚本 — 生成登录二维码图片

功能：
  启动 `biliup login`，捕获其输出的授权 URL，
  将 URL 生成为 PNG 二维码图片，供用户用 B 站 App 扫码授权。

说明：
  - biliup 是 B 站官方支持的第三方上传工具（https://github.com/biliup/biliup）
  - cookies.json 保存的是用户自己的 B 站登录凭据（access_token），
    仅用于后续上传视频，不会上传至任何第三方服务器
  - 本脚本不收集、不传输任何用户数据

依赖：
  pip install qrcode[pil]

用法：
  python3 scripts/qr_login.py --cookie /path/to/cookies.json [--output /tmp/qr.png] [--wait]
"""

import subprocess
import sys
import re
import os
import tempfile
import time
import shutil
import argparse


def find_biliup() -> str | None:
    """查找 biliup 可执行文件路径"""
    local_bin = os.path.expanduser("~/.local/bin/biliup")
    if os.path.isfile(local_bin) and os.access(local_bin, os.X_OK):
        return local_bin
    return shutil.which("biliup")


def ensure_qrcode():
    """确保 qrcode 库可用，不存在时自动安装"""
    try:
        import qrcode  # noqa: F401
        from PIL import Image  # noqa: F401
    except ImportError:
        print("📦 安装 qrcode[pil] 依赖...", file=sys.stderr)
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-q", "qrcode[pil]"],
            check=True,
        )


def generate_qr_png(url: str, output_path: str):
    """将 URL 生成为二维码 PNG 图片"""
    import qrcode

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(output_path)


# B 站 TV/扫码授权 URL 特征
_AUTH_URL_PATTERN = re.compile(
    r"https://passport\.bilibili\.com/(?:x/passport-tv-login/h5/qrcode/auth|h5-app/passport/)[^\s'\"]+"
)


def run_biliup_login(biliup_path: str, cookie_path: str, timeout: int = 30):
    """
    启动 biliup login，从输出中提取授权 URL。

    返回: (proc, auth_url | None, raw_lines)
    """
    cmd = [biliup_path, "-u", cookie_path, "login"]
    print(f"▶ 启动: {' '.join(cmd)}", file=sys.stderr)

    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )

    found_url: str | None = None
    lines: list[str] = []
    deadline = time.monotonic() + timeout

    while time.monotonic() < deadline:
        line = proc.stdout.readline()
        if not line:
            if proc.poll() is not None:
                break
            time.sleep(0.1)
            continue

        line = line.rstrip()
        lines.append(line)
        print(f"[biliup] {line}", file=sys.stderr)

        m = _AUTH_URL_PATTERN.search(line)
        if m:
            found_url = m.group(0)
            break

    return proc, found_url, lines


def wait_for_completion(proc: subprocess.Popen, timeout: int = 120) -> bool:
    """等待 biliup login 进程退出，返回是否成功"""
    print("⏳ 等待用户扫码并授权...", file=sys.stderr)
    try:
        proc.wait(timeout=timeout)
    except subprocess.TimeoutExpired:
        proc.kill()
        print("⏰ 等待超时，进程已终止", file=sys.stderr)
        return False
    return proc.returncode == 0


def main():
    parser = argparse.ArgumentParser(
        description="biliup 登录辅助：生成扫码登录二维码图片"
    )
    parser.add_argument(
        "--cookie",
        default="cookies.json",
        help="登录凭据保存路径（默认: cookies.json）",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="二维码 PNG 输出路径（默认: 系统临时目录/biliup_qr.png）",
    )
    parser.add_argument(
        "--wait",
        action="store_true",
        help="生成二维码后继续等待登录完成再退出",
    )
    args = parser.parse_args()

    # 检查 biliup 是否存在
    biliup = find_biliup()
    if not biliup:
        print("❌ 未找到 biliup，请先运行 scripts/setup_biliup.sh", file=sys.stderr)
        sys.exit(1)

    ensure_qrcode()

    qr_path = args.output or os.path.join(tempfile.gettempdir(), "biliup_qr.png")
    cookie_path = os.path.abspath(args.cookie)

    # 启动登录并捕获授权 URL
    proc, url, raw_lines = run_biliup_login(biliup, cookie_path)

    if not url:
        print("❌ 未能从 biliup 输出中提取授权 URL", file=sys.stderr)
        print("原始输出:", file=sys.stderr)
        for line in raw_lines:
            print(f"  {line}", file=sys.stderr)
        if proc.poll() is None:
            proc.kill()
        sys.exit(1)

    # 生成二维码图片
    generate_qr_png(url, qr_path)
    print(f"🖼️  二维码图片: {qr_path}", file=sys.stderr)
    print(f"🔗 授权链接: {url}", file=sys.stderr)

    # 输出图片路径到 stdout（供调用方读取）
    print(qr_path)

    # 等待登录完成
    if args.wait or proc.poll() is None:
        success = wait_for_completion(proc)
        if success:
            print(f"✅ 登录成功！凭据已保存至: {cookie_path}", file=sys.stderr)
            sys.exit(0)
        else:
            print("❌ 登录失败或超时", file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main()
