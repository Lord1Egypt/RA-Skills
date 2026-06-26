# -*- coding: utf-8 -*-
"""
Data+AI Daily Brief — 邮件推送脚本
将日报以邮件形式发送给订阅者。

用法:
  python send_email.py                        # 推送今天的日报
  python send_email.py 2026-03-10             # 推送指定日期的日报

环境变量:
  SMTP_HOST       — SMTP 服务器地址
  SMTP_PORT       — SMTP 端口（默认 587）
  SMTP_USER       — SMTP 用户名
  SMTP_PASSWORD   — SMTP 密码
  EMAIL_FROM      — 发件人地址
  EMAIL_TO        — 收件人地址（逗号分隔多个）
"""
import os
import sys
import json
import smtplib
import argparse
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
PROJECT_DIR = SCRIPT_DIR.parent
CONFIG_FILE = PROJECT_DIR / "daily-brief-config.json"


def load_config():
    """加载配置文件。"""
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def get_email_config():
    """获取邮件配置。"""
    config = load_config()
    email_cfg = config.get("adapters", {}).get("email", {})

    return {
        "smtp_host": os.environ.get("SMTP_HOST", email_cfg.get("smtp_host", "")),
        "smtp_port": int(os.environ.get("SMTP_PORT", email_cfg.get("smtp_port", 587))),
        "smtp_user": os.environ.get("SMTP_USER", email_cfg.get("smtp_user", "")),
        "smtp_password": os.environ.get("SMTP_PASSWORD", email_cfg.get("smtp_password", "")),
        "from_addr": os.environ.get("EMAIL_FROM", email_cfg.get("from_addr", "")),
        "to_addrs": os.environ.get("EMAIL_TO", ",".join(email_cfg.get("to_addrs", []))),
        "use_tls": email_cfg.get("use_tls", True),
    }


def find_files(date_str, search_dirs=None):
    """查找指定日期的日报文件。"""
    if search_dirs is None:
        search_dirs = [PROJECT_DIR, Path(".")]

    patterns = [
        f"Data+AI全球日报_{date_str}",
        f"Data+AI全球日报_{date_str}_v3",
        f"Data+AI全球日报_{date_str}_v2",
    ]

    md_path = None
    html_path = None

    for directory in search_dirs:
        for base in patterns:
            md = directory / f"{base}.md"
            html = directory / f"{base}.html"
            if md.exists() and not md_path:
                md_path = md
            if html.exists() and not html_path:
                html_path = html

    return md_path, html_path


def send_email(config, date_str, md_path, html_path=None):
    """发送日报邮件。"""
    if not config["smtp_host"] or not config["smtp_user"]:
        print("[错误] 邮件配置不完整，请设置 SMTP 相关环境变量或配置文件")
        sys.exit(1)

    to_addrs = [addr.strip() for addr in config["to_addrs"].split(",") if addr.strip()]
    if not to_addrs:
        print("[错误] 未配置收件人地址")
        sys.exit(1)

    # 读取 HTML 内容（用作邮件正文）
    if html_path and html_path.exists():
        with open(html_path, "r", encoding="utf-8") as f:
            html_content = f.read()
    else:
        # 如果没有 HTML，用 MD 内容
        with open(md_path, "r", encoding="utf-8") as f:
            html_content = f"<pre>{f.read()}</pre>"

    # 构建邮件
    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"Data+AI 全球日报 | {date_str}"
    msg["From"] = config["from_addr"] or config["smtp_user"]
    msg["To"] = ", ".join(to_addrs)

    # 纯文本版本
    with open(md_path, "r", encoding="utf-8") as f:
        text_content = f.read()
    msg.attach(MIMEText(text_content, "plain", "utf-8"))

    # HTML 版本
    msg.attach(MIMEText(html_content, "html", "utf-8"))

    # 发送
    print(f"  连接 {config['smtp_host']}:{config['smtp_port']}...")
    try:
        if config["use_tls"]:
            server = smtplib.SMTP(config["smtp_host"], config["smtp_port"])
            server.starttls()
        else:
            server = smtplib.SMTP_SSL(config["smtp_host"], config["smtp_port"])

        server.login(config["smtp_user"], config["smtp_password"])
        server.sendmail(
            config["from_addr"] or config["smtp_user"],
            to_addrs,
            msg.as_string()
        )
        server.quit()
        print(f"  [成功] 邮件已发送至: {', '.join(to_addrs)}")
    except Exception as e:
        print(f"  [失败] 邮件发送错误: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Data+AI 日报邮件推送")
    parser.add_argument("date", nargs="?", default=None, help="日期 YYYY-MM-DD")
    parser.add_argument("--search-dir", action="append", help="额外搜索目录")
    args = parser.parse_args()

    if args.date:
        try:
            dt = datetime.strptime(args.date, "%Y-%m-%d")
            date_str = dt.strftime("%Y-%m-%d")
        except ValueError:
            print(f"[错误] 日期格式无效: {args.date}，应为 YYYY-MM-DD")
            sys.exit(1)
    else:
        date_str = datetime.now().strftime("%Y-%m-%d")

    config = get_email_config()

    search_dirs = [PROJECT_DIR, Path(".")]
    if args.search_dir:
        search_dirs.extend(Path(d) for d in args.search_dir)

    print("=" * 55)
    print(f"  Data+AI Daily Brief — 邮件推送")
    print(f"  目标日期: {date_str}")
    print("=" * 55)

    md_path, html_path = find_files(date_str, search_dirs)
    if not md_path:
        print(f"\n[错误] 未找到 {date_str} 的 Markdown 日报文件")
        sys.exit(1)

    print(f"\n[MD]   {md_path.name}")
    if html_path:
        print(f"[HTML] {html_path.name}")

    print(f"\n发送邮件...")
    send_email(config, date_str, md_path, html_path)

    print("\n" + "=" * 55)
    print("  推送完成!")
    print("=" * 55)


if __name__ == "__main__":
    main()
