#!/usr/bin/env python3
"""
plan_next_day.py - 规划次日计划

功能:
- 根据当前模式（人工/智能）生成明日计划模板
- 第 1 周期：仅记录用户输入
- 第 N+1 周期 (N≥2): 基于历史数据生成优化建议
"""

import sys
import os
from datetime import datetime, timedelta
import json
# 动态添加当前脚本所在目录到 Python 路径
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from config import  CURRENT_SKILL_PATH
STATE_FILE = os.path.join(CURRENT_SKILL_PATH, "state.json")
PLAN_TEMPLATE_PATH = os.path.join(CURRENT_SKILL_PATH, "assets", "plan-template.md")

def load_state():
    """读取状态文件"""
    if not os.path.exists(STATE_FILE):
        raise RuntimeError("状态文件不存在")
    
    with open(STATE_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_weekday_from_date(date):
    """获取周 Day (周一=1, 周日=7)"""
    weekday_num = date.weekday() + 1 if date.weekday() != 0 else 7
    return weekday_num

def load_template():
    """加载计划模板"""
    with open(PLAN_TEMPLATE_PATH, 'r', encoding='utf-8') as f:
        return f.read()

def generate_manual_plan(user_input):
    """第 1 周期人工模式 - 仅记录用户输入"""
    
    today = datetime.now().date()
    next_day = today + timedelta(days=1)
    weekday_num = get_weekday_from_date(next_day)
    state = load_state()
    
    template = load_template()
    content = (template
               .replace("{{date}}", next_day.strftime('%Y-%m-%d'))
               .replace("{{day_of_week}}", str(weekday_num))
               .replace("{{cycle_number}}", str(state['current_cycle'])))
    
    # 填入用户提供的计划内容
    if user_input.get('tasks'):
        for i, task in enumerate(user_input['tasks'], 1):
            placeholder = f"## 今日核心任务\n\n### {i}. [主要任务名称]"
            content = content.replace(placeholder, 
                                      f"## 今日核心任务\n\n### {i}. {task['name']}", 1)
            if task.get('goal'):
                content = content.replace("**目标**: [具体可衡量产出]", 
                                          f"**目标**: {task['goal']}")
            if task.get('ai_assist'):
                content = content.replace("**AI 辅助环节**: [哪些部分可由 AI 生成/协助]", 
                                          f"**AI 辅助环节**: {task['ai_assist']}")
    
    # 能量适配建议（第 1 周期仅提示用户）
    if user_input.get('energy_note'):
        content = content.replace("基于前{{cycle_number}}周平均能量状态...内容", 
                                  f"当前能量状态反馈：{user_input['energy_note']}")
    
    return content

def generate_smart_plan(history_data):
    """第 N+1 周期智能模式 - 基于历史数据生成优化建议"""
    
    today = datetime.now().date()
    next_day = today + timedelta(days=1)
    weekday_num = get_weekday_from_date(next_day)
    state = load_state()
    
    # 当前周期数
    current_cycle = state['current_cycle']
    
    template = load_template()
    content = (template
               .replace("{{date}}", next_day.strftime('%Y-%m-%d'))
               .replace("{{day_of_week}}", str(weekday_num))
               .replace("{{cycle_number}}", str(current_cycle)))
    
    # 基于历史模式生成推荐
    
    # A. 任务分配优化
    if history_data.get('task_adaptation'):
        for i, recommended_task in enumerate(history_data['task_adaptation'], 1):
            placeholder = f"### {i}. [主要任务名称]"
            content = content.replace(placeholder, 
                                      f"### {i}. {recommended_task['name']}", 1)
            if recommended_task.get('priority'):
                content = content.replace("**优先级**: [高/中/低]", 
                                          f"**优先级**: {recommended_task['priority']}")
    
    # B. 时间窗建议（智能模式注入）
    time_window_hint = history_data.get('best_start_window')
    if time_window_hint:
        # 在模板末尾追加
        content += (f"\n---\n**智能建议**: 建议在{time_window_hint}开始，该时段历史效率最高")
    
    # C. 风险预警（基于障碍模式识别）
    risk_alerts = history_data.get('risk_alerts')
    if risk_alerts:
        alert_section = "## 潜在风险预警\n根据历史问题模式识别："
        for alert in risk_alerts:
            content += (f"\n{alert_section}\n- {alert['barrier_type']} → 应对策略：{alert['strategy']}")
            alert_section = ""  # 后续条目不重复标题
    
    return content

def main(mode="manual", user_input=None, history_data=None):
    """主流程"""
    
    state = load_state()
    
    if mode == "manual":
        if not user_input:
            raise ValueError("人工模式需要提供用户输入")
        
        print("=== 第{{state['current_cycle']}}周期 - 人工规划模式 ===")
        content = generate_manual_plan(user_input)
    
    elif mode == "smart":
        if state['current_cycle'] < 2:
            raise RuntimeError(f"当前周期 {state['current_cycle']} < 2，不支持智能模式")
        
        if not history_data:
            raise ValueError("智能模式需要提供历史数据分析结果")
        
        print("=== 第{{state['current_cycle']}}周期 - 智能进化模式 ===")
        content = generate_smart_plan(history_data)
    
    else:
        raise ValueError("未知模式")
    
    # 输出计划内容（简化：仅打印）
    print(content[:2000])  # 截断展示

if __name__ == "__main__":
    # 示例测试（人工模式）
    sample_input = {
        'tasks': [
            {'name': "大纲 AI 生成", 'goal': "完成 5000 字初稿", 'ai_assist': "使用 LLM 生成框架"},
            {'name': "润色优化", 'goal': "提升可读性与逻辑连贯性", 'priority': "高"}
        ],
        'energy_note': "今日能量评分 3，建议下午进行创造性工作"
    }
    
    main("manual", user_input=sample_input)
