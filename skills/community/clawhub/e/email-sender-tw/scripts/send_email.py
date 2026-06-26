#!/usr/bin/env python3
"""
郵件發送腳本
支持純文字/HTML 郵件、附件和批量發送
"""

import smtplib
import os
import sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from typing import List, Optional
import json

# 配置文件路徑
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(SCRIPT_DIR, "smtp_config.json")
KEYCHAIN_SERVICE = "openclaw-email-sender"


def get_account_config(account_name: Optional[str] = None):
    """獲取 SMTP 配置"""
    # 讀取配置文件
    if not os.path.exists(CONFIG_FILE):
        raise Exception("配置文件不存在。請先使用 config.py setup 配置 SMTP。")

    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        config = json.load(f)

    if not config["accounts"]:
        raise Exception("沒有找到任何 SMTP 配置。")

    # 如果沒有指定名稱，使用第一個配置
    if account_name is None:
        account_name = config["accounts"][0]["name"]

    # 查找配置
    account = None
    for acc in config["accounts"]:
        if acc["name"] == account_name:
            account = acc
            break

    if account is None:
        raise Exception(f"找不到配置 '{account_name}'。")

    return account


def get_password_from_keychain(email: str) -> str:
    """從 macOS Keychain 獲取密碼"""
    cmd = [
        "security", "find-generic-password",
        "-s", KEYCHAIN_SERVICE,
        "-a", email,
        "-w"
    ]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        raise Exception(f"無法從 Keychain 獲取 {email} 的密碼")


import subprocess


def send_email(
    to: str,
    subject: str,
    body: str,
    from_email: Optional[str] = None,
    account_name: Optional[str] = None,
    html: bool = False,
    cc: Optional[str] = None,
    bcc: Optional[str] = None,
    reply_to: Optional[str] = None,
    attachments: Optional[List[str]] = None
) -> bool:
    """
    發送郵件

    參數:
        to: 收件人郵件地址
        subject: 郵件主題
        body: 郵件內容
        from_email: 發件人郵件地址（可選，默認使用 SMTP 帳號）
        account_name: SMTP 配置名稱（可選，默認使用第一個）
        html: 是否為 HTML 郵件（默認 False）
        cc: 抄送郵件地址（可選）
        bcc: 密送郵件地址（可選）
        reply_to: 回覆郵件地址（可選）
        attachments: 附件檔案路徑列表（可選）

    返回:
        bool: 發送成功返回 True，失敗返回 False
    """
    try:
        # 獲取 SMTP 配置
        account = get_account_config(account_name)

        # 獲取密碼
        password = get_password_from_keychain(account["email"])

        # 獲取發件人郵件地址
        sender = from_email or account["email"]

        # 創建郵件
        if attachments:
            # 如果有附件，使用 MIMEMultipart
            msg = MIMEMultipart()
            msg.attach(MIMEText(body, "html" if html else "plain", "utf-8"))
        else:
            # 沒有附件，直接使用 MIMEText
            msg = MIMEText(body, "html" if html else "plain", "utf-8")

        # 設置郵件頭
        msg["Subject"] = subject
        msg["From"] = f"{sender} <{account['email']}>"
        msg["To"] = to

        if cc:
            msg["Cc"] = cc

        if reply_to:
            msg["Reply-To"] = reply_to

        # 添加附件
        if attachments:
            for file_path in attachments:
                if not os.path.exists(file_path):
                    print(f"⚠️  附件不存在: {file_path}")
                    continue

                with open(file_path, "rb") as f:
                    part = MIMEApplication(f.read())

                # 設置附件檔名
                filename = os.path.basename(file_path)
                part.add_header(
                    "Content-Disposition",
                    "attachment",
                    filename=filename
                )
                msg.attach(part)

        # 連接 SMTP 服務器
        if account["use_tls"]:
            server = smtplib.SMTP(account["smtp_server"], account["smtp_port"])
            server.starttls()
        else:
            server = smtplib.SMTP_SSL(account["smtp_server"], account["smtp_port"])

        # 登入
        server.login(account["email"], password)

        # 準備收件人列表（包括抄送和密送）
        recipients = [to]
        if cc:
            recipients.extend([addr.strip() for addr in cc.split(",")])
        if bcc:
            recipients.extend([addr.strip() for addr in bcc.split(",")])

        # 發送郵件
        server.send_message(msg)
        server.quit()

        print(f"✅ 郵件已成功發送到: {to}")
        if cc:
            print(f"   抄送: {cc}")
        if attachments:
            print(f"   附件: {len(attachments)} 個")

        return True

    except Exception as e:
        print(f"❌ 郵件發送失敗: {e}")
        return False


def send_batch(
    recipients: List[str],
    subject: str,
    body: str,
    account_name: Optional[str] = None,
    html: bool = False,
    attachments: Optional[List[str]] = None
) -> dict:
    """
    批量發送郵件

    參數:
        recipients: 收件人郵件地址列表
        subject: 郵件主題
        body: 郵件內容
        account_name: SMTP 配置名稱（可選）
        html: 是否為 HTML 郵件（默認 False）
        attachments: 附件檔案路徑列表（可選）

    返回:
        dict: {email: success} 郵件發送結果
    """
    results = {}

    for recipient in recipients:
        success = send_email(
            to=recipient,
            subject=subject,
            body=body,
            account_name=account_name,
            html=html,
            attachments=attachments
        )
        results[recipient] = success

    # 統計結果
    success_count = sum(1 for v in results.values() if v)
    total_count = len(results)

    print(f"\n批量發送完成: {success_count}/{total_count} 成功")

    return results


def main():
    """命令行界面（用於測試）"""
    print("=== Email Sender CLI ===\n")

    # 導入 config 模塊
    sys.path.insert(0, SCRIPT_DIR)
    import config

    # 列出可用配置
    config.list_configs()

    # 選擇配置
    account_name = input("\n選擇配置名稱（留空使用第一個）: ").strip() or None

    # 輸入郵件信息
    to = input("收件人: ").strip()
    subject = input("主題: ").strip()
    print("郵件內容（輸入結束後按 Ctrl+D）:")

    # 讀取多行輸入
    body_lines = []
    try:
        while True:
            line = input()
            body_lines.append(line)
    except EOFError:
        pass

    body = "\n".join(body_lines)

    # 詢問是否為 HTML
    html_choice = input("是否為 HTML 郵件？(y/n，默認 n): ").strip().lower()
    html = html_choice == 'y'

    # 發送郵件
    send_email(
        to=to,
        subject=subject,
        body=body,
        account_name=account_name,
        html=html
    )


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "batch":
        # 批量發送模式
        print("=== 批量發送郵件 ===")
        recipients = input("收件人郵件地址（用逗號分隔）: ").strip().split(",")
        recipients = [r.strip() for r in recipients if r.strip()]

        subject = input("主題: ").strip()
        body = input("郵件內容: ").strip()

        html_choice = input("是否為 HTML 郵件？(y/n，默認 n): ").strip().lower()
        html = html_choice == 'y'

        send_batch(recipients, subject, body, html=html)
    else:
        main()
