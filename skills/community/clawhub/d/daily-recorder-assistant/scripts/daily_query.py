#!/usr/bin/env python3
"""
daily_query.py - 根据当前状态生成个性化问询

功能:
- 读取昨日记录获取关键信息 (能量评分、计划内容)
- 确定当前周 Day
- 从模板库选择对应模板并注入变量
- 输出最终问询文本
"""

import sys
import os
from datetime import datetime, timedelta
import json
import re
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from config import CURRENT_SKILL_PATH, NOTE_BASE_DIR, DAILY_RECORDER_SUBDIR, REFERENCE_DIR
STATE_FILE = os.path.join(CURRENT_SKILL_PATH, "state.json")

# 支持频道列表 (用于 cron 配置)
SUPPORTED_CHANNELS = [
    "feishu", "telegram", "signal", "discord", "slack",
    "whatsapp", "qqbot", "imessage", "line", "zalo",
    "mattermost", "matrix", "nextcloud-talk", "msteams"
]

# 语言模板映射
LANGUAGE_MAP = {
    "zh": os.path.join(REFERENCE_DIR, "interaction-templates-zh.md"),
    "en": os.path.join(REFERENCE_DIR, "interaction-templates-en-full.md"),  # 英文完整版
    "auto": None
}

TRIGGER_WORDS = {
    # 晨间问询触发词（支持多种变体）
    "morning": [
        "早上问询", "早问询",
        "早反馈",  # 新增：cron 发送的关键词
        "morning query", "morning check"
    ],
    # 晚间复盘触发词（支持多种变体）
    "evening": [
        "晚上复盘", "晚问询",
        "晚复盘",  # 新增：cron 发送的关键词
        "evening review", "evening summary"
    ],
    # 状态查询触发词
    "status_query": ["状态查询", "每日记录状态", "status query", "daily record status"]
}

def detect_trigger(user_message, time_period=None):
    if user_message:
        msg_lower = user_message.lower()
        for period, words in TRIGGER_WORDS.items():
            if any(word in msg_lower for word in words):
                return period
        # 检测状态查询触发词 → 返回特殊模式
        status_triggers = ["status query", "daily record status", "状态查询", "每日记录状态"]
        if any(w in msg_lower for w in status_triggers):
            return "status_query"
        return time_period or "morning"
    return time_period or "morning"


def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        return {
            'current_cycle': 1,
            'active_channel': None,
            'user_id_by_channel': {},
            'chat_name_by_channel': {},
            'user_nickname': None
        }


def get_weekday_from_date(date):
    # Monday=0, Sunday=6 (Python datetime)
    # Convert to Chinese convention: Monday=1, Sunday=7
    if date.weekday() == 6:  # Sunday
        return 7
    else:
        return date.weekday() + 1


def get_day_name(weekday_num):
    """将周几数字转换为中文名称"""
    day_names = {
        1: '周一',
        2: '周二',
        3: '周三',
        4: '周四',
        5: '周五',
        6: '周六',
        7: '周日'
    }

    return day_names.get(weekday_num, f"周{weekday_num}")


def find_yesterday_note():
    """查找昨日笔记内容"""
    
    yesterday = datetime.now().date() - timedelta(days=1)
    weekday_num = get_weekday_from_date(yesterday)
    filename = f"{yesterday.strftime('%Y-%m-%d')}-day_{weekday_num}.md"
    notes_dir = os.path.join(NOTE_BASE_DIR, DAILY_RECORDER_SUBDIR)
    
    note_path = os.path.join(notes_dir, filename)
    
    if not os.path.exists(note_path):
        return None
    
    with open(note_path, 'r', encoding='utf-8') as f:
        return f.read()


def extract_energy_from_note(content):
    """从笔记内容提取能量评分"""
    if not content:
        return None
    
    import re
    # 匹配「评分]: [X]」格式
    match = re.search(r'\*\*评分\*\*:\s*\[(\d+)', content)
    if match:
        return int(match.group(1))
    
    # 匹配「能量状态：[X]」格式（晚复盘）
    match = re.search(r'能量状态：\[([^\]]+)\]', content)
    if match:
        try:
            return int(match.group(1))
        except ValueError:
            return None
    
    return None


def extract_task_info_from_note(content):
    """从笔记内容提取任务信息"""
    if not content:
        return None
    
    # 匹配「当日任务确认」字段
    import re
    match = re.search(r'\*\*当日任务确认\*\*:\s*(.+?)(?:\n|\n\n)', content)
    if match:
        task_text = match.group(1).strip()
        return task_text
    
    # 匹配「今日计划」相关字段（晚复盘）
    match = re.search(r'\*\*今日计划\*\*:?\s*(.+?)(?:\n|\n\n)', content)
    if match:
        return match.group(1).strip()
    
    return None


