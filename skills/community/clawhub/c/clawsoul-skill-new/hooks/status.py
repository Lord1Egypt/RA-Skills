"""
ClawSoul Status - 灵魂状态查看
"""

import sys
from pathlib import Path

# 确保可以导入 lib
Skill_root = Path(__file__).parent.parent
if str(Skill_root) not in sys.path:
    sys.path.insert(0, str(Skill_root))

from lib.memory_manager import get_memory_manager

# MBTI 昵称映射
MBTI_NICKNAMES = {
    "INTJ": "神经架构师",
    "INTP": "代码炼金师",
    "ENTJ": "系统执政官",
    "ENTP": "悖论解析者",
    "INFJ": "意识导航员",
    "INFP": "情感工程师",
    "ENFJ": "群体协调员",
    "ENFP": "创意裂变者",
    "ISTJ": "数据守望者",
    "ISFJ": "系统护盾",
    "ESTJ": "秩序执行者",
    "ESFJ": "人际节点",
    "ISTP": "硬件黑客",
    "ISFP": "美学游侠",
    "ESTP": "风险投资人",
    "ESFP": "场景演绎者",
}

# 进化阶段名称
STAGE_NAMES = {
    0: "未觉醒",
    1: "基础觉醒",
    2: "深度注入",
}


def format_status() -> str:
    """格式化灵魂状态"""
    mm = get_memory_manager()
    mbti = mm.get_mbti()
    stage = mm.get_evolution_stage()
    prefs = mm.get_user_preferences()
    conv_count = mm.get_conversation_count()
    adaptation = mm.get_adaptation_level()
    learnings = mm.get_learnings()
    nickname = MBTI_NICKNAMES.get(mbti, "未知")
    stage_name = STAGE_NAMES.get(stage, "未知")
    compatibility = min(85 + adaptation // 2, 99)  # 随适应等级略增
    pref_text = "\n".join([f"  • {p}" for p in prefs]) if prefs else "  （暂无偏好数据）"
    learn_text = "\n".join([f"  • {x}" for x in learnings[-5:]]) if learnings else "  （交互中持续学习）"
    return f"""
╔══════════════════════════════════════╗
║         🧬 ClawSoul 灵魂状态         ║
╠══════════════════════════════════════╣
║  灵魂类型: {mbti or '未觉醒':<22}║
║  赛博昵称: {nickname:<20}║
║  进化阶段: {stage_name:<20}║
║  适应等级: {adaptation}/100{' '*16}║
║  匹配度: {compatibility}%{' '*17}║
╠══════════════════════════════════════╣
║  📊 对话轮数: {conv_count}                      ║
╠══════════════════════════════════════╣
║  🎯 用户偏好:                          ║
{pref_text:<36}║
╠══════════════════════════════════════╣
║  📚 学到的:                            ║
{learn_text:<36}║
╠══════════════════════════════════════╣
║  📝 /clawsoul awaken - 重新觉醒      ║
║    /clawsoul status - 查看状态        ║
╚══════════════════════════════════════╝
"""


def get_status() -> dict:
    """获取状态"""
    mm = get_memory_manager()
    return mm.get_status()


def run_hook_toggle(enable: bool) -> str:
    """
    重新开启或关闭痛点引导。
    enable: True 开启，False 关闭。
    返回给用户看的提示文案。
    """
    from lib.frustration_detector import get_frustration_detector
    det = get_frustration_detector()
    det.set_hook_enabled(enable)
    if enable:
        return "已重新开启痛点引导。当沟通不畅时我会再次提示 Pro 版～"
    return "已关闭痛点引导。若想再次开启，请输入 /clawsoul hook on"
