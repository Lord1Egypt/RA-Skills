#!/usr/bin/env python3
"""
版本管理工具
备份和回滚 Skill 版本
"""

import argparse
import json
import shutil
import sys
from pathlib import Path
from datetime import datetime


def get_current_version(base_dir, slug):
    """获取当前版本号"""
    meta_path = Path(base_dir) / slug / 'meta.json'
    if meta_path.exists():
        with open(meta_path, 'r', encoding='utf-8') as f:
            meta = json.load(f)
            return meta.get('version', 'v1')
    return 'v1'


def backup_version(base_dir, slug):
    """备份当前版本"""
    skill_path = Path(base_dir) / slug
    versions_path = skill_path / 'versions'
    
    if not skill_path.exists():
        print(f"Skill 不存在: {slug}", file=sys.stderr)
        return False
    
    # 获取当前版本号
    current_version = get_current_version(base_dir, slug)
    
    # 创建备份目录
    backup_path = versions_path / current_version
    backup_path.mkdir(parents=True, exist_ok=True)
    
    # 备份关键文件
    files_to_backup = ['SKILL.md', 'memory.md', 'persona.md', 'meta.json']
    for filename in files_to_backup:
        src = skill_path / filename
        if src.exists():
            shutil.copy2(src, backup_path / filename)
    
    # 记录备份信息
    backup_info = {
        'version': current_version,
        'backed_up_at': datetime.now().isoformat(),
        'files': files_to_backup
    }
    
    info_path = backup_path / 'backup_info.json'
    with open(info_path, 'w', encoding='utf-8') as f:
        json.dump(backup_info, f, ensure_ascii=False, indent=2)
    
    print(f"已备份版本 {current_version} 到 {backup_path}")
    return True


def rollback_version(base_dir, slug, version):
    """回滚到指定版本"""
    skill_path = Path(base_dir) / slug
    backup_path = skill_path / 'versions' / version
    
    if not backup_path.exists():
        print(f"版本不存在: {version}", file=sys.stderr)
        return False
    
    # 恢复文件
    files_to_restore = ['SKILL.md', 'memory.md', 'persona.md', 'meta.json']
    for filename in files_to_restore:
        src = backup_path / filename
        if src.exists():
            shutil.copy2(src, skill_path / filename)
    
    print(f"已回滚到版本 {version}")
    return True


def list_versions(base_dir, slug):
    """列出所有版本"""
    versions_path = Path(base_dir) / slug / 'versions'
    
    if not versions_path.exists():
        print(f"没有版本记录")
        return []
    
    versions = []
    for version_dir in versions_path.iterdir():
        if version_dir.is_dir():
            info_path = version_dir / 'backup_info.json'
            if info_path.exists():
                with open(info_path, 'r', encoding='utf-8') as f:
                    info = json.load(f)
                    versions.append({
                        'version': info.get('version'),
                        'backed_up_at': info.get('backed_up_at')
                    })
    
    return sorted(versions, key=lambda x: x['backed_up_at'])


def increment_version(base_dir, slug):
    """增加版本号"""
    meta_path = Path(base_dir) / slug / 'meta.json'
    
    if meta_path.exists():
        with open(meta_path, 'r', encoding='utf-8') as f:
            meta = json.load(f)
        
        current = meta.get('version', 'v1')
        # 解析版本号
        if current.startswith('v'):
            try:
                num = int(current[1:])
                new_version = f'v{num + 1}'
            except:
                new_version = 'v2'
        else:
            new_version = 'v2'
        
        meta['version'] = new_version
        meta['updated_at'] = datetime.now().isoformat()
        
        with open(meta_path, 'w', encoding='utf-8') as f:
            json.dump(meta, f, ensure_ascii=False, indent=2)
        
        return new_version
    
    return 'v1'


def main():
    parser = argparse.ArgumentParser(description='管理 Skill 版本')
    parser.add_argument('--action', required=True,
                       choices=['backup', 'rollback', 'list', 'increment'],
                       help='操作类型')
    parser.add_argument('--base-dir', default='./echoes', help='基础目录')
    parser.add_argument('--slug', required=True, help='Skill 标识符')
    parser.add_argument('--version', help='目标版本（用于 rollback）')
    
    args = parser.parse_args()
    
    if args.action == 'backup':
        backup_version(args.base_dir, args.slug)
    
    elif args.action == 'rollback':
        if not args.version:
            print("Error: --version is required for rollback", file=sys.stderr)
            sys.exit(1)
        rollback_version(args.base_dir, args.slug, args.version)
    
    elif args.action == 'list':
        versions = list_versions(args.base_dir, args.slug)
        
        if not versions:
            print(f"\n'{args.slug}' 没有版本记录")
            return
        
        print(f"\n'{args.slug}' 的版本历史:")
        print("-" * 50)
        for v in versions:
            print(f"  {v['version']:<10} {v['backed_up_at']}")
        print()
    
    elif args.action == 'increment':
        new_version = increment_version(args.base_dir, args.slug)
        print(f"版本已更新为: {new_version}")


if __name__ == '__main__':
    main()