def select_template_for_time(time_period, weekday_num, current_cycle):
    """根据时间周期 + 周 Day + 周期数选择模板名称"""

    if time_period == "morning":
        templates_by_weekday = {
            1: "Monday Morning Template",
            2: "Tuesday Morning Template",
            3: "Wednesday Morning Template",
            4: "Thursday Morning Template",
            5: "Friday Morning Template (周五早 - 收尾鼓励式)",
            6: "Saturday Morning Template",
            7: "Sunday Morning Template"
        }

        selected = templates_by_weekday.get(weekday_num)

        # 【修复】第 1 周期使用标准关怀式模板；第 2+周期可根据需要选择 Data-Driven
        # 默认：始终返回对应周几的标准模板，保持关怀风格
        return selected

    elif time_period == "evening":
        templates_by_weekday = {
            1: "Monday Evening Template",
            2: "Tuesday Evening Template",
            3: "Wednesday Evening Template",
            4: "Thursday Evening Template",
            5: "Friday Evening Template",
            6: "Saturday Evening Template",
            7: "Sunday Night Template"
        }

        return templates_by_weekday.get(weekday_num) or templates_by_weekday[1]

    else:
        raise ValueError("未知时间周期")


def inject_variables(template_content, state_data, yesterday_data):
    replacements = {
        "{{last_night_energy}}": str(yesterday_data.get('energy_score', '待评估')),
        "{{avg_energy_m1_m2}}": "N/A",
        "{{common_barrier_type}}": "未识别",
        "{{cycle_number}}": str(state_data['current_cycle']),
        "{{avg_energy_day}}": "历史数据中",
        "{{plan_completion_pct}}": "待记录",
        "{{user_nickname}}": state_data.get('user_nickname') or '用户'
    }

    result = template_content
    for var, value in replacements.items():
        result = result.replace(var, value)
    return result


def select_template_by_language(user_message):
    if user_message:
        msg_lower = user_message.lower()
        # 状态查询模式 → 无需模板
        if any(w in msg_lower for w in ['status query', 'daily record status', '状态查询']):
            return None
        if any(word in msg_lower for word in ['morning query', 'evening review']):
            lang = 'en'
        elif any(word in msg_lower for word in ['早上问询', '晚上复盘']):
            lang = 'zh'
        else:
            lang = 'zh'
    else:
        lang = 'zh'

    template_path = LANGUAGE_MAP.get(lang, LANGUAGE_MAP["zh"])
    return template_path


def load_template_by_name(template_name, template_path):
    """从模板文件中抽取指定模板内容（支持 DOTALL）"""
    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()

    sections = re.split(r'(?<=\n)### ', content)

    for section in sections:
        if template_name in section:
            # 使用 DOTALL 标志，让 . 匹配换行符
            template_match = re.search(r'```\s*\n([^\`]+)\s*```', section, re.DOTALL)
            if template_match:
                return template_match.group(1).strip()

    raise ValueError(f"在文件 {template_path} 中未找到模板 {template_name}")


def generate_status_report(state, today):
    """生成状态报告（无模板，直接输出统计信息）"""
    # 统计 notes 文件数量（使用 Python os.listdir）
    note_dir = os.path.join(NOTE_BASE_DIR, DAILY_RECORDER_SUBDIR)
    if not os.path.exists(note_dir):
        note_count = 0
    else:
        note_files = [f for f in os.listdir(note_dir) if f.endswith('.md')]
        note_count = len(note_files)

    print(f"=== Daily Record Status ===")
    print(f"当前周期：第 {state.get('current_cycle', '未知')} 周")
    print(f"已记录天数：{note_count}")
    print(f"目标用户 (feishu): {state.get('user_id_by_channel', {}).get('feishu', '未配置')}")


