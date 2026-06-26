#!/usr/bin/env python3
"""
SMTP 配置管理腳本
使用 macOS Keychain 安全存儲密碼
"""

import json
import subprocess
import sys
import os
from getpass import getpass

# 配置文件路徑
CONFIG_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(CONFIG_DIR, "smtp_config.json")
KEYCHAIN_SERVICE = "openclaw-email-sender"


def run_command(cmd):
    """執行 shell 命令並返回結果"""
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip(), None
    except subprocess.CalledProcessError as e:
        return None, e.stderr.strip()


def keychain_add_password(account, password):
    """將密碼添加到 macOS Keychain"""
    cmd = [
        "security", "add-generic-password",
        "-s", KEYCHAIN_SERVICE,
        "-a", account,
        "-w", password,
        "-U"  # 更新已存在的密碼
    ]
    _, error = run_command(cmd)
    return error is None, error


def keychain_get_password(account):
    """從 macOS Keychain 獲取密碼"""
    cmd = [
        "security", "find-generic-password",
        "-s", KEYCHAIN_SERVICE,
        "-a", account,
        "-w"
    ]
    password, error = run_command(cmd)
    return password if error is None else None


def keychain_delete_password(account):
    """從 macOS Keychain 刪除密碼"""
    cmd = [
        "security", "delete-generic-password",
        "-s", KEYCHAIN_SERVICE,
        "-a", account
    ]
    _, error = run_command(cmd)
    # 如果密碼不存在，security 返回非 0 但我們忽略這個錯誤
    return True


def load_config():
    """加載配置文件"""
    if not os.path.exists(CONFIG_FILE):
        return {"accounts": []}

    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_config(config):
    """保存配置文件"""
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)


def setup():
    """配置 SMTP 服務器"""
    print("=== Email Sender SMTP 配置 ===\n")

    # 輸入 SMTP 配置
    name = input("SMTP 配置名稱（用於識別，例如: gmail）: ").strip()

    # 檢查是否已存在
    config = load_config()
    for account in config["accounts"]:
        if account["name"] == name:
            print(f"\n⚠️  配置 '{name}' 已存在。")
            choice = input("是否要更新配置？(y/n): ").strip().lower()
            if choice != 'y':
                print("配置已取消。")
                return

            # 刪除舊密碼
            keychain_delete_password(account["email"])
            config["accounts"] = [a for a in config["accounts"] if a["name"] != name]

    smtp_server = input("SMTP 服務器（例如: smtp.gmail.com）: ").strip()
    smtp_port = input("SMTP 端口（587 for TLS, 465 for SSL，默認: 587）: ").strip() or "587"
    use_tls = smtp_port == "587"
    email = input("郵件帳號（例如: yourname@gmail.com）: ").strip()
    password = getpass("郵件密碼（或應用專屬密碼）: ").strip()

    # 驗證端口
    try:
        smtp_port = int(smtp_port)
    except ValueError:
        print("❌ 無效的端口號。")
        return

    # 保存密碼到 Keychain
    success, error = keychain_add_password(email, password)
    if not success:
        print(f"❌ 保存密碼失敗: {error}")
        return

    # 保存配置
    account_config = {
        "name": name,
        "smtp_server": smtp_server,
        "smtp_port": smtp_port,
        "use_tls": use_tls,
        "email": email
    }

    config["accounts"].append(account_config)
    save_config(config)

    print(f"\n✅ SMTP 配置 '{name}' 已保存！")
    print(f"   服務器: {smtp_server}:{smtp_port}")
    print(f"   郵件帳號: {email}")


def test_config(name=None):
    """測試 SMTP 配置"""
    config = load_config()

    if not config["accounts"]:
        print("❌ 沒有找到任何 SMTP 配置。請先使用 'setup' 命令配置。")
        return

    # 如果沒有指定名稱，使用第一個配置
    if name is None:
        name = config["accounts"][0]["name"]
        print(f"使用配置: {name}")

    # 查找配置
    account = None
    for acc in config["accounts"]:
        if acc["name"] == name:
            account = acc
            break

    if account is None:
        print(f"❌ 找不到配置 '{name}'。")
        return

    # 從 Keychain 獲取密碼
    password = keychain_get_password(account["email"])
    if password is None:
        print(f"❌ 無法從 Keychain 獲取密碼。")
        return

    # 測試連接
    try:
        import smtplib
        from email.mime.text import MIMEText

        print(f"\n測試 SMTP 連接: {account['smtp_server']}:{account['smtp_port']}")

        if account["use_tls"]:
            server = smtplib.SMTP(account["smtp_server"], account["smtp_port"])
            server.starttls()
        else:
            server = smtplib.SMTP_SSL(account["smtp_server"], account["smtp_port"])

        server.login(account["email"], password)

        # 發送測試郵件
        print("發送測試郵件...")
        msg = MIMEText("這是 Email Sender 的測試郵件。", "plain", "utf-8")
        msg["Subject"] = "Email Sender 測試"
        msg["From"] = account["email"]
        msg["To"] = account["email"]

        server.send_message(msg)
        server.quit()

        print("\n✅ SMTP 配置測試成功！")
        print(f"   已發送測試郵件到: {account['email']}")

    except Exception as e:
        print(f"\n❌ SMTP 測試失敗: {e}")
        print("\n可能的原因:")
        print("1. SMTP 服務器或端口不正確")
        print("2. 郵件帳號或密碼錯誤")
        print("3. 網路連線問題")
        print("4. 郵件服務商的限制（如 Gmail 需要應用專屬密碼）")


def list_configs():
    """列出所有配置"""
    config = load_config()

    if not config["accounts"]:
        print("沒有任何 SMTP 配置。")
        return

    print("=== SMTP 配置列表 ===\n")

    for i, account in enumerate(config["accounts"], 1):
        print(f"{i}. {account['name']}")
        print(f"   服務器: {account['smtp_server']}:{account['smtp_port']}")
        print(f"   郵件帳號: {account['email']}")
        print(f"   加密: {'TLS' if account['use_tls'] else 'SSL'}")
        print()


def remove_config(name):
    """刪除配置"""
    config = load_config()

    # 查找配置
    account = None
    for acc in config["accounts"]:
        if acc["name"] == name:
            account = acc
            break

    if account is None:
        print(f"❌ 找不到配置 '{name}'。")
        return

    # 刪除 Keychain 中的密碼
    keychain_delete_password(account["email"])

    # 刪除配置
    config["accounts"] = [a for a in config["accounts"] if a["name"] != name]
    save_config(config)

    print(f"✅ 配置 '{name}' 已刪除。")


def main():
    """主函數"""
    if len(sys.argv) < 2:
        print("用法:")
        print("  python3 config.py setup          - 配置 SMTP 服務器")
        print("  python3 config.py test [name]    - 測試 SMTP 配置")
        print("  python3 config.py list           - 列出所有配置")
        print("  python3 config.py remove <name>  - 刪除配置")
        return

    command = sys.argv[1]

    if command == "setup":
        setup()
    elif command == "test":
        name = sys.argv[2] if len(sys.argv) > 2 else None
        test_config(name)
    elif command == "list":
        list_configs()
    elif command == "remove":
        if len(sys.argv) < 3:
            print("❌ 請指定要刪除的配置名稱。")
            return
        remove_config(sys.argv[2])
    else:
        print(f"❌ 未知命令: {command}")


if __name__ == "__main__":
    main()
