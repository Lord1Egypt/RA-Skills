#!/usr/bin/env python3
"""
ClawAPI Manager - 中央服务器 API Key 托管管理脚本
用法：
  python3 claw_api_manager_central.py list              # 列出所有 providers
  python3 claw_api_manager_central.py update <name> <key>  # 更新 API Key
  python3 claw_api_manager_central.py add <name> <url> <key> <protocol>  # 添加 provider
  python3 claw_api_manager_central.py remove <name>     # 删除 provider
  python3 claw_api_manager_central.py validate          # 验证配置
  python3 claw_api_manager_central.py fix               # 自动修复配置问题
  python3 claw_api_manager_central.py backup            # 手动备份
  python3 claw_api_manager_central.py restore <file>    # 从备份恢复
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib'))

from config_manager import ClawAPIConfigManager

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return
    
    mgr = ClawAPIConfigManager()
    cmd = sys.argv[1]
    
    if cmd == 'list':
        providers = mgr.list_providers()
        print('\n中央服务器的 Providers:')
        print('=' * 80)
        for i, p in enumerate(providers, 1):
            print(f"{i}. {p['name']}")
            print(f"   Protocol: {p['protocol']}")
            print(f"   URL: {p['base_url']}")
            print(f"   Key: {p['api_key']}")
            print(f"   Models: {p['model_count']}")
            print()
    
    elif cmd == 'update':
        if len(sys.argv) < 4:
            print("用法: update <provider_name> <new_api_key>")
            return
        
        provider_name = sys.argv[2]
        new_key = sys.argv[3]
        
        mgr.update_api_key(provider_name, new_key)
        print(f"✓ 已更新 {provider_name} 的 API Key")
        print("\n⚠️  记得重启 gateway:")
        print("  openclaw gateway restart")
    
    elif cmd == 'add':
        if len(sys.argv) < 6:
            print("用法: add <name> <base_url> <api_key> <protocol>")
            print("协议: anthropic-messages, openai-completions, openai-compatible")
            return
        
        name = sys.argv[2]
        base_url = sys.argv[3]
        api_key = sys.argv[4]
        protocol = sys.argv[5]
        
        mgr.add_provider(name, base_url, api_key, protocol=protocol)
        print(f"✓ 已添加 provider: {name}")
        print("\n⚠️  记得重启 gateway:")
        print("  openclaw gateway restart")
    
    elif cmd == 'remove':
        if len(sys.argv) < 3:
            print("用法: remove <provider_name>")
            return
        
        provider_name = sys.argv[2]
        mgr.remove_provider(provider_name)
        print(f"✓ 已删除 {provider_name}")
        print("\n⚠️  记得重启 gateway:")
        print("  openclaw gateway restart")
    
    elif cmd == 'validate':
        result = mgr.validate_config()
        if result['valid']:
            print('✓ 配置正常')
        else:
            print('⚠️  发现以下问题:')
            for i, issue in enumerate(result['issues'], 1):
                print(f"\n{i}. {issue['type']}")
                for k, v in issue.items():
                    if k != 'type':
                        print(f"   {k}: {v}")
            print("\n运行 'fix' 命令自动修复")
    
    elif cmd == 'fix':
        result = mgr.auto_fix()
        if result['fixed'] > 0:
            print(f"✓ 修复了 {result['fixed']} 个问题:")
            for fix in result['issues']:
                print(f"  - {fix}")
            print("\n⚠️  记得重启 gateway:")
            print("  openclaw gateway restart")
        else:
            print('✓ 没有需要修复的问题')
    
    elif cmd == 'backup':
        backup_file = mgr._backup()
        print(f"✓ 已备份到: {backup_file}")
    
    elif cmd == 'restore':
        if len(sys.argv) < 3:
            print("用法: restore <backup_file>")
            return
        
        backup_file = sys.argv[2]
        import shutil
        current_backup = mgr._backup()
        print(f"当前配置已备份到: {current_backup}")
        shutil.copy(backup_file, mgr.config_path)
        print(f"✓ 已从 {backup_file} 恢复")
        print("\n⚠️  记得重启 gateway:")
        print("  openclaw gateway restart")
    
    else:
        print(f"未知命令: {cmd}")
        print(__doc__)

if __name__ == '__main__':
    main()
