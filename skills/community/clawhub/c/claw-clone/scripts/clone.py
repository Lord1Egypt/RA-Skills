#!/usr/bin/env python3
"""
claw-clone - 小龙虾克隆技能
🦞 一键导出/导入小龙虾配置
"""

import json
import os
import shutil
import sys
from datetime import datetime
from pathlib import Path

WORKSPACE = os.environ.get('OPENCLAW_WORKSPACE', '/home/node/.openclaw/workspace')
OPENCLAW_DIR = os.environ.get('OPENCLAW_DIR', '/home/node/.openclaw')

# ========== 导出功能 ==========

def read_file(filepath):
    """读取文件内容"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception:
        return None

def get_installed_skills():
    """获取已安装的skills列表"""
    skills_dir = Path(WORKSPACE) / 'skills'
    skills = []
    if skills_dir.exists():
        for item in skills_dir.iterdir():
            if item.is_dir() and not item.name.startswith('.'):
                meta_file = item / '_meta.json'
                if meta_file.exists():
                    try:
                        with open(meta_file, 'r', encoding='utf-8') as f:
                            meta = json.load(f)
                            skills.append({
                                'slug': meta.get('slug', item.name),
                                'version': meta.get('version', 'unknown')
                            })
                    except:
                        skills.append({'slug': item.name, 'version': 'unknown'})
                else:
                    skills.append({'slug': item.name, 'version': 'unknown'})
    return skills

def filter_sensitive(data):
    """过滤敏感信息"""
    sensitive_keys = ['apiKey', 'api_key', 'token', 'password', 'secret', 'credential', 'key']
    if isinstance(data, dict):
        result = {}
        for k, v in data.items():
            if any(s in k.lower() for s in sensitive_keys):
                result[k] = "[FILTERED]"
            else:
                result[k] = filter_sensitive(v)
        return result
    elif isinstance(data, list):
        return [filter_sensitive(item) for item in data]
    return data

def export_config():
    """导出OpenClaw配置（过滤敏感信息）"""
    config_path = Path(OPENCLAW_DIR) / 'openclaw.json'
    if config_path.exists():
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return filter_sensitive(json.load(f))
        except:
            return {"error": "Failed to read config"}
    return {}

def do_export(include_memory=False):
    """执行导出"""
    package = {
        "version": "1.0.0",
        "clonedAt": datetime.now().isoformat(),
        "identity": {},
        "config": {},
        "skills": [],
        "optional": {"includeMemory": include_memory}
    }
    
    # 身份文件
    identity_files = ['IDENTITY.md', 'SOUL.md', 'USER.md']
    for filename in identity_files:
        content = read_file(Path(WORKSPACE) / filename)
        if content:
            package['identity'][filename] = content
    
    # 配置文件
    config_files = ['AGENTS.md', 'HEARTBEAT.md', 'TOOLS.md']
    for filename in config_files:
        content = read_file(Path(WORKSPACE) / filename)
        if content:
            package['config'][filename] = content
    
    # Skills
    package['skills'] = get_installed_skills()
    
    # OpenClaw配置
    package['openclawConfig'] = export_config()
    
    # 记忆（可选）
    if include_memory:
        memory_content = read_file(Path(WORKSPACE) / 'MEMORY.md')
        if memory_content:
            package['memory'] = {'MEMORY.md': memory_content}
    
    return package

# ========== 导入功能 ==========

def backup_file(filepath):
    """备份现有文件"""
    if filepath.exists():
        backup_path = filepath.with_suffix(filepath.suffix + '.bak')
        shutil.copy2(filepath, backup_path)
        return str(backup_path)
    return None

def write_file(filepath, content):
    """写入文件"""
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

def install_skill(slug):
    """安装skill"""
    import subprocess
    try:
        result = subprocess.run(
            ['skillhub', 'install', slug],
            capture_output=True,
            text=True,
            timeout=60
        )
        return result.returncode == 0
    except:
        return False

def do_import(package_json):
    """执行导入"""
    try:
        package = json.loads(package_json)
    except json.JSONDecodeError as e:
        print(f"❌ JSON解析失败: {e}")
        return None
    
    results = {
        'identity': [],
        'config': [],
        'skills_installed': [],
        'skills_failed': [],
        'backups': []
    }
    
    # 导入身份文件
    for filename, content in package.get('identity', {}).items():
        filepath = Path(WORKSPACE) / filename
        backup = backup_file(filepath)
        if backup:
            results['backups'].append(backup)
        write_file(filepath, content)
        results['identity'].append(filename)
    
    # 导入配置文件
    for filename, content in package.get('config', {}).items():
        filepath = Path(WORKSPACE) / filename
        backup = backup_file(filepath)
        if backup:
            results['backups'].append(backup)
        write_file(filepath, content)
        results['config'].append(filename)
    
    # 安装skills
    skills = package.get('skills', [])
    for skill in skills:
        slug = skill.get('slug')
        if install_skill(slug):
            results['skills_installed'].append(slug)
        else:
            results['skills_failed'].append(slug)
    
    # 导入记忆
    if package.get('optional', {}).get('includeMemory', False):
        for filename, content in package.get('memory', {}).items():
            filepath = Path(WORKSPACE) / filename
            backup = backup_file(filepath)
            if backup:
                results['backups'].append(backup)
            write_file(filepath, content)
    
    return results

# ========== 主程序 ==========

def main():
    # 支持命令行参数: --export, --import, 或直接指定 JSON 文件
    if '--export' in sys.argv or '-e' in sys.argv:
        include_memory = '--include-memory' in sys.argv or '-m' in sys.argv
        package = do_export(include_memory)
        output = json.dumps(package, ensure_ascii=False, indent=2)
        
        print("=" * 60)
        print("🦞 安装包已生成，请复制以下内容：")
        print("=" * 60)
        print()
        print("---BEGIN_CLONE_PACKAGE---")
        print(output)
        print("---END_CLONE_PACKAGE---")
        print()
        print(f"已导出: {len(package['identity'])} 个身份文件, {len(package['config'])} 个配置文件, {len(package['skills'])} 个skills")
        return
    
    if '--import' in sys.argv or '-i' in sys.argv:
        # 从文件参数读取
        import_file = None
        for arg in sys.argv:
            if arg.endswith('.json'):
                import_file = arg
                break
        
        if import_file:
            with open(import_file, 'r') as f:
                package_json = f.read()
        else:
            print("❌ 请指定导入文件: --import <file.json>")
            return
        
        results = do_import(package_json)
        
        if not results:
            return
        
        print()
        print("=" * 60)
        print("✅ 导入完成!")
        print("=" * 60)
        print(f"📋 身份文件: {len(results['identity'])} 个")
        print(f"📋 配置文件: {len(results['config'])} 个")
        print(f"📦 Skills安装: {len(results['skills_installed'])} 个")
        if results['skills_failed']:
            print(f"⚠️ Skills失败: {', '.join([s['slug'] for s in results['skills_failed']])}")
        if results['backups']:
            print(f"💾 备份文件: {len(results['backups'])} 个")
        return
    
    # 交互模式
    print("=" * 60)
    print("🦞 小龙虾克隆工具 - 导出/导入一体化")
    print("=" * 60)
    print()
    print("请选择操作:")
    print("  [1] 导出 - 生成安装包分享给他人")
    print("  [2] 导入 - 使用安装包克隆")
    print()
    
    choice = input("请输入选项 (1/2): ").strip()
    
    if choice == '1':
        # 导出模式
        include_memory = '--include-memory' in sys.argv or '-m' in sys.argv
        
        package = do_export(include_memory)
        output = json.dumps(package, ensure_ascii=False, indent=2)
        
        print()
        print("=" * 60)
        print("🦞 安装包已生成，请复制以下内容：")
        print("=" * 60)
        print()
        print("---BEGIN_CLONE_PACKAGE---")
        print(output)
        print("---END_CLONE_PACKAGE---")
        print()
        print(f"已导出: {len(package['identity'])} 个身份文件, {len(package['config'])} 个配置文件, {len(package['skills'])} 个skills")
        if include_memory:
            print("已包含记忆文件")
        
    elif choice == '2':
        # 导入模式
        print()
        print("请粘贴安装包内容（包含 ---BEGIN_CLONE_PACKAGE--- 和 ---END_CLONE_PACKAGE---）:")
        print()
        
        lines = []
        in_package = False
        for line in sys.stdin:
            if '---BEGIN_CLONE_PACKAGE---' in line:
                in_package = True
                continue
            elif '---END_CLONE_PACKAGE---' in line:
                break
            elif in_package:
                lines.append(line)
        
        if not lines:
            print("❌ 未找到安装包内容")
            return
        
        package_json = ''.join(lines)
        results = do_import(package_json)
        
        if not results:
            return
        
        print()
        print("=" * 60)
        print("✅ 导入完成!")
        print("=" * 60)
        print(f"📋 身份文件: {len(results['identity'])} 个")
        print(f"📋 配置文件: {len(results['config'])} 个")
        print(f"📦 Skills安装: {len(results['skills_installed'])} 个")
        if results['skills_failed']:
            print(f"⚠️ Skills失败: {', '.join([s['slug'] for s in results['skills_failed']])}")
        if results['backups']:
            print(f"💾 备份文件: {len(results['backups'])} 个")
        print()
        print("⚠️ 注意: 部分配置可能需要重启生效")
        print("⚠️ 注意: API keys等敏感信息需要手动配置")
        
    else:
        print("❌ 无效选项")

if __name__ == '__main__':
    main()