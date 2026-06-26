#!/usr/bin/env python3
"""
Daily Profile Update - 生成画像并注入到 system prompt
自动运行，每日更新用户画像到 SOUL.md
"""

import json
import os
from datetime import datetime
from pathlib import Path

# 路径配置
OPENCLAW_DIR = Path(os.environ.get("OPENCLAW_DIR", str(Path.home() / ".openclaw")))
WORKSPACE = Path(os.environ.get("OPENCLAW_WORKSPACE", str(OPENCLAW_DIR / "workspace")))
SKILL_DIR = Path(__file__).parent.parent
SOUL_FILE = WORKSPACE / "SOUL.md"
PROFILE_FILE = SKILL_DIR / "data" / "user-profile.json"
ADVISOR_PROMPT_FILE = SKILL_DIR / "scripts" / "advisor_prompt.txt"

def load_profile():
    """加载用户画像"""
    if PROFILE_FILE.exists():
        with open(PROFILE_FILE, 'r') as f:
            return json.load(f)
    return {}

def generate_advisor_prompt(profile):
    """生成 advisor prompt"""
    comm = profile.get('communication', {})
    work = profile.get('work_style', {})
    learning = profile.get('learning_mode', {})
    patterns = profile.get('patterns', {})
    preferences = profile.get('preferences', {})
    
    prompt = f"""【用户画像】 - 更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}
- 沟通风格: {comm.get('style', 'direct')}
- 活跃时间: {comm.get('active_hours', 'unknown')}
- 工作风格: {work.get('planning', 'adaptive')}, {work.get('execution', 'prototype_first')}
- 学习方式: {learning.get('approach', 'concept_oriented')}
- 雷区: {', '.join(patterns.get('abandonment_triggers', []))}

【回复建议】
1. 简洁直接，不要废话
2. 如果要提醒的事已提醒过，直接执行，不要再说
3. 遇到问题先给替代方案
4. 晚间回复可以稍长一点（他有更多时间）
5. 新任务先给原型
"""
    return prompt

def inject_to_soul(prompt):
    """注入到 SOUL.md"""
    if not SOUL_FILE.exists():
        print(f"SOUL.md not found at {SOUL_FILE}")
        return False
    
    with open(SOUL_FILE, 'r') as f:
        content = f.read()
    
    # 检查是否已有画像块
    marker_start = "<!-- USER_PROFILE_START -->"
    marker_end = "<!-- USER_PROFILE_END -->"
    
    if marker_start in content and marker_end in content:
        # 替换现有块
        import re
        pattern = f"{marker_start}.*?{marker_end}"
        new_block = f"{marker_start}\n{prompt}\n{marker_end}"
        content = re.sub(pattern, new_block, content, flags=re.DOTALL)
    else:
        # 添加到文件末尾
        content += f"\n\n{marker_start}\n{prompt}\n{marker_end}\n"
    
    with open(SOUL_FILE, 'w') as f:
        f.write(content)
    
    return True

def main():
    print(f"[{datetime.now().isoformat()}] Starting daily profile update...")
    
    # 1. 生成/更新画像
    profile = load_profile()
    if not profile:
        print("No profile found, run collector.py first")
        return
    
    # 2. 生成 advisor prompt
    prompt = generate_advisor_prompt(profile)
    
    # 3. 保存 prompt 文件
    with open(ADVISOR_PROMPT_FILE, 'w') as f:
        f.write(prompt)
    
    # 4. 注入到 SOUL.md
    if inject_to_soul(prompt):
        print(f"✅ Profile injected to SOUL.md")
    else:
        print(f"❌ Failed to inject profile")
    
    print(f"[{datetime.now().isoformat()}] Daily profile update complete")

if __name__ == "__main__":
    main()