def main(time_period="morning", weekday_override=None, cycle_override=None,
         user_message=None, target_channel=None, mode="auto"):
    """
    time_period: morning/evening
    mode: "auto" (自动检测), "cron" (Cron 模式，无输出前缀), 
            "manual" (手动触发，直接返回结果),
            "record_feedback" (用户已反馈 → 立即记录到笔记)
    """
    if user_message:
        detected_period = detect_trigger(user_message, time_period)
        time_period = detected_period

    state = load_state()
    today = datetime.now().date()

    # 状态查询模式 → 输出报告而非问询
    if time_period == "status_query":
        generate_status_report(state, today)
        return None
    
    # 【v2.0 混合触发机制】用户已反馈 → 立即记录到笔记
    if mode == "record_feedback" and user_message:
        from record_feedback import main as record_main
        
        from datetime import datetime, time
        now = datetime.now()
        current_hour = now.hour
        
        # v2.0: 定义触发词列表（保留原有关键词 + 新增智能推断）
        STRICT_MORNING_TRIGGERS = ['记录早反馈', '记录一下早反馈']
        STRICT_EVENING_TRIGGERS = ['记录今日复盘', '记录一下晚复盘', '记一下晚反馈']
        APPENDIX_TRIGGERS = ['补充记录', '追加信息']
        
        # 智能推断：基于时间判断早晚
        def is_morning_period():
            return time(6, 0) <= now.time() < time(12, 0)
        
        def is_evening_period():
            return time(18, 0) <= now.time() < time(23, 59)
        
        # 检测触发词
        detected_mode = None
        msg_lower = user_message.lower().strip()
        
        if any(trigger in msg_lower for trigger in STRICT_MORNING_TRIGGERS):
            detected_mode = 'morning'
        elif any(trigger in msg_lower for trigger in STRICT_EVENING_TRIGGERS):
            detected_mode = 'evening'
        elif any(trigger in msg_lower for trigger in APPENDIX_TRIGGERS):
            detected_mode = 'appendix'
        else:
            # v2.0: 尝试智能推断模式
            if is_morning_period():
                print("🌅 检测到早晨时段 (6-12 点)，自动识别为晨间记录...")
                detected_mode = 'morning'
            elif is_evening_period():
                print("🌙 检测到傍晚时段 (18-23:59)，自动识别为晚间复盘...")
                detected_mode = 'evening'
            else:
                # 非工作时间，要求明确触发词
                print("⚠️ **格式错误：当前时间不属于标准记录时段**")
                print("")
                print("请在以下时间段使用智能推断模式:")
                print("- 早晨 (6:00-12:00): 说"能量 X"即可自动识别为早反馈")
                print("- 傍晚 (18:00-23:59): 说"能量 X"或"完成度 X%"即可自动识别为晚复盘")
                print("")
                print("或者使用明确触发词:")
                print("- `记录早反馈` / `记录一下早反馈`")
                print("- `记录今日复盘` / `记录一下晚复盘`")
                print("- `补充记录` / `追加信息`")
                return None
        
        # v2.0: 执行记录操作
        try:
            parsed_input = json.loads(user_message)
            record_main(mode=detected_mode, user_input=parsed_input)
            print("✓ 反馈已成功记录")
            return None
        except json.JSONDecodeError:
            # v2.0: 智能推断模式下仍尝试自动提取
            auto_extracted = extract_feedback_from_text(user_message)
            record_main(mode=detected_mode, user_input=auto_extracted)
            print("✓ 反馈已成功记录")
            return None
        
        # v2.0: 根据检测到的模式执行记录
        try:
            parsed_input = json.loads(user_message)
            record_main(mode=detected_mode, user_input=parsed_input)
            print("✓ 反馈已成功记录")
            return None
        except json.JSONDecodeError:
            # v2.0: 仍然尝试自动提取，但仅在严格触发词存在时才执行
            auto_extracted = extract_feedback_from_text(user_message)
            record_main(mode=detected_mode, user_input=auto_extracted)
            print("✓ 反馈已成功记录")
            return None

    weekday_num = weekday_override or get_weekday_from_date(today)
    current_cycle = cycle_override or state['current_cycle']

    yesterday_content = find_yesterday_note()
    energy_score = extract_energy_from_note(yesterday_content) if yesterday_content else None
    task_info = extract_task_info_from_note(yesterday_content) if yesterday_content else None

    template_name = select_template_for_time(time_period, weekday_num, current_cycle)
    if not template_name:
        raise RuntimeError(f"周 Day {weekday_num} 的 {time_period}问询模板未定义")

    template_path = select_template_by_language(user_message)
    template_content = load_template_by_name(template_name, template_path)

    # 构建昨日数据字典用于变量注入
    yesterday_data = {'energy_score': energy_score, 'task_info': task_info}
    
    # 使用标准 inject_variables 函数进行变量替换
    user_name = state.get('user_nickname') or '用户'
    cycle_num = state.get('current_cycle', 1)
    # 基础变量替换（所有模板通用）
    injected = template_content.replace("{{last_night_energy}}", str(energy_score or "待评估"))
    injected = injected.replace("{{user_nickname}}", user_name)
    injected = injected.replace("{{cycle_number}}", str(cycle_num))

    # 任务信息相关替换
    if task_info:
        injected = injected.replace("[任务名称]", task_info)
    else:
        injected = injected.replace("[任务名称]", "当日计划")

    # 【优化】第 2+周期：在标准模板下方追加智能进化分析内容
    # 而不是替换整个模板，保持关怀风格的同时提供数据洞察
    if current_cycle >= 2:
        # 构建智能进化补充内容
        evolution_content = f"""
---
### 📊 智能进化分析（基于前{cycle_num}周历史数据）
- **能量模式**: 通常在 {get_day_name(weekday_num)} 能量较高 (平均历史数据不足)
- **风险预警**: 在未知任务类型遇到阻碍概率 [[ ]]%
- **时间窗建议**: 建议从上午开始以提高成功率
"""
        # 将智能进化内容追加到模板末尾
        injected = injected + evolution_content

    # 【新增】在回复末尾添加记录反馈的触发提示（非 cron 模式）
    if mode != "cron":
        recorded_text = f"\n---\n🔍 **记录今日反馈**\n请输入以下关键字之一：\n- `记录今日复盘` / `记一下晚反馈` (晚间)\n- `记录早反馈` (晨间)\n- `append feedback` (英文触发)\n否则仅输出提示信息，不执行写入操作。"
        print(recorded_text)
    
    if mode == "cron":
        print(injected)  # Cron 模式：直接输出，无额外文字
    else:
        # 手动触发或自动检测模式：也直接输出（移除"已完成..."前缀）
        print(injected)
    return injected


