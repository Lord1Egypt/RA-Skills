#!/usr/bin/env python3
"""
Skill自动发布脚本
功能：
1. 发布Skill到ClawHub
2. 发布Skill到GitHub  
3. 生成抖音宣传文案
"""

import os
import sys
import json
import subprocess
import re
from datetime import datetime

CLAWHUB_CMD = "clawhub"
GITHUB_REPO_BASE = "https://github.com/chongjie-ran/"

def get_skill_info(skill_path):
    """读取Skill信息"""
    skill_md = os.path.join(skill_path, "SKILL.md")
    if not os.path.exists(skill_md):
        return None
    
    with open(skill_md, 'r') as f:
        content = f.read()
    
    # 解析name和description
    name_match = re.search(r'^name:\s*(.+)$', content, re.MULTILINE)
    desc_match = re.search(r'^description:\s*(.+)$', content, re.MULTILINE)
    
    return {
        "name": name_match.group(1).strip() if name_match else None,
        "description": desc_match.group(1).strip() if desc_match else None,
        "content": content
    }

def publish_to_clawhub(skill_name):
    """发布到ClawHub"""
    print(f"📦 发布到ClawHub: {skill_name}...")
    try:
        result = subprocess.run(
            [CLAWHUB_CMD, "publish", skill_name],
            capture_output=True,
            text=True,
            cwd=os.path.expanduser("~/.openclaw/workspace")
        )
        if result.returncode == 0:
            print(f"✅ ClawHub发布成功")
            return True
        else:
            print(f"⚠️ ClawHub发布失败: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ ClawHub发布异常: {e}")
        return False

def publish_to_github(skill_name, skill_path):
    """发布到GitHub"""
    print(f"📤 发布到GitHub: {skill_name}...")
    
    repo_name = f"skill-{skill_name}"
    local_path = skill_path
    
    try:
        # 初始化git（如果需要）
        if not os.path.exists(os.path.join(local_path, ".git")):
            subprocess.run(["git", "init"], cwd=local_path, check=True)
            subprocess.run(["git", "add", "."], cwd=local_path, check=True)
            subprocess.run(
                ["git", "commit", "-m", f"Add {skill_name} skill"],
                cwd=local_path, check=True
            )
        
        # 创建GitHub仓库并推送
        result = subprocess.run(
            ["gh", "repo", "create", repo_name, "--public", "--source", ".", "--push"],
            cwd=local_path,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print(f"✅ GitHub发布成功")
            return GITHUB_REPO_BASE + repo_name
        else:
            # 仓库可能已存在，尝试推送
            if "already exists" in result.stderr:
                subprocess.run(["git", "push", "origin", "main"], cwd=local_path, check=True)
                return GITHUB_REPO_BASE + repo_name
            print(f"⚠️ GitHub发布失败: {result.stderr}")
            return None
    except Exception as e:
        print(f"❌ GitHub发布异常: {e}")
        return None

def generate_douyin_post(skill_name, skill_info, clawhub_url=None, github_url=None):
    """生成抖音宣传文案"""
    name = skill_info.get("name", skill_name)
    description = skill_info.get("description", "")
    
    post = f"""🎉 新Skill发布！

【{name}】
📦 下载: {clawhub_url or "ClawHub搜索同名"}
💡 功能: {description}

📖 使用方法:
告诉SC"帮我创建一个{name}"即可

#AI #OpenClaw #Skill #{name}"""
    
    print("\n" + "="*50)
    print("📝 抖音宣传文案:")
    print("="*50)
    print(post)
    print("="*50)
    
    # 保存到文件
    output_file = f"~/.openclaw/workspace/memory/douyin-publish-{skill_name}-{datetime.now().strftime('%Y%m%d')}.md"
    with open(os.path.expanduser(output_file), 'w') as f:
        f.write(post)
    
    print(f"\n💾 已保存到: {output_file}")
    return post

def main(skill_name):
    """主函数"""
    skill_path = f"~/.openclaw/workspace/skills/{skill_name}"
    skill_path = os.path.expanduser(skill_path)
    
    if not os.path.exists(skill_path):
        print(f"❌ Skill不存在: {skill_name}")
        sys.exit(1)
    
    # 获取Skill信息
    skill_info = get_skill_info(skill_path)
    if not skill_info:
        print("❌ 无法读取Skill信息")
        sys.exit(1)
    
    print(f"🚀 开始发布Skill: {skill_name}")
    print(f"   描述: {skill_info.get('description', 'N/A')}")
    print()
    
    # 1. 发布到ClawHub
    clawhub_success = publish_to_clawhub(skill_name)
    clawhub_url = f"https://clawhub.com/skill/{skill_name}" if clawhub_success else None
    
    # 2. 发布到GitHub
    github_url = publish_to_github(skill_name, skill_path)
    
    # 3. 生成抖音宣传
    if clawhub_success or github_url:
        generate_douyin_post(skill_name, skill_info, clawhub_url, github_url)
        print("\n✅ 发布流程完成!")
    else:
        print("\n⚠️ 发布未完成，但已生成宣传文案")
        generate_douyin_post(skill_name, skill_info, None, None)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python publish_skill.py <skill-name>")
        sys.exit(1)
    
    main(sys.argv[1])
