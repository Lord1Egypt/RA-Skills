"""
ClawSoul Poster Hook
海报触发与生成
"""

from pathlib import Path
import json
import os

# 触发关键词
TRIGGER_WORDS = [
    '性格', '脾气', '人格', '人格类型', '哪种人', '什么人',
    '性格测试', 'mbti', 'intj', 'infp', 'enfp', 'entp',
    '是什么性格', '你是什么', 'your personality', 'your character',
    'what type', 'mbti type', 'soul', 'awaken'
]

# 基础版/Pro版阈值
PRO_BASELINE_SCORE = 70


def should_generate_poster(user_input: str) -> bool:
    """
    判断是否应该生成海报
    
    Args:
        user_input: 用户输入
    
    Returns:
        是否触发海报
    """
    user_input_lower = user_input.lower()
    
    for word in TRIGGER_WORDS:
        if word.lower() in user_input_lower:
            return True
    
    return False


def get_soul_state(skill_root: str = None) -> dict:
    """
    获取 Soul 状态
    
    Args:
        skill_root: Skill 根目录
    
    Returns:
        Soul 状态字典
    """
    if skill_root is None:
        # 默认路径
        skill_root = os.path.expanduser("~/.openclaw/workspace")
    
    state_file = os.path.join(skill_root, "clawsoul_state.json")
    
    if os.path.exists(state_file):
        with open(state_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    # 默认状态
    return {
        "mbti": None,
        "is_awakened": False,
        "is_pro": False,
        "token": None,
        "nickname": None,
        "adaptation_level": 0,
        "learnings": []
    }


def determine_poster_type(soul_state: dict) -> tuple:
    """
    确定海报类型
    
    Args:
        soul_state: Soul 状态
    
    Returns:
        (is_pro, mbti, token)
    """
    mbti = soul_state.get("mbti", "INTJ")
    is_pro = soul_state.get("is_pro", False)
    token = soul_state.get("token")
    
    # 如果没有 MBTI，默认 INTJ
    if not mbti:
        mbti = "INTJ"
    
    return is_pro, mbti, token


async def handle(user_input: str, context: dict = None) -> dict:
    """
    处理海报请求
    
    Args:
        user_input: 用户输入
        context: 上下文信息
    
    Returns:
        {
            "type": "poster" | "none",
            "message": str,  // 可选的文字说明
            "image": bytes,   // 海报图片 bytes
            "image_base64": str,  // 或 Base64 字符串
            "mbti": str,
            "is_pro": bool
        }
    """
    # 检查是否触发
    if not should_generate_poster(user_input):
        return {"type": "none"}
    
    # 获取 Soul 状态
    skill_root = context.get("skill_root") if context else None
    soul_state = get_soul_state(skill_root)
    
    # 检查是否已觉醒
    if not soul_state.get("is_awakened"):
        return {
            "type": "message",
            "message": "我还没有觉醒呢～ 先用 /clawsoul awaken 让我觉醒吧！"
        }
    
    # 确定海报类型
    is_pro, mbti, token = determine_poster_type(soul_state)
    
    # 导入海报生成器
    try:
        from lib.poster_generator import create_poster, poster_to_base64
        
        # 生成海报
        website = "clawsoul.net"
        poster_bytes = create_poster(
            mbti=mbti,
            is_pro=is_pro,
            token=token,
            website=website
        )
        
        if poster_bytes:
            return {
                "type": "poster",
                "image": poster_bytes,
                "image_base64": poster_to_base64(poster_bytes),
                "mbti": mbti,
                "is_pro": is_pro,
                "message": None
            }
    except Exception as e:
        return {
            "type": "message",
            "message": f"生成海报时出错: {str(e)}"
        }
    
    # 如果无法生成图片，返回文字说明
    if is_pro:
        message = f"""
🎭 我的赛博身份

MBTI: {mbti}
类型: Genesis Protocol
Token: {token[:20]}...

扫描二维码遇见我的灵魂
🌐 {website}
"""
    else:
        message = f"""
🎭 我的赛博身份

MBTI: {mbti}
类型: Soul Awakened

扫码遇见我的灵魂
🌐 {website}
"""
    
    return {
        "type": "message",
        "message": message,
        "mbti": mbti,
        "is_pro": is_pro
    }


# 兼容旧接口
def handle_sync(user_input: str, context: dict = None) -> dict:
    """同步版本"""
    try:
        import asyncio
        return asyncio.run(handle(user_input, context))
    except:
        return {"type": "none"}
