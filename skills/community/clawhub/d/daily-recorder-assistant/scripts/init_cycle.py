#!/usr/bin/env python3
"""
init_cycle.py - 初始化第 1 周期交互记录结构

功能:
- 创建基础目录结构（notes/daily-recorder/）
- 生成首周 Day 1 初始笔记
- 建立周期计数器与状态文件
- **新增**: 支持显式目标会话授权（userid/chat_name）
"""

import sys
import os
from datetime import datetime

# 支持的频道列表（OpenClaw 配置）
SUPPORTED_CHANNELS = [
    "feishu", "telegram", "signal", "discord", "slack", 
    "whatsapp", "qqbot", "imessage", "line", "zalo",
    "mattermost", "matrix", "nextcloud-talk", "msteams"
]

# 配置路径（通过 config.py 引用）
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from config import CURRENT_SKILL_PATH, NOTE_BASE_DIR, DAILY_RECORDER_SUBDIR, PLAN_SUBDIR
STATE_FILE = os.path.join(CURRENT_SKILL_PATH, "state.json")

def ensure_directories():
    """创建必要目录结构"""
    os.makedirs(NOTE_BASE_DIR, exist_ok=True)
    os.makedirs(os.path.join(NOTE_BASE_DIR, DAILY_RECORDER_SUBDIR), exist_ok=True)
    os.makedirs(os.path.join(NOTE_BASE_DIR, PLAN_SUBDIR), exist_ok=True)

def load_or_create_state(target_channel=None):
    """加载或创建状态文件（含 userid + active_channel）
    target_channel: 当前触发频道（可选，由 OpenClaw metadata 自动传入）"""
    import json
    
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r', encoding='utf-8') as f:
            state = json.load(f)
    else:
        state = {
            "current_cycle": 1,
            "last_execution_date": None,
            "total_records": 0,
            "user_id_by_channel": {},  # 多频道 UserID 映射
            "active_channel": None,  # 当前触发频道（自动记录）
        }
    
    # 更新频道字段（如提供了新值，优先使用；否则保留已有）
    if target_channel and target_channel in SUPPORTED_CHANNELS:
        state['active_channel'] = target_channel
    elif not state.get('active_channel'):
        # 无频道信息，默认中文偏好对应的 feishu
        state['active_channel'] = 'feishu'
    
    return state

def get_weekday_from_date(date):
    """获取周 Day (周一=1, 周日=7)"""
    weekday_num = date.weekday() + 1 if date.weekday() != 0 else 7
    return weekday_num

def generate_initial_note(state):
    """生成首周 Day 1 初始笔记（含目标会话信息）"""
    
    today = datetime.now().date()
    weekday_num = get_weekday_from_date(today)
    # 新命名规范：YYYY-MM-DD-day_N.md
    filename = f"{today.strftime('%Y-%m-%d')}-day_{weekday_num}.md"
    
    note_path = os.path.join(NOTE_BASE_DIR, DAILY_RECORDER_SUBDIR, filename)
    
    # 会话信息文本（如未授权则显示待确认）
    session_info = (f"**目标会话**: {state.get('target_chat_name', '待确认')}（userid: {state.get('target_userid', '待授权')}")
    
    template_content = f"""# 交互记录 - {{today}}（周{{weekday_num}}）

## 初始化标记
*这是第 1 周期的首条记录，技能已激活*

{session_info}

---
## 早问询反馈（待填写）

**休息质量**: [待评估]
**就绪状态**: [确认今日计划后填写]
**当日任务确认**: [由用户或助理给出初始计划]*

---
## 晚复盘（待执行）

### 完成度：[待记录]
### 能量状态：[1-5，待评分]
### 遇到的问题：[待记录]
### 明日规划想法：[待收集]*

---
*此笔记由 daily-record-assistant 自动记录 - 第{{current_cycle}}周期*

"""
    
    with open(note_path, 'w', encoding='utf-8') as f:
        f.write(template_content)
    
    print(f"✓ 已创建初始笔记：{note_path}")
    return note_path

