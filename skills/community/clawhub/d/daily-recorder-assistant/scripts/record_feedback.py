#!/usr/bin/env python3
"""
record_feedback.py - 记录用户反馈到 Obsidian 笔记 (Append-only Mode v2.0)

功能:
- 读取现有笔记文件 → 追加/更新字段 → 写回（Append-only mode）
- 支持晨间记录 + 晚间复盘的分离写入
- **必须显式触发**才能执行写入，避免误操作
"""

import sys
import os
from datetime import datetime
import json
import re

SCRIPT_DIR = os.path.dirname(os.path.abspath(sys.argv[0]))
sys.path.insert(0, SCRIPT_DIR)
from config import CURRENT_SKILL_PATH, NOTE_BASE_DIR, DAILY_RECORDER_SUBDIR
STATE_FILE = os.path.join(CURRENT_SKILL_PATH, "state.json")
TEMPLATE_PATH = os.path.join(CURRENT_SKILL_PATH, "assets", "notes-template.md")

def load_state():
    if not os.path.exists(STATE_FILE):
        return {'total_records': 0}
    with open(STATE_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_state(state):
    with open(STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

def get_weekday_from_date(date):
    return date.weekday() + 1

def find_or_create_note_file():
    today = datetime.now().date()
    weekday_num = get_weekday_from_date(today)
    
    notes_dir = os.path.join(NOTE_BASE_DIR, DAILY_RECORDER_SUBDIR)
    os.makedirs(notes_dir, exist_ok=True)
    
    filename = f"{today.strftime('%Y-%m-%d')}-day_{weekday_num}.md"
    note_path = os.path.join(notes_dir, filename)
    
    if not os.path.exists(note_path):
        with open(note_path, 'w', encoding='utf-8') as f:
            f.write(f"# 交互记录 - {today.strftime('%Y-%m-%d')}（周{weekday_num}）\n\n")
    
    return note_path

def update_morning_fields(file_content, user_input):
    """更新早反馈字段（仅更新，不覆盖）"""
    content = file_content
    
    if user_input.get('early_feedback'):
        energy_val = user_input['early_feedback'].get('energy', '待评估')
        readiness_val = user_input['early_feedback'].get('readiness', '待确认')
        
        # 替换休息质量
        if isinstance(energy_val, int):
            content = re.sub(r'\*\*休息质量\*\*: \[.*?\]', f'**休息质量**: [{energy_val}]', content)
        
        # 替换就绪状态  
        content = re.sub(r'\*\*就绪状态\*\*: .*?$', f"**就绪状态**: {readiness_val}", content, count=1, flags=re.MULTILINE)
    
    print("✅ 已更新早反馈字段（仅更新，不覆盖原有数据）")
    return content

def update_evening_fields(file_content, user_input):
    """更新晚复盘字段（仅更新，不覆盖）"""
    content = file_content
    
    # 1. 更新完成度字段
    if user_input.get('completion_rates') and len(user_input['completion_rates']) > 0:
        new_completion_lines = "### 完成度\n\n"
        for task, rate in user_input['completion_rates'].items():
            if isinstance(rate, int):
                new_completion_lines += f"- **{task}**: [{rate}] %\n"
            else:
                new_completion_lines += f"- **{task}**: [{rate}%]\n"
        
        content = re.sub(r'### 完成度[\\s\\S]*?(?=### 能量状态)', new_completion_lines + "\n", content, flags=re.DOTALL)
    
    # 2. 更新能量评分和时段分析
    if user_input.get('energy_score'):
        energy_val = user_input['energy_score']
        new_energy_line = f"### 能量状态\n- **评分**: [{energy_val}] (1=极累，3=正常，5=充沛)"
        
        content = re.sub(r'### 能量状态[\\s\\S]*?(?=### 遇到的问题)', new_energy_line, content, flags=re.DOTALL)
    
    # 3. 更新时段分析
    if user_input.get('time_analysis'):
        time_analysis = user_input['time_analysis']
        new_time_lines = f"- **上午**: {time_analysis.get('morning', '待补充')}\n" \
                        f"- **下午**: {time_analysis.get('afternoon', '待补充')}\n" \
                        f"- **晚上**: {time_analysis.get('evening', '待补充')}"
        
        content = re.sub(r'### 能量状态[\\s\\S]*?(?=### 遇到的问题)', 
                        f"### 能量状态\n{new_time_lines}", 
                        content, flags=re.DOTALL)
    
    # 4. 更新遇到的问题
    if user_input.get('barriers'):
        new_problems_lines = "### 遇到的问题\n\n"
        for barrier in user_input['barriers']:
            if isinstance(barrier, str):
                new_problems_lines += f"- {barrier}\n"
        
        content = re.sub(r'### 遇到问题[\\s\\S]*?(?=### 计划偏差度)', new_problems_lines + "\n", content, flags=re.DOTALL)
    
    # 5. 更新计划偏差度
    if user_input.get('plan_deviation'):
        deviation_info = user_input['plan_deviation']
        
        new_deviation_lines = f"### 计划偏差度\n\n- **原计划**: {deviation_info.get('original_plan', '待补充')}\n"
        new_deviation_lines += "- **实际执行**:\n"
        for item in deviation_info.get('actual_execution', []):
            if isinstance(item, str):
                new_deviation_lines += f"  - {item}\n"
        new_deviation_lines += f"- **偏差原因**: {deviation_info.get('cause', '待补充')}"
        
        content = re.sub(r'### 计划偏差度[\\s\\S]*?(?=##)', new_deviation_lines + "\n", content, flags=re.DOTALL)
    
    print("✅ 已更新晚复盘字段（仅更新，不覆盖原有数据）")
    return content

def append_appendix_note(file_content, user_input):
    """追加附录内容"""
    if user_input.get('appendix_notes'):
        notes = "\n".join(user_input['appendix_notes'])
        content = file_content.rstrip() + f"\n\n---\n\n## 附录：{datetime.now().strftime('%H:%M')}补充记录\n{notes}\n"
    print("✅ 已追加附录内容")
    return content

def write_note_to_file(content, note_path):
    with open(note_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    state = load_state()
    state['total_records'] += 1
    save_state(state)
    
    print(f"✓ 笔记已更新：{note_path}")

def main(mode='morning', user_input=None):
    """主流程 - Append-only Mode"""
    
    print("=== 记录反馈到 Obsidian (Append-only Mode) ===")
    print(f"模式：{mode}")
    if user_input:
        for key, val in user_input.items():
            print(f"  {key}: {val}")
    
    try:
        note_path = find_or_create_note_file()
        
        with open(note_path, 'r', encoding='utf-8') as f:
            file_content = f.read()
        
        original_content = file_content
        
        if mode == 'morning' and user_input:
            file_content = update_morning_fields(file_content, user_input)
        elif mode == 'evening' and user_input:
            file_content = update_evening_fields(file_content, user_input)
        elif mode == 'appendix' and user_input:
            file_content = append_appendix_note(file_content, user_input)
        else:
            print("⚠️ 模式或输入为空，跳过更新")
            return False
        
        write_note_to_file(file_content, note_path)
        
        return True
    
    except Exception as e:
        print(f"❌ 错误：{str(e)}")
        print("⚠️ 已回滚到原始内容，未保存更改")
        with open(note_path, 'w', encoding='utf-8') as f:
            f.write(original_content)
        return False

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="记录反馈到 Obsidian (Append-only Mode)")
    parser.add_argument('--mode', choices=['morning', 'evening'], default='auto')
    
    args = parser.parse_args()
    
    sample_input_evening = {
        'completion_rates': {'文案/大纲生成': 80, '润色优化': 50},
        'energy_score': 5,
        'time_analysis': {
            'morning': "专注高效，完成原文全通读",
            'afternoon': "深度加工 AI 初稿",
            'evening': "状态饱满"
        },
        'barriers': ["核心洞察：AI 提取的关键词需人工深加工"],
        'plan_deviation': {
            'original_plan': "完成文案初稿",
            'actual_execution': ["✅ 原文第十章 100% 读完"],
            'cause': "优先保证原文全通读"
        }
    }
    
    if args.mode == 'evening':
        main(mode='evening', user_input=sample_input_evening)
