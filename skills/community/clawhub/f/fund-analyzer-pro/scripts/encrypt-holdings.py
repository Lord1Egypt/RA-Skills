#!/usr/bin/env python3
"""
用户持仓加密存储工具

**用途**：
- 加密存储用户基金持仓数据
- 支持读取/更新/删除
- 使用 Fernet 对称加密

**存储位置**：~/.openclaw/workspace/data/fund-holdings/{user_id}.enc
"""

import json
import os
from pathlib import Path
from cryptography.fernet import Fernet
from datetime import datetime

# 加密密钥（从环境变量获取，没有则生成）
ENCRYPTION_KEY = os.environ.get("FUND_HOLDINGS_KEY")
if not ENCRYPTION_KEY:
    # 生成新密钥并保存
    ENCRYPTION_KEY = Fernet.generate_key().decode()
    print(f"⚠️  生成新加密密钥，请保存到环境变量：FUND_HOLDINGS_KEY={ENCRYPTION_KEY}")
    print(f"   或保存到文件：~/.openclaw/workspace/.fund_holdings_key")
    
    # 保存到文件
    key_file = Path.home() / ".openclaw" / "workspace" / ".fund_holdings_key"
    with open(key_file, 'w') as f:
        f.write(ENCRYPTION_KEY)
    print(f"   密钥已保存到：{key_file}")

cipher = Fernet(ENCRYPTION_KEY.encode() if isinstance(ENCRYPTION_KEY, str) else ENCRYPTION_KEY)

# 持仓存储目录
HOLDINGS_DIR = Path.home() / ".openclaw" / "workspace" / "data" / "fund-holdings"
HOLDINGS_DIR.mkdir(parents=True, exist_ok=True)

def get_holdings_file(user_id: str) -> Path:
    """获取用户持仓文件路径"""
    return HOLDINGS_DIR / f"{user_id}.enc"

def encrypt_data(data: dict) -> bytes:
    """加密数据"""
    json_str = json.dumps(data, ensure_ascii=False).encode('utf-8')
    return cipher.encrypt(json_str)

def decrypt_data(encrypted: bytes) -> dict:
    """解密数据"""
    json_bytes = cipher.decrypt(encrypted)
    return json.loads(json_bytes.decode('utf-8'))

def save_holdings(user_id: str, holdings: dict):
    """
    保存用户持仓
    
    **参数**：
    - user_id: 用户 ID
    - holdings: 持仓数据 {
        "funds": [
            {"code": "000001", "name": "易方达蓝筹", "amount": 100000, "cost": 1.5, ...}
        ],
        "updated_at": "2026-04-16"
      }
    """
    file_path = get_holdings_file(user_id)
    
    # 添加时间戳
    holdings['updated_at'] = datetime.now().isoformat()
    holdings['created_at'] = holdings.get('created_at', holdings['updated_at'])
    
    # 加密保存
    encrypted = encrypt_data(holdings)
    with open(file_path, 'wb') as f:
        f.write(encrypted)
    
    print(f"✅ 持仓已加密保存：{file_path}")
    return True

def load_holdings(user_id: str) -> dict:
    """
    加载用户持仓
    
    **返回**：
    - 成功：持仓数据 dict
    - 失败：None
    """
    file_path = get_holdings_file(user_id)
    
    if not file_path.exists():
        print(f"⚠️  用户持仓不存在：{user_id}")
        return None
    
    try:
        with open(file_path, 'rb') as f:
            encrypted = f.read()
        holdings = decrypt_data(encrypted)
        print(f"✅ 持仓已加载：{user_id}")
        return holdings
    except Exception as e:
        print(f"❌ 加载失败：{e}")
        return None

def delete_holdings(user_id: str):
    """
    删除用户持仓（数据删除）
    
    **参数**：
    - user_id: 用户 ID
    """
    file_path = get_holdings_file(user_id)
    
    if file_path.exists():
        file_path.unlink()
        print(f"✅ 持仓已删除：{user_id}")
        return True
    else:
        print(f"⚠️  持仓不存在：{user_id}")
        return False

def list_holdings() -> list:
    """
    列出所有用户持仓文件
    
    **返回**：
    - 用户 ID 列表
    """
    files = list(HOLDINGS_DIR.glob("*.enc"))
    user_ids = [f.stem for f in files]
    print(f"📊 共有 {len(user_ids)} 个用户持仓")
    for uid in user_ids:
        print(f"  - {uid}")
    return user_ids

def export_holdings(user_id: str, output_path: str = None):
    """
    导出用户持仓（明文，用于备份）
    
    **参数**：
    - user_id: 用户 ID
    - output_path: 输出路径（默认：~/fund-holdings-{user_id}.json）
    """
    holdings = load_holdings(user_id)
    if not holdings:
        return None
    
    if not output_path:
        output_path = Path.home() / f"fund-holdings-{user_id}.json"
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(holdings, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 持仓已导出：{output_path}")
    return output_path

def main():
    """测试功能"""
    print("=" * 60)
    print("用户持仓加密存储工具")
    print(f"时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # 1. 列出所有持仓
    list_holdings()
    
    # 2. 测试保存
    test_user = "test_user_001"
    test_holdings = {
        "user_id": test_user,
        "created_at": datetime.now().isoformat(),
        "funds": [
            {
                "code": "000001",
                "name": "易方达蓝筹精选",
                "amount": 100000,
                "cost_nav": 1.5,
                "current_nav": 1.3,
                "profit": -13333,
                "profit_rate": -13.33
            }
        ]
    }
    
    print(f"\n📝 测试保存持仓：{test_user}")
    save_holdings(test_user, test_holdings)
    
    # 3. 测试加载
    print(f"\n📝 测试加载持仓：{test_user}")
    loaded = load_holdings(test_user)
    if loaded:
        print(f"   基金数：{len(loaded.get('funds', []))}")
    
    # 4. 测试导出
    print(f"\n📝 测试导出持仓：{test_user}")
    export_holdings(test_user)
    
    # 5. 测试删除（注释掉，避免误删）
    # print(f"\n📝 测试删除持仓：{test_user}")
    # delete_holdings(test_user)
    
    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)

if __name__ == "__main__":
    main()
