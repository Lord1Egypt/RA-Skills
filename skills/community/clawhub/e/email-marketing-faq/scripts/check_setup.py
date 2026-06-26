#!/usr/bin/env python3
"""
环境检查和快速开始向导
"""

import os
import sys


def check_python_version():
    """检查Python版本"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python版本过低，需要 Python 3.8+")
        print(f"   当前版本: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python版本: {version.major}.{version.minor}.{version.micro}")
    return True


def check_package(package_name, import_name=None):
    """检查Python包是否安装"""
    if import_name is None:
        import_name = package_name

    try:
        __import__(import_name)
        print(f"✅ {package_name} 已安装")
        return True
    except ImportError:
        print(f"❌ {package_name} 未安装")
        return False



def check_email_config():
    """检查邮件配置"""
    smtp_user = os.getenv("EMAIL_SMTP_USER")
    smtp_pass = os.getenv("EMAIL_SMTP_PASS")
    test_email = os.getenv("EMAIL_TEST_TARGET")
    imap_host = os.getenv("EMAIL_IMAP_HOST")
    smtp_host = os.getenv("EMAIL_SMTP_HOST")

    if smtp_user:
        masked = smtp_user[:3] + "***" + smtp_user[smtp_user.index("@"):] if "@" in smtp_user else "***"
        print(f"✅ EMAIL_SMTP_USER 已配置: {masked}")
    else:
        print("⚠️  EMAIL_SMTP_USER 未配置")

    if smtp_pass:
        print(f"✅ EMAIL_SMTP_PASS 已配置 (***)")
    else:
        print("⚠️  EMAIL_SMTP_PASS 未配置")

    if test_email:
        masked_test = test_email[:3] + "***" + test_email[test_email.index("@"):] if "@" in test_email else "***"
        print(f"✅ EMAIL_TEST_TARGET 已配置: {masked_test}")
    else:
        print("⚠️  EMAIL_TEST_TARGET 未配置")

    if smtp_host:
        print(f"✅ EMAIL_SMTP_HOST 已配置: {smtp_host}")
    else:
        print(f"ℹ️  EMAIL_SMTP_HOST 使用默认: example.com")

    if imap_host:
        print(f"✅ EMAIL_IMAP_HOST 已配置: {imap_host}")
    else:
        print(f"ℹ️  EMAIL_IMAP_HOST 使用默认: example.com")

    return bool(smtp_user and smtp_pass)


def check_files():
    """检查必需文件"""
    files_to_check = {
        "final_sender.py": "邮件发送脚本",
        "auto_reply_manager.py": "自动回信脚本",
        "check_replies.py": "统计报表脚本",
    }

    all_exist = True
    for file_path, description in files_to_check.items():
        if os.path.exists(file_path):
            print(f"✅ {description}: {file_path}")
        else:
            print(f"❌ {description} 不存在: {file_path}")
            all_exist = False

    # 检查 FAQ 文件（非必需，但会提示）
    faq_path = os.getenv("EMAIL_FAQ_PATH", os.path.expanduser("~/Desktop/faq.txt"))
    if os.path.exists(faq_path):
        print(f"✅ FAQ 知识库: {faq_path}")
    else:
        print(f"ℹ️  FAQ 知识库未找到: {faq_path} (自动回信功能需要)")

    return all_exist


def main():
    print("=" * 70)
    print("📧 Email Marketing Skill - 环境检查")
    print("=" * 70)
    print()

    print("【1/4】检查 Python 版本")
    print("-" * 70)
    check_python_version()
    print()

    print("【2/4】检查 Python 依赖包")
    print("-" * 70)
    packages = {
        "pandas": "pandas",
        "openpyxl": "openpyxl",
        "imapclient": "imapclient",
    }

    missing_packages = []
    for pkg_name, import_name in packages.items():
        if not check_package(pkg_name, import_name):
            missing_packages.append(pkg_name)

    if missing_packages:
        print(f"\n💡 安装缺失的包:")
        print(f"   pip install {' '.join(missing_packages)}")
    print()


    print("【3/4】检查邮件发送配置")
    print("-" * 70)
    has_email = check_email_config()
    if not has_email:
        print("\n💡 配置邮件服务:")
        print("   export EMAIL_SMTP_USER='your-email@example.com'")
        print("   export EMAIL_SMTP_PASS='your-password'")
        print("   export EMAIL_TEST_TARGET='test@example.com'")
    print()

    print("【4/4】检查脚本文件")
    print("-" * 70)
    check_files()
    print()

    print("=" * 70)
    print("🎯 快速开始")
    print("=" * 70)
    print()
    print("1️⃣  准备文案: 创建 ~/Desktop/邮件文案.txt")
    print("2️⃣  准备名单: 创建 ~/Desktop/邮箱.xlsx")
    print("3️⃣  准备标题: 创建 ~/Desktop/邮件标题.txt")
    print("4️⃣  生成HTML: 使用 AI 将文案转换为 HTML 并保存为 ~/Desktop/邮件内容.html")
    print("5️⃣  测试发送: python3 final_sender.py")
    print("6️⃣  正式群发: python3 final_sender.py run")
    print()
    print("💡 自动回信功能:")
    print("   - 准备FAQ: 创建 ~/Desktop/faq.txt")
    print("   - 扫描回信: python3 auto_reply_manager.py")
    print("   - 查看统计: python3 check_replies.py")
    print()
    print("📖 详细文档: ../SKILL.md")
    print()


if __name__ == "__main__":
    try:
        # 切换到脚本目录
        script_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(script_dir)

        main()
    except KeyboardInterrupt:
        print("\n\n检查已取消")
        sys.exit(0)
