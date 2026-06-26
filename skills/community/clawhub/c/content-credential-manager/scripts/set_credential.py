#!/usr/bin/env python3
"""
凭证写入脚本
用法: python3 set_credential.py <platform> <field> <value>
示例: python3 set_credential.py tavily api_key tvly-xxxxx
"""
import json
import os
import sys

CREDENTIALS_FILE = os.path.expanduser("~/.openclaw/credentials.json")

VALID_PLATFORMS = ["tavily", "stepfun", "meitu", "xiaohongshu", "wechat"]
VALID_FIELDS = {
    "tavily": ["api_key"],
    "stepfun": ["api_key"],
    "meitu": ["access_key", "secret_key"],
    "xiaohongshu": ["cookie"],
    "wechat": ["app_id", "app_secret"]
}

def load_credentials():
    if os.path.exists(CREDENTIALS_FILE):
        try:
            with open(CREDENTIALS_FILE, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    return {}

def save_credentials(creds):
    os.makedirs(os.path.dirname(CREDENTIALS_FILE), exist_ok=True)
    # 凭证文件权限：仅本人可读写
    os.umask(0o077)
    with open(CREDENTIALS_FILE, 'w') as f:
        json.dump(creds, f, indent=2, ensure_ascii=False)
    print(f"✅ 已保存到 {CREDENTIALS_FILE}")

def mask(value):
    """只显示前2后2位，中间用*"""
    if not value or len(value) <= 4:
        return "****"
    return value[:2] + "*" * (len(value) - 4) + value[-2:]

def main():
    if len(sys.argv) != 4:
        print("用法: python3 set_credential.py <platform> <field> <value>")
        print(f"平台: {', '.join(VALID_PLATFORMS)}")
        print("字段示例: api_key, access_key, secret_key, cookie, app_id, app_secret")
        print("\n示例:")
        print("  python3 set_credential.py tavily api_key tvly-xxxxx")
        print("  python3 set_credential.py stepfun api_key sk-xxxxx")
        print("  python3 set_credential.py wechat app_id wx_xxxxx")
        sys.exit(1)
    
    platform = sys.argv[1]
    field = sys.argv[2]
    value = sys.argv[3]
    
    # 验证平台
    if platform not in VALID_PLATFORMS:
        print(f"❌ 无效平台: {platform}")
        print(f"有效平台: {', '.join(VALID_PLATFORMS)}")
        sys.exit(1)
    
    # 验证字段
    if field not in VALID_FIELDS[platform]:
        print(f"❌ 无效字段: {field}")
        print(f"{platform} 有效字段: {', '.join(VALID_FIELDS[platform])}")
        sys.exit(1)
    
    # 加载现有凭证
    creds = load_credentials()
    if platform not in creds:
        creds[platform] = {}
    
    # 写入
    creds[platform][field] = value
    save_credentials(creds)
    
    print(f"\n📝 {platform}.{field} = {mask(value)}")

if __name__ == "__main__":
    main()
