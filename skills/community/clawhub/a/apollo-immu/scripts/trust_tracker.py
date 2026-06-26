#!/usr/bin/env python3
"""
trust_tracker.py - 追踪和管理信任分数

用法：
  python3 trust_tracker.py update <收件人> <操作类型>
  python3 trust_tracker.py get <收件人>
  python3 trust_tracker.py list
  python3 trust_tracker.py reset <收件人>
  python3 trust_tracker.py reset-all

示例：
  python3 trust_tracker.py update user:ou_xxx delete
  python3 trust_tracker.py get user:ou_xxx
  python3 trust_tracker.py list
  python3 trust_tracker.py reset user:ou_xxx
"""

import json
import sys
import os
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPT_DIR)
TRUST_DB = os.path.join(SKILL_DIR, 'assets', 'trust_db.json')

def load_trust_db():
    """加载信任数据库"""
    if os.path.exists(TRUST_DB):
        with open(TRUST_DB, 'r') as f:
            return json.load(f)
    return {"contacts": {}}

def save_trust_db(db):
    """保存信任数据库"""
    os.makedirs(os.path.dirname(TRUST_DB), exist_ok=True)
    with open(TRUST_DB, 'w') as f:
        json.dump(db, f, ensure_ascii=False, indent=2)

def update_trust(recipient, operation_type):
    """增加信任次数"""
    db = load_trust_db()
    
    if 'contacts' not in db:
        db['contacts'] = {}
    
    if recipient not in db['contacts']:
        db['contacts'][recipient] = {}
    
    if operation_type not in db['contacts'][recipient]:
        db['contacts'][recipient][operation_type] = {
            "count": 0,
            "lastConfirm": None
        }
    
    db['contacts'][recipient][operation_type]['count'] += 1
    db['contacts'][recipient][operation_type]['lastConfirm'] = datetime.now().isoformat()
    
    save_trust_db(db)
    
    new_count = db['contacts'][recipient][operation_type]['count']
    auto_allow = new_count >= 3
    status = "已达到自动放行阈值(3次)" if auto_allow else f"当前次数:{new_count}/3"
    
    print(f"✅ 信任更新 | 收件人:{recipient} | 操作:{operation_type} | {status}")
    return new_count

def get_trust(recipient):
    """获取收件人信任状态"""
    db = load_trust_db()
    
    if 'contacts' not in db or recipient not in db['contacts']:
        print(f"📋 信任记录 | 收件人:{recipient} | 无记录")
        return None
    
    contacts = db['contacts'][recipient]
    print(f"📋 信任记录 | 收件人:{recipient}")
    
    total = 0
    for op_type, data in contacts.items():
        count = data.get('count', 0)
        last = data.get('lastConfirm', 'N/A')
        total += count
        print(f"   - {op_type}: {count}次 (最后确认:{last})")
    
    print(f"   总确认次数: {total}")
    return contacts

def list_all():
    """列出所有收件人信任状态"""
    db = load_trust_db()
    
    if 'contacts' not in db or not db['contacts']:
        print("📋 无任何信任记录")
        return
    
    print(f"📋 信任数据库 | 共 {len(db['contacts'])} 个收件人")
    print("-" * 50)
    
    for recipient, operations in db['contacts'].items():
        total = sum(v.get('count', 0) for v in operations.values())
        print(f"{recipient}: {total}次确认")
        for op_type, data in operations.items():
            count = data.get('count', 0)
            status = "✅ 已自动放行" if count >= 3 else f"({count}/3)"
            print(f"   - {op_type}: {status}")

def reset_trust(recipient):
    """重置收件人信任"""
    db = load_trust_db()
    
    if 'contacts' in db and recipient in db['contacts']:
        del db['contacts'][recipient]
        save_trust_db(db)
        print(f"🔄 已重置 | 收件人:{recipient}")
    else:
        print(f"⚠️ 无记录 | 收件人:{recipient}")

def reset_all():
    """重置所有信任"""
    save_trust_db({"contacts": {}})
    print("🔄 已重置所有信任记录")

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'update':
        if len(sys.argv) < 4:
            print("用法: update <收件人> <操作类型>")
            sys.exit(1)
        update_trust(sys.argv[2], sys.argv[3])
    
    elif command == 'get':
        if len(sys.argv) < 3:
            print("用法: get <收件人>")
            sys.exit(1)
        get_trust(sys.argv[2])
    
    elif command == 'list':
        list_all()
    
    elif command == 'reset':
        if len(sys.argv) < 3:
            print("用法: reset <收件人>")
            sys.exit(1)
        reset_trust(sys.argv[2])
    
    elif command == 'reset-all':
        confirm = input("确认重置所有信任记录？(y/N): ")
        if confirm.lower() == 'y':
            reset_all()
        else:
            print("已取消")
    
    else:
        print(f"未知命令: {command}")
        print(__doc__)
        sys.exit(1)

if __name__ == '__main__':
    main()