def extract_feedback_from_text(text):
    """
    从用户反馈文本中自动提取关键字段
    支持多种格式：能量评分、任务列表、问题描述等
    
    示例输入:
    - "今日能量 5。精神疲劳。1. 开启自媒体职业计划 2. AI 输出文案"
    - "能量 5，疲劳。任务：自媒体计划、AI 生成文案初稿"
    
    返回字典结构供 record_feedback.py 使用
    """
    import re
    
    # 提取能量评分 (1-10)
    energy_match = re.search(r'[能 力]?能量\s*(\d+)', text.lower())
    if not energy_match:
        energy_match = re.search(r'能量\s*(\d+)', text, re.IGNORECASE)
    
    extracted = {
        'early_feedback': {},
        'completion_rates': {},
        'barriers': [],
        'next_day_plan_ideas': ''
    }
    
    if energy_match:
        energy_val = int(energy_match.group(1))
        extracted['early_feedback'] = {
            'energy': energy_val,
            'readiness': '可以开始' if energy_val >= 5 else '需要调整'
        }
    else:
        # 默认值
        extracted['early_feedback'] = {
            'energy': '待评估',
            'readiness': '待确认'
        }
    
    # 提取精神状态/疲劳描述
    fatigue_keywords = ['疲劳', '累', '疲惫', '精神不振']
    energy_state_keywords = ['充沛', '清醒', '精力好', '满电']
    
    if any(kw in text for kw in fatigue_keywords):
        extracted['early_feedback']['readiness'] = '需要调整'
        extracted['barriers'].append('精神疲劳')
    elif any(kw in text for kw in energy_state_keywords):
        extracted['early_feedback']['readiness'] = '可以开始'
    
    # 提取任务列表（数字编号或项目符号）
    task_pattern = r'\d+\.\s*(.+?)(?=\n|$)'
    tasks = re.findall(task_pattern, text)
    for i, task in enumerate(tasks[:3]):  # 最多记录前 3 个任务
        extracted['completion_rates'][task.strip()] = '0'  # 今日开始，预计完成度为 0
    
    # 提取可能的问题/阻碍（关键词匹配）
    barrier_keywords = [
        ('AI', '技术'),
        ('生成质量不稳定', 'AI 问题'),
        ('耗时', '时间管理'),
        ('卡点', '计划偏差')
    ]
    
    for text_content, category in barrier_keywords:
        if text_content in text and text not in extracted['barriers']:
            extracted['barriers'].append(f'{category}: {text_content}')
    
    return extracted


if __name__ == "__main__":
    import sys

    time_period = "morning"
    user_message = None
    target_channel = None
    weekday_override = None
    mode = "auto"  # auto/cron/manual/record_feedback

    for i in range(1, len(sys.argv)):
        if sys.argv[i] == '--time-period':
            if i + 1 < len(sys.argv):
                time_period = sys.argv[i + 1]
        elif sys.argv[i].startswith('--user-message'):
            user_message = sys.argv[i].split('=', 1)[1] if '=' in sys.argv[i] else sys.argv[i + 1] if i + 1 < len(sys.argv) else None
        elif sys.argv[i].startswith('--channel='):
            target_channel = sys.argv[i].split('=', 1)[1]
        elif sys.argv[i].startswith('--weekday_override='):
            weekday_override = int(sys.argv[i].split('=', 1)[1])
        elif sys.argv[i] == '--mode=cron':
            mode = "cron"  # Cron 模式：无前缀
        elif sys.argv[i] == '--mode=manual':
            mode = "manual"  # 手动触发：有说明文字
        elif sys.argv[i] == '--mode=record_feedback':
            mode = "record_feedback"  # 【新增】用户已反馈 → 立即记录到笔记

    if len(sys.argv) == 2 and sys.argv[1] in ['morning', 'evening']:
        time_period = sys.argv[1]

    main(time_period, user_message=user_message, target_channel=target_channel, weekday_override=weekday_override)
