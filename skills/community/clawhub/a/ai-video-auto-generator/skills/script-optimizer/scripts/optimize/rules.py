"""
优化器规则与默认值常量。
被 optimize/__init__.py 通过 from .rules import * 导入。
"""

# ── 必填字段定义 ──
REQUIRED_GLOBAL_KEYS = {"image_style": str, "negative_prompt": str, "tone": str}
REQUIRED_CHAR_FIELDS = [
    "name", "title", "personality", "age_range", "build",
    "color_scheme", "distinctive_mark", "gender", "aesthetic_style",
]
REQUIRED_APPEARANCE_FIELDS = ["face", "hair", "armor/clothing", "aura"]
REQUIRED_FACE_DETAILS = ["face_shape", "eyes", "eyebrows", "nose", "lips", "jaw"]
REQUIRED_SCENE_FIELDS = ["id", "name", "description"]

# 模板占位符
PLACEHOLDER_PATTERNS = [r'角色名', r'角色称号', r'性格描述', r'面部描述', r'25-30岁']

OPTIMIZER_VERSION = "2.3.0"
MAX_ROUNDS = 10

# ── 基础默认值模板 ──
_BASE_DEFAULTS = {
    "global_style": "通用视频风格，画面明亮清晰，色彩自然，细节层次丰富",
    "aesthetic_style": "通用清晰风格",
    "tone": "通用叙事",
    "negative_prompt": "anime, illustration, cartoon, sketch, blurry",
    "image_style": "clean realistic",
    "color_tone": "自然色",
    "lighting": "标准布光",
    "asset_generation_model": "",
    "first_frame_model": "",
    "video_model": "",
    "scene_aspect_ratio": "16:9",
    "scene_size": "1280x720",
    "character_card_background": "white",
    "character_card_no_weapon": True,
}

# ── shot_type 默认运镜（分镜头型 + 叙事型） ──
DEFAULT_SHOT_CAMERA = {
    # 镜头型（按取景范围）
    "wide": "静态远景，镜头缓慢，建立场景空间感",
    "full": "全景固定镜头，角色全身可见",
    "medium": "中景固定镜头，标准叙事视角",
    "medium_two": "中景双人镜头，两人同框",
    "closeup": "近景特写，聚焦面部表情",
    "pov": "第一人称主观视角，轻微手持晃动",
    "extreme_closeup": "极端特写，聚焦局部细节",
    "over_shoulder": "过肩镜头，跟随对话关系",
    "low_angle": "低角度仰拍镜头，增强画面张力",
    # 叙事型（按剧情功能）
    "establishing": "广角远景，镜头缓慢推入，建立场景空间感",
    "reveal": "中景镜头，缓慢揭示主体，制造悬念",
    "emotional": "近景固定镜头，聚焦角色情感变化",
    "dialogue": "中景双人或过肩镜头，标准对话视角",
    "reaction": "近景特写，聚焦反应瞬间",
    "flashback": "全景固定镜头，边缘柔光虚化，营造回忆感",
    "action": "中景跟拍，轻微晃动增强动感",
    "comedy": "中景固定镜头，保持画面稳定配合喜剧节奏",
    "cliffhanger": "近景推近，制造紧张悬念",
    "slice_of_life": "中景固定镜头，日常叙事视角",
    "detail": "极端特写，聚焦局部细节",
    "transition": "广角平移镜头，场景过渡或时间跳跃",
}

# ── 场景 mood 推断 ──
DEFAULT_SCENE_MOOD = {
    "day": {"lighting": "自然天光，散射光为主", "mood": "日常/中性"},
    "night": {"lighting": "月光/火光+少量环境光", "mood": "安静/神秘"},
    "sunset": {"lighting": "金色落日余晖，暖色调", "mood": "温暖/怀旧"},
    "dawn": {"lighting": "晨曦微光，蓝紫渐变", "mood": "希望/新生"},
    "morning": {"lighting": "柔和晨光，金色调", "mood": "清新/生机"},
    "evening": {"lighting": "暮色余晖，低色温", "mood": "疲惫/沉思"},
    "dusk": {"lighting": "黄昏过渡光，蓝紫渐变", "mood": "神秘/不安"},
    "indoor": {"lighting": "室内灯光为主，人造光", "mood": "私密/封闭"},
    "overcast": {"lighting": "阴天散射光，无阴影", "mood": "压抑/沉闷"},
}

# ── 性别推断关键词 ──
MALE_KW = ["健硕", "高大", "魁梧", "肌肉结实", "强悍", "硬朗", "雄性",
           "胡子", "络腮胡", "胡茬", "宽阔", "方正", "粗犷", "铁血", "魁伟",
           "高大挺拔", "利落硬朗", "桀骜英气", "杀伐果断", "荷尔蒙"]
FEMALE_KW = ["娇小", "纤细", "婀娜", "柔美", "温婉", "纤瘦", "窈窕", "曼妙",
             "曲线", "苗条", "妩媚", "端庄", "清丽", "秀丽"]
MALE_NEUTRAL = ["清瘦", "单薄", "偏瘦", "瘦弱", "苍白", "白皙"]

# ── 面部子字段提取 ──
FACE_DETAIL_MAP = {
    "face_shape": ["脸型", "瓜子脸", "鹅蛋脸", "方脸", "圆脸", "国字脸", "窄长脸"],
    "eyes": ["眼", "眸", "瞳", "睛"],
    "eyebrows": ["眉"],
    "nose": ["鼻"],
    "lips": ["唇", "嘴"],
    "jaw": ["下颌", "颚", "下巴", "腮"],
}

FACE_DEFAULTS = {
    "face_shape": "标准脸型", "eyes": "有神双眸", "eyebrows": "标准眉形",
    "nose": "高挺鼻梁", "lips": "唇形分明", "jaw": "标准下颌",
}

# ── 质量分级 ──
QUALITY_BAD_VALUES = {
    "face_shape": ["标准脸型", "普通脸型"],
    "eyes": ["有神双眸", "标准眼睛"],
    "distinctive_mark": ["标志性特征"],
}

TEMPLATE_WEAPONS = {"剑", "弓"}
TEMPLATE_ACTIONS = {"行礼", "战斗"}
