#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Agency Agents Caller - Installation Verification
验证安装是否成功
"""

import os
import sys
import sqlite3
from typing import List, Dict

def check_python_version():
    """检查Python版本"""
    print("[PYTHON] Checking Python version...")
    
    version = sys.version_info
    print(f"  Current: {version.major}.{version.minor}.{version.micro}")
    
    if version.major >= 3 and version.minor >= 6:
        print("  [OK] Python version OK (>= 3.6)")
        return True
    else:
        print("  [ERROR] Python version too old (need >= 3.6)")
        return False

def check_directory_structure():
    """检查目录结构"""
    print("\n[DIR] Checking directory structure...")
    
    required_dirs = [
        'memory',
        'memory/database',
        'scripts',
        'examples'
    ]
    
    all_ok = True
    for directory in required_dirs:
        if os.path.exists(directory):
            print(f"  [OK] {directory}")
        else:
            print(f"  [ERROR] {directory} (missing)")
            all_ok = False
    
    return all_ok

def check_database_file():
    """检查数据库文件"""
    print("\n[DB] Checking database file...")
    
    db_path = os.path.join('memory', 'database', 'xiaozhi_memory.db')
    
    if not os.path.exists(db_path):
        print(f"  [ERROR] Database file not found: {db_path}")
        print(f"  [INFO] Run: python scripts/init_database.py")
        return False
    
    print(f"  [OK] Database file exists: {db_path}")
    
    # 检查文件大小
    size = os.path.getsize(db_path)
    print(f"  [INFO] File size: {size} bytes")
    
    if size < 1000:
        print(f"  [WARN] Database seems empty or corrupted")
        return False
    
    return True

def check_database_structure():
    """检查数据库结构"""
    print("\n[CHECK] Checking database structure...")
    
    db_path = os.path.join('memory', 'database', 'xiaozhi_memory.db')
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 检查表是否存在
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        required_tables = ['agent_prompts']
        all_ok = True
        
        for table in required_tables:
            if table in tables:
                print(f"  [OK] Table: {table}")
            else:
                print(f"  [ERROR] Table: {table} (missing)")
                all_ok = False
        
        # 检查索引
        cursor.execute("SELECT name FROM sqlite_master WHERE type='index'")
        indexes = [row[0] for row in cursor.fetchall()]
        
        print(f"  [INFO] Indexes: {len(indexes)}")
        
        # 检查Agent数量
        cursor.execute("SELECT COUNT(*) FROM agent_prompts")
        agent_count = cursor.fetchone()[0]
        print(f"  [INFO] Agents: {agent_count}")
        
        if agent_count == 0:
            print(f"  [WARN] No agents in database")
            print(f"  [INFO] Please import agents from agency-agents repository")
        
        conn.close()
        
        return all_ok
        
    except Exception as e:
        print(f"  [ERROR] Error checking database: {e}")
        return False

def check_agent_caller_module():
    """检查agent_caller模块"""
    print("\n[MODULE] Checking agent_caller module...")
    
    try:
        # 添加scripts目录到路径
        scripts_dir = os.path.join(os.path.dirname(__file__), 'scripts')
        if scripts_dir not in sys.path:
            sys.path.insert(0, scripts_dir)
        
        from agent_caller import AgentCaller
        
        print("  [OK] agent_caller module imported")
        
        # 尝试初始化
        caller = AgentCaller()
        
        # 测试基本操作
        categories = caller.get_categories()
        print(f"  [OK] Categories: {len(categories)}")
        
        agent_count = caller.count_agents()
        print(f"  [INFO] Total agents: {agent_count}")
        
        return True
        
    except ImportError as e:
        print(f"  [ERROR] Cannot import agent_caller: {e}")
        return False
    except Exception as e:
        print(f"  [ERROR] Error testing agent_caller: {e}")
        return False

def check_required_files():
    """检查必需文件"""
    print("\n[FILES] Checking required files...")
    
    required_files = [
        'SKILL.md',
        'README.md',
        'package.json',
        'scripts/agent_caller.py',
        'examples/usage_demo.py'
    ]
    
    all_ok = True
    for file_path in required_files:
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            print(f"  [OK] {file_path} ({size} bytes)")
        else:
            print(f"  [ERROR] {file_path} (missing)")
            all_ok = False
    
    return all_ok

def main():
    """主函数"""
    print("="*70)
    print("Agency Agents Caller - Installation Verification")
    print("="*70)
    print()
    
    # 运行所有检查
    checks = [
        ("Python Version", check_python_version),
        ("Directory Structure", check_directory_structure),
        ("Required Files", check_required_files),
        ("Database File", check_database_file),
        ("Database Structure", check_database_structure),
        ("Agent Caller Module", check_agent_caller_module)
    ]
    
    results = {}
    for name, check_func in checks:
        try:
            results[name] = check_func()
        except Exception as e:
            print(f"\n[ERROR] Error in {name}: {e}")
            results[name] = False
    
    # 总结
    print("\n" + "="*70)
    print("Verification Summary")
    print("="*70)
    print()
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for name, result in results.items():
        status = "[PASS]" if result else "[FAIL]"
        print(f"  {status} {name}")
    
    print()
    print(f"[RESULT] Result: {passed}/{total} checks passed")
    print()
    
    if passed == total:
        print("[SUCCESS] All checks passed! Installation is successful.")
        print()
        print("[READY] You can now use the agent caller:")
        print("  from scripts.agent_caller import AgentCaller")
        print("  caller = AgentCaller()")
        print()
        return 0
    else:
        print("[WARNING] Some checks failed. Please review the errors above.")
        print()
        print("[FIX] Common fixes:")
        print("  - Run: python scripts/init_database.py")
        print("  - Check: Python version >= 3.6")
        print("  - Import: Import agents from agency-agents repository")
        print()
        return 1

if __name__ == "__main__":
    sys.exit(main())
