#!/usr/bin/env python3
"""
Email Pro Optimized 技能自动提交推送脚本
修改代码后自动 commit 和 push 到 GitHub
"""

import subprocess
import sys
from pathlib import Path
from datetime import datetime

SKILL_DIR = Path.home() / '.openclaw' / 'skills' / 'email-pro-optimized'

def run_command(cmd, cwd=None):
    """运行命令"""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            cwd=cwd or SKILL_DIR,
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def check_git_status():
    """检查 git 状态"""
    print("🔍 检查 git 状态...\n")
    
    success, stdout, stderr = run_command("git status --porcelain")
    
    if not success:
        print("❌ 不是 git 仓库或 git 命令失败")
        return None
    
    if not stdout.strip():
        print("✅ 无需提交（工作区干净）")
        return []
    
    # 解析变化的文件
    changed_files = []
    for line in stdout.strip().split('\n'):
        if line:
            status = line[:2]
            filename = line[3:]
            changed_files.append((status, filename))
            print(f"  {status} {filename}")
    
    return changed_files

def stage_changes():
    """暂存所有变化"""
    print("\n📝 暂存变化...\n")
    
    success, stdout, stderr = run_command("git add -A")
    
    if success:
        print("✅ 所有变化已暂存")
        return True
    else:
        print(f"❌ 暂存失败: {stderr}")
        return False

def create_commit_message(changed_files):
    """生成提交信息"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # 统计变化类型
    added = sum(1 for s, _ in changed_files if s.startswith('A'))
    modified = sum(1 for s, _ in changed_files if s.startswith('M'))
    deleted = sum(1 for s, _ in changed_files if s.startswith('D'))
    
    message = f"🔄 Auto-update: {timestamp}\n\n"
    
    if modified > 0:
        message += f"✏️ Modified: {modified} file(s)\n"
    if added > 0:
        message += f"➕ Added: {added} file(s)\n"
    if deleted > 0:
        message += f"➖ Deleted: {deleted} file(s)\n"
    
    message += "\n📋 Changes:\n"
    for status, filename in changed_files:
        if status.startswith('M'):
            message += f"  ✏️ {filename}\n"
        elif status.startswith('A'):
            message += f"  ➕ {filename}\n"
        elif status.startswith('D'):
            message += f"  ➖ {filename}\n"
    
    message += f"\n🤖 Auto-committed by sync script"
    
    return message

def commit_changes(message):
    """提交变化"""
    print("\n💾 提交变化...\n")
    
    # 转义消息中的特殊字符
    escaped_message = message.replace('"', '\\"').replace('$', '\\$')
    
    success, stdout, stderr = run_command(f'git commit -m "{escaped_message}"')
    
    if success:
        print("✅ 提交成功")
        # 显示提交信息
        success, commit_info, _ = run_command("git log -1 --oneline")
        if success:
            print(f"   {commit_info.strip()}")
        return True
    else:
        print(f"❌ 提交失败: {stderr}")
        return False

def push_changes():
    """推送到远程"""
    print("\n🚀 推送到 GitHub...\n")
    
    # 获取当前分支
    success, branch, _ = run_command("git rev-parse --abbrev-ref HEAD")
    if not success:
        print("❌ 无法获取当前分支")
        return False
    
    branch = branch.strip()
    
    # 推送
    success, stdout, stderr = run_command(f"git push origin {branch}")
    
    if success:
        print(f"✅ 推送成功到 origin/{branch}")
        return True
    else:
        # 检查是否是因为没有上游分支
        if "no upstream branch" in stderr.lower() or "set-upstream" in stderr.lower():
            print(f"⚠️ 设置上游分支...")
            success, _, _ = run_command(f"git push -u origin {branch}")
            if success:
                print(f"✅ 推送成功到 origin/{branch}")
                return True
        
        print(f"❌ 推送失败: {stderr}")
        return False

def get_remote_url():
    """获取远程仓库 URL"""
    success, url, _ = run_command("git config --get remote.origin.url")
    if success:
        return url.strip()
    return None

def main():
    """主函数"""
    print("=" * 70)
    print("🔄 Email Pro Optimized 技能自动提交推送")
    print("=" * 70 + "\n")
    
    # 1. 检查 git 状态
    changed_files = check_git_status()
    
    if changed_files is None:
        return 1
    
    if not changed_files:
        print("\n✅ 无需更新")
        return 0
    
    # 2. 暂存变化
    if not stage_changes():
        return 1
    
    # 3. 创建提交信息
    message = create_commit_message(changed_files)
    
    # 4. 提交
    if not commit_changes(message):
        return 1
    
    # 5. 推送
    if not push_changes():
        print("\n⚠️ 推送失败，但本地提交已成功")
        return 1
    
    # 6. 显示结果
    print("\n" + "=" * 70)
    print("✨ 自动提交推送完成")
    print("=" * 70)
    
    remote_url = get_remote_url()
    if remote_url:
        print(f"\n📦 仓库: {remote_url}")
    
    print("\n📝 提交信息:")
    for line in message.split('\n'):
        print(f"   {line}")
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
