#!/usr/bin/env python3
"""
Email Sender 測試腳本
用於快速測試各項功能
"""

import os
import sys

# 添加 scripts 目錄到路徑
SCRIPT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scripts")
sys.path.insert(0, SCRIPT_DIR)

from template_manager import list_templates, preview_template
from send_email import send_email


def test_template_preview():
    """測試模板預覽功能"""
    print("=" * 60)
    print("測試 1: 模板預覽")
    print("=" * 60)

    templates = list_templates()

    if not templates:
        print("⚠️  沒有可用的模板。先運行 'python3 scripts/template_manager.py init-defaults'")
        return False

    print(f"\n找到 {len(templates)} 個模板: {', '.join(templates)}\n")

    # 測試第一個模板
    print(f"預覽模板: {templates[0]}")
    print("-" * 60)

    preview_template(templates[0], {"name": "測試用戶", "date": "2026-03-08", "sender": "文森"})

    print("\n✅ 模板預覽測試通過！\n")
    return True


def test_config_status():
    """檢查配置狀態"""
    print("=" * 60)
    print("測試 2: 配置檢查")
    print("=" * 60)

    config_file = os.path.join(SCRIPT_DIR, "smtp_config.json")

    if not os.path.exists(config_file):
        print("⚠️  SMTP 配置文件不存在。")
        print("   請運行: python3 scripts/config.py setup")
        return False

    with open(config_file, 'r', encoding='utf-8') as f:
        import json
        config = json.load(f)

    if not config.get("accounts"):
        print("⚠️  沒有 SMTP 配置。")
        print("   請運行: python3 scripts/config.py setup")
        return False

    print(f"\n找到 {len(config['accounts'])} 個 SMTP 配置:")

    for account in config["accounts"]:
        print(f"  - {account['name']}: {account['email']}")

    print("\n✅ 配置檢查通過！\n")
    return True


def test_send_email():
    """測試發送郵件功能"""
    print("=" * 60)
    print("測試 3: 發送郵件")
    print("=" * 60)

    config_file = os.path.join(SCRIPT_DIR, "smtp_config.json")

    if not os.path.exists(config_file):
        print("⚠️  請先配置 SMTP: python3 scripts/config.py setup")
        return False

    choice = input("\n要實際發送測試郵件嗎？(y/n): ").strip().lower()

    if choice != 'y':
        print("跳過實際發送測試。")
        return True

    # 獲取收件人
    with open(config_file, 'r', encoding='utf-8') as f:
        import json
        config = json.load(f)

    # 使用配置中的郵件帳號作為收件人
    recipient = config["accounts"][0]["email"]

    print(f"\n發送測試郵件到: {recipient}")

    success = send_email(
        to=recipient,
        subject="Email Sender 測試郵件",
        body="這是 Email Sender 的測試郵件。如果你看到這封郵件，表示發送功能正常運作！"
    )

    if success:
        print("\n✅ 郵件發送測試通過！\n")
        return True
    else:
        print("\n❌ 郵件發送測試失敗。\n")
        return False


def main():
    """主函數"""
    print("\n" + "=" * 60)
    print("Email Sender 功能測試")
    print("=" * 60 + "\n")

    results = []

    # 測試 1: 模板預覽
    results.append(("模板預覽", test_template_preview()))

    # 測試 2: 配置檢查
    results.append(("配置檢查", test_config_status()))

    # 測試 3: 發送郵件（可選）
    if results[1][1]:  # 如果配置存在
        results.append(("發送郵件", test_send_email()))

    # 總結
    print("=" * 60)
    print("測試總結")
    print("=" * 60)

    for name, result in results:
        status = "✅ 通過" if result else "❌ 失敗"
        print(f"{name}: {status}")

    # 整體結果
    all_passed = all(result for _, result in results)
    print()
    if all_passed:
        print("🎉 所有測試通過！Email Sender 可以正常使用。")
    else:
        print("⚠️  部分測試失敗，請檢查配置。")

    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  測試已被中斷。")