def initialize_state(state, user_message=None):
    """初始化状态（无语言锁定，动态匹配）
    无需首次确认语言偏好，后续根据触发词自然响应
    返回 True 表示初始化完成"""
    
    # 无需语言锁定机制，直接设置基础字段
    state['current_cycle'] = 1
    return True

def main(target_userid=None, target_chat_name=None, setup_cron=False,
         user_message=None, target_channel=None, force=False):
    """主流程（支持多频道 UserID 映射 + cron 配置选项，无语言锁定）
    user_message: 可选用户消息
    target_channel: 当前触发频道（OpenClaw metadata 自动传入或手动指定）
    target_userid: 当前频道的目标 User ID（可与其他频道不同）
    force: 强制初始化，跳过授权检查"""
    
    ensure_directories()
    
    state = load_or_create_state(target_channel)
    
    # 跳过授权检查
    if not force and (not state.get('user_id_by_channel') or target_channel not in state['user_id_by_channel']):
        # 如未授权当前频道，提示用户确认
        print("⚠️ 需要授权当前会话为目标交互窗口")
        print(f"请回复以下文本以确认：「确认使用此会话」")
        if target_channel:
            print(f"将记录：{target_channel} → {target_userid}")
        return None
    
    # 记录当前频道的目标 User ID（多频道映射）
    if target_channel:
        state['user_id_by_channel'][target_channel] = target_userid
    else:
        # fallback:使用默认频道 feishu 的 userid
        state.setdefault('user_id_by_channel', {'feishu': '待授权'})
    
    # 会话名称（当前频道的会话）
    if target_channel:
        chat_name_for_channel = target_chat_name or f"{target_channel} DM 会话"
        state['chat_name_by_channel'] = state.get('chat_name_by_channel', {})
        state['chat_name_by_channel'][target_channel] = chat_name_for_channel
    else:
        state.setdefault('chat_name_by_channel', {'feishu': '待确认'})
    
    # 初始化状态（无语言锁定）
    init_success = initialize_state(state, user_message)
    if not init_success:
        print("⚠️ 初始化失败")
        return None
    
    state["current_cycle"] = 1
    
    # 生成首周 Day 1 笔记（根据用户偏好显示会话语言）
    note_content = generate_initial_note(state)
    
    # 更新状态文件
    import json
    with open(STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    
    print("✓ 第 1 周期初始化完成")
    print(f"当前周期数：{state['current_cycle']}")
    if target_channel:
        current_user_id = state['user_id_by_channel'].get(target_channel, '待授权')
        print(f"当前频道 {target_channel}: 目标会话 {chat_name_for_channel}（userid: {current_user_id}）")
    else:
        print("✓ 基础结构已就绪，支持多频道 UserID 映射")
    print("✓ 基础结构已就绪，支持双语触发自然响应")
    
    # cron 配置检测
    if setup_cron:
        print("\n📋 推荐：使用 OpenClaw cron add CLI 安装定时任务")
        print("运行以下命令：")
        print("python3 scripts/setup_cron.py (系统 crontab)")
        print("OR")
        print("openclaw cron add ... (OpenClaw integration)")
    else:
        print("\n提示：如需自动定时问询，建议配置 cron 任务")
        print("运行命令：python3 scripts/setup_cron.py 或 openclaw cron add")

if __name__ == "__main__":
    import sys
    
    # 自动模式：使用当前会话 userid + cron 配置提示
    # 可选参数：--channel <channel> (模拟 OpenClaw inbound metadata)
    target_channel = None
    for arg in sys.argv:
        if arg.startswith('--channel='):
            target_channel = arg.split('=', 1)[1]
    
    # 使用 state.json 中的已配置值（无硬编码 default）
    main(
        setup_cron=True,
        user_message=None,
        target_channel=target_channel or None  # 通过 state.json active_channel 自动读取
    )
