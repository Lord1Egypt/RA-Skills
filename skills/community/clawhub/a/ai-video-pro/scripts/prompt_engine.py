"""
镜头语言提示词优化引擎

将用户的自然语言描述转化为结构化的影视级 prompt，
并根据不同视频生成 Provider 的特点进行适配输出。
"""

import json
import sys
from dataclasses import dataclass, field, asdict
from typing import Optional


@dataclass
class CinematicElements:
    """结构化的影视元素。"""
    shot_type: Optional[str] = None
    camera_movement: Optional[str] = None
    lighting: Optional[str] = None
    color_grade: Optional[str] = None
    temporal: Optional[str] = None  # 慢动作/正常/延时
    aspect_ratio: Optional[str] = None
    duration_seconds: Optional[int] = None
    visual_style: Optional[str] = None  # 写实/动漫/3D等


@dataclass
class CharacterDynamics:
    """角色动态要素。"""
    characters: list = field(default_factory=list)
    spatial_relationship: Optional[str] = None
    action_type: Optional[str] = None
    impact_level: Optional[str] = None  # 打击力度
    impact_reaction: Optional[str] = None  # 受击反应
    impact_effects: list = field(default_factory=list)  # 火花/碎片等
    injury_effects: Optional[str] = None  # 受伤效果
    expression_start: Optional[str] = None
    expression_end: Optional[str] = None
    eye_contact: Optional[bool] = None
    body_language: Optional[str] = None
    mecha_motion_style: Optional[str] = None  # 机甲运动风格


@dataclass
class SceneAnalysis:
    """场景分析结果。"""
    scene_type: str = "general"  # action/character/mecha/emotional/landscape
    user_input: str = ""
    cinematic: CinematicElements = field(default_factory=CinematicElements)
    dynamics: CharacterDynamics = field(default_factory=CharacterDynamics)
    missing_elements: list = field(default_factory=list)
    questions_for_user: list = field(default_factory=list)


# 场景类型关键词映射
SCENE_TYPE_KEYWORDS = {
    "action": ["打架", "战斗", "决斗", "攻击", "格斗", "武术", "fight", "battle", "combat",
               "拳击", "踢", "射击", "爆炸", "追逐", "冲击", "clash", "打斗"],
    "mecha": ["机甲", "机器人", "mecha", "robot", "变形", "高达", "gundam",
              "机体", "装甲", "titan", "mech", "机械"],
    "emotional": ["哭", "笑", "悲伤", "开心", "难过", "怒", "泪", "表情", "情感", "感动",
                  "emotion", "cry", "smile", "tear", "sad", "happy", "喜悦", "愤怒",
                  "恐惧", "惊讶", "快乐"],
    "character": ["对话", "交流", "拥抱", "握手", "告别", "重逢", "关系", "离别",
                  "conversation", "hug", "farewell", "reunion", "送别", "父亲",
                  "母亲", "朋友", "恋人", "家人"],
    "landscape": ["风景", "城市", "海洋", "森林", "山", "天空", "日落",
                  "landscape", "city", "ocean", "forest", "mountain", "sunset"],
}

# 各场景类型的必需元素
REQUIRED_ELEMENTS = {
    "action": [
        ("impact_level", "打击/冲击力度级别", "这个打击场景需要什么级别的冲击力？轻柔的接触、沉重的打击、还是夸张的影视效果？"),
        ("impact_reaction", "受击反应", "被击中的角色应该如何反应？后退、倒地、格挡还是被击飞？"),
        ("expression_start", "攻击者表情", "攻击者打击前后的面部表情是怎样的？（如：冷静→愤怒→坚定）"),
        ("expression_end", "受击者表情", "被击者受击前后的面部表情是怎样的？（如：惊讶→痛苦→不屈）"),
        ("impact_effects", "冲击特效", "是否需要冲击特效？如火花、碎片飞溅、冲击波、画面震动等"),
        ("injury_effects", "受伤效果", "需要表现受伤效果吗？比如划痕、护甲破损、流血等"),
    ],
    "mecha": [
        ("mecha_motion_style", "运动风格", "机甲的运动风格是什么？像高达那样流畅敏捷，还是像太平洋机甲那样沉重有力？"),
        ("characters", "机甲尺寸", "机甲有多大？和人差不多大，还是可以踩扁汽车的巨型机器人？"),
        ("body_language", "关节细节", "需要展示关节的机械细节吗？比如液压杆伸缩、齿轮转动、管线联动等"),
        ("spatial_relationship", "环境反馈", "机甲的运动是否需要影响环境？比如踏步碎裂地面、奔跑掀起沙尘等"),
    ],
    "emotional": [
        ("expression_start", "起始表情", "角色的表情从什么状态开始？（如：平静、悲伤、迷茫）"),
        ("expression_end", "结束表情", "角色的表情变化到什么状态？（如：欢笑、释然、坚定）"),
        ("temporal", "变化速度", "这个表情变化是瞬间的还是缓慢渐变的？"),
        ("eye_contact", "眼部细节", "需要表现泪光、瞳孔放大等眼部细节吗？"),
    ],
    "character": [
        ("spatial_relationship", "角色关系", "这些角色之间是什么关系？朋友、对手、亲人、还是陌生人？"),
        ("action_type", "情绪基调", "这个场景的情绪基调是什么？紧张、温暖、悲伤还是欢快？"),
        ("eye_contact", "眼神交流", "角色之间是否有眼神交流？直视、回避还是对峙？"),
        ("body_language", "空间变化", "在镜头中，角色之间的距离会发生变化吗？走近/远离/保持？"),
    ],
}

# 所有场景通用的必问元素
UNIVERSAL_REQUIRED = [
    ("aspect_ratio", "画面比例", "画面比例是什么？16:9（横屏）、9:16（竖屏，适合抖音）、还是 1:1（方形，适合小红书）？"),
    ("duration_seconds", "目标时长", "视频大约需要多长？3秒、5秒还是10秒？"),
    ("visual_style", "视觉风格", "希望什么视觉风格？写实、动漫、3D渲染、水彩、油画？"),
]

# ── 提取模式字典 ─────────────────────────────────────────────────────────────

SHOT_TYPE_PATTERNS = {
    "ECU": ["特写", "大特写", "extreme close", "ECU"],
    "CU": ["近景", "close up", "close-up", "CU"],
    "MS": ["中景", "medium shot", "MS"],
    "FS": ["全景", "full shot", "FS"],
    "WS": ["远景", "wide shot", "wide"],
    "aerial": ["鸟瞰", "俯瞰", "aerial", "bird's eye"],
    "low_angle": ["仰拍", "仰角", "low angle"],
    "dutch_angle": ["荷兰角", "dutch angle"],
    "OTS": ["过肩", "over the shoulder"],
}

CAMERA_MOVEMENT_PATTERNS = {
    "static": ["固定", "static", "still"],
    "pan": ["横摇", "pan", "panning"],
    "dolly_in": ["推轨", "dolly", "推进", "缓慢推进", "push in"],
    "tracking": ["跟拍", "tracking", "follow shot"],
    "handheld": ["手持", "handheld", "shaky cam"],
    "steadicam": ["斯坦尼康", "steadicam"],
    "crane": ["摇臂", "crane", "jib"],
    "whip_pan": ["甩镜", "whip pan"],
}

LIGHTING_PATTERNS = {
    "rembrandt": ["伦勃朗", "rembrandt"],
    "golden_hour": ["黄金时刻", "golden hour", "magic hour", "黄昏", "日落", "夕阳"],
    "neon": ["霓虹", "neon"],
    "volumetric": ["体积光", "volumetric", "god rays", "光束"],
    "backlit": ["逆光", "轮廓光", "backlit", "rim light"],
    "silhouette": ["剪影", "silhouette"],
    "soft": ["柔光", "soft light", "soft"],
}

COLOR_GRADE_PATTERNS = {
    "teal_orange": ["青橙", "teal orange", "teal and orange"],
    "desaturated": ["去饱和", "desaturated", "低饱和", "muted"],
    "warm": ["暖色", "warm", "orange tones"],
    "cool": ["冷色", "cool", "blue tones"],
    "film": ["胶片", "film grain", "analog", "胶片感"],
    "monochrome": ["黑白", "单色", "monochrome", "black and white"],
}

TEMPORAL_PATTERNS = {
    "slow_motion": ["慢动作", "慢镜", "slow motion", "slow-mo", "bullet time", "升格"],
    "timelapse": ["延时", "time-lapse", "timelapse"],
    "speed_ramp": ["变速", "speed ramp"],
    "freeze": ["定格", "freeze frame", "freeze"],
}

IMPACT_LEVEL_PATTERNS = {
    "light": ["轻触"],
    "heavy": ["重击"],
    "exaggerated": ["夸张"],
    "intense": ["猛烈"],
}

IMPACT_EFFECT_PATTERNS = {
    "sparks": ["火花"],
    "debris": ["碎片"],
    "shockwave": ["冲击波"],
    "dust": ["扬尘"],
}

# Emotion words used for expression hint extraction
EMOTION_WORDS = [
    "平静", "悲伤", "迷茫", "欢笑", "释然", "坚定",
    "愤怒", "恐惧", "惊讶", "快乐", "痛苦", "冷静",
    "绝望", "希望", "紧张", "放松", "自信", "怀疑",
]


def _match_patterns(text: str, patterns: dict) -> Optional[str]:
    """Return the first pattern key whose keyword list has a match in text."""
    text_lower = text.lower()
    for label, keywords in patterns.items():
        for kw in keywords:
            if kw.lower() in text_lower:
                return label
    return None


def extract_cinematic_elements(description: str) -> CinematicElements:
    """
    Scan *description* for cinematography keywords and return a populated
    CinematicElements dataclass.  Fields that cannot be inferred stay None.
    """
    return CinematicElements(
        shot_type=_match_patterns(description, SHOT_TYPE_PATTERNS),
        camera_movement=_match_patterns(description, CAMERA_MOVEMENT_PATTERNS),
        lighting=_match_patterns(description, LIGHTING_PATTERNS),
        color_grade=_match_patterns(description, COLOR_GRADE_PATTERNS),
        temporal=_match_patterns(description, TEMPORAL_PATTERNS),
        # aspect_ratio / duration_seconds / visual_style are not pattern-detectable
        # from free-form text in a reliable way; leave them for user clarification.
    )


def extract_character_dynamics(description: str) -> CharacterDynamics:
    """
    Scan *description* for character / impact keywords and return a populated
    CharacterDynamics dataclass.
    """
    dynamics = CharacterDynamics()

    # Impact level
    dynamics.impact_level = _match_patterns(description, IMPACT_LEVEL_PATTERNS)

    # Impact effects – collect ALL matching effects
    effects = []
    desc_lower = description.lower()
    for effect_label, keywords in IMPACT_EFFECT_PATTERNS.items():
        for kw in keywords:
            if kw.lower() in desc_lower:
                effects.append(effect_label)
                break
    dynamics.impact_effects = effects

    # Expression hints: look for emotion words in roughly the first / last
    # quarter of the description to guess start → end expression.
    tokens = description.split()
    quarter = max(1, len(tokens) // 4)
    start_text = " ".join(tokens[:quarter])
    end_text = " ".join(tokens[-quarter:])

    for word in EMOTION_WORDS:
        if word in start_text and dynamics.expression_start is None:
            dynamics.expression_start = word
        if word in end_text and dynamics.expression_end is None:
            dynamics.expression_end = word

    return dynamics


def detect_scene_type(description: str) -> str:
    """根据描述内容检测场景类型。"""
    description_lower = description.lower()
    scores = {}

    for scene_type, keywords in SCENE_TYPE_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in description_lower)
        if score > 0:
            scores[scene_type] = score

    if not scores:
        return "general"

    # 特定场景类型的优先级加权（更具体的类型优先）
    priority_boost = {"mecha": 0.5, "emotional": 0.5, "character": 0.3}
    for scene_type in scores:
        scores[scene_type] += priority_boost.get(scene_type, 0)

    return max(scores, key=scores.get)


def detect_all_scene_types(description: str) -> list:
    """
    Return ALL scene types that score > 0, sorted by descending score.
    Allows a scene to be both 'action' and 'emotional' at the same time.
    """
    description_lower = description.lower()
    scores = {}

    for scene_type, keywords in SCENE_TYPE_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in description_lower)
        if score > 0:
            scores[scene_type] = score

    if not scores:
        return ["general"]

    priority_boost = {"mecha": 0.5, "emotional": 0.5, "character": 0.3}
    for scene_type in scores:
        scores[scene_type] += priority_boost.get(scene_type, 0)

    return sorted(scores, key=scores.get, reverse=True)


def _dynamics_field_filled(dynamics: CharacterDynamics, field_name: str) -> bool:
    """Return True if a CharacterDynamics field has been populated."""
    value = getattr(dynamics, field_name, None)
    if value is None:
        return False
    if isinstance(value, list):
        return len(value) > 0
    if isinstance(value, bool):
        return True  # False is still a real answer
    return bool(value)


def _cinematic_field_filled(cinematic: CinematicElements, field_name: str) -> bool:
    """Return True if a CinematicElements field has been populated."""
    value = getattr(cinematic, field_name, None)
    if value is None:
        return False
    return bool(value)


def analyze_scene(description: str) -> SceneAnalysis:
    """
    分析用户描述，提取影视元素，识别缺失要素。

    Args:
        description: 用户的自然语言描述

    Returns:
        SceneAnalysis 对象，包含分析结果和需要询问的问题
    """
    # Detect all matching scene types
    scene_types = detect_all_scene_types(description)
    primary_scene_type = scene_types[0]

    analysis = SceneAnalysis(
        user_input=description,
        scene_type=primary_scene_type,
    )

    # Extract cinematic elements and character dynamics from description
    analysis.cinematic = extract_cinematic_elements(description)
    analysis.dynamics = extract_character_dynamics(description)

    # Merge required-element lists for ALL detected scene types, deduplicating
    seen_fields = set()
    merged_required: list = []
    for scene_type in scene_types:
        for item in REQUIRED_ELEMENTS.get(scene_type, []):
            field_name = item[0]
            if field_name not in seen_fields:
                seen_fields.add(field_name)
                merged_required.append(item)

    # Only add to missing_elements / questions if the field is STILL None after extraction
    for field_name, element_name, question in merged_required:
        # Check both dynamics and cinematic objects
        already_filled = (
            _dynamics_field_filled(analysis.dynamics, field_name)
            or _cinematic_field_filled(analysis.cinematic, field_name)
        )
        if not already_filled:
            analysis.missing_elements.append(element_name)
            analysis.questions_for_user.append({
                "field": field_name,
                "element": element_name,
                "question": question,
            })

    # Check universal required elements (only those still None)
    for field_name, element_name, question in UNIVERSAL_REQUIRED:
        already_filled = _cinematic_field_filled(analysis.cinematic, field_name)
        if not already_filled:
            analysis.missing_elements.append(element_name)
            analysis.questions_for_user.append({
                "field": field_name,
                "element": element_name,
                "question": question,
            })

    return analysis


def format_for_provider(analysis: SceneAnalysis, provider: str,
                        user_answers: dict = None) -> str:
    """
    将分析结果格式化为特定 Provider 的 prompt。

    Args:
        analysis: 场景分析结果
        provider: 目标 provider (lumaai/runway/replicate/comfyui/dalle)
        user_answers: 用户对缺失元素的回答

    Returns:
        格式化后的 prompt 字符串
    """
    if provider == "lumaai":
        return _format_lumaai(analysis, user_answers)
    elif provider == "runway":
        return _format_runway(analysis, user_answers)
    elif provider == "replicate":
        return _format_replicate(analysis, user_answers)
    elif provider == "comfyui":
        return _format_comfyui(analysis, user_answers)
    elif provider == "dalle":
        return _format_dalle(analysis, user_answers)
    else:
        return _format_generic(analysis, user_answers)


def _resolve(analysis: SceneAnalysis, answers: dict, key: str):
    """
    Helper: return the value for *key* from user_answers if present,
    otherwise fall back to the matching field in dynamics or cinematic.
    """
    if answers and key in answers and answers[key]:
        return answers[key]
    dyn_val = getattr(analysis.dynamics, key, None)
    if dyn_val is not None and dyn_val != [] and dyn_val is not False:
        return dyn_val
    cin_val = getattr(analysis.cinematic, key, None)
    return cin_val


def _format_lumaai(analysis: SceneAnalysis, answers: dict = None) -> str:
    """LumaAI 偏好自然语言嵌入镜头指令。"""
    parts = []

    # 镜头描述
    shot = analysis.cinematic.shot_type or "cinematic shot"
    movement = analysis.cinematic.camera_movement
    if movement:
        parts.append(f"Camera {movement} in a {shot}")
    else:
        parts.append(f"{shot}")

    # 主体描述
    parts.append(f"of {analysis.user_input}")

    # 灯光和色彩
    if analysis.cinematic.lighting:
        parts.append(f"{analysis.cinematic.lighting} lighting")
    if analysis.cinematic.color_grade:
        parts.append(f"{analysis.cinematic.color_grade} color grading")

    # 动态元素 – prefer extracted values, fall back to user_answers
    impact_level = _resolve(analysis, answers, "impact_level")
    if impact_level:
        parts.append(f"with {impact_level} impact force")

    impact_effects = _resolve(analysis, answers, "impact_effects")
    if impact_effects:
        effects_str = impact_effects if isinstance(impact_effects, str) else ", ".join(impact_effects)
        if effects_str:
            parts.append(f"creating {effects_str}")

    expression_start = _resolve(analysis, answers, "expression_start")
    expression_end = _resolve(analysis, answers, "expression_end")
    if expression_start and expression_end:
        parts.append(
            f"expression transitioning from {expression_start} "
            f"to {expression_end}"
        )

    # 时间控制
    if analysis.cinematic.temporal:
        parts.append(f"{analysis.cinematic.temporal}")

    # 风格和质量
    style = analysis.cinematic.visual_style or "photorealistic"
    parts.append(f"{style}, cinematic quality, 4K")

    return ", ".join(parts) + "."


def _format_runway(analysis: SceneAnalysis, answers: dict = None) -> str:
    """Runway 偏好结构化的分离描述。"""
    sections = []

    sections.append(f"Subject: {analysis.user_input}")

    # 镜头
    camera_parts = []
    if analysis.cinematic.shot_type:
        camera_parts.append(analysis.cinematic.shot_type)
    if analysis.cinematic.camera_movement:
        camera_parts.append(analysis.cinematic.camera_movement)
    if analysis.cinematic.temporal:
        camera_parts.append(analysis.cinematic.temporal)
    if camera_parts:
        sections.append(f"Camera: {', '.join(camera_parts)}")

    # 灯光和风格
    style_parts = []
    style_parts.append(analysis.cinematic.visual_style or "Photorealistic")
    if analysis.cinematic.lighting:
        style_parts.append(analysis.cinematic.lighting)
    if analysis.cinematic.color_grade:
        style_parts.append(analysis.cinematic.color_grade)
    sections.append(f"Style: {', '.join(style_parts)}")

    # 动态 – prefer extracted values, fall back to user_answers
    action_parts = []
    impact_level = _resolve(analysis, answers, "impact_level")
    if impact_level:
        action_parts.append(f"{impact_level} impact")

    impact_effects = _resolve(analysis, answers, "impact_effects")
    if impact_effects:
        effects_str = impact_effects if isinstance(impact_effects, str) else ", ".join(impact_effects)
        if effects_str:
            action_parts.append(effects_str)

    impact_reaction = _resolve(analysis, answers, "impact_reaction")
    if impact_reaction:
        action_parts.append(f"target reacts with {impact_reaction}")

    if action_parts:
        sections.append(f"Action: {', '.join(action_parts)}")

    expression_start = _resolve(analysis, answers, "expression_start")
    expression_end = _resolve(analysis, answers, "expression_end")
    if expression_start:
        sections.append(
            f"Expression: {expression_start} → {expression_end or 'determined'}"
        )

    return "\n".join(sections)


def _format_replicate(analysis: SceneAnalysis, answers: dict = None) -> str:
    """Replicate 模型通常偏好简洁的 tag 风格。"""
    tags = []

    tags.append(analysis.user_input)

    if analysis.cinematic.shot_type:
        tags.append(analysis.cinematic.shot_type)
    if analysis.cinematic.camera_movement:
        tags.append(analysis.cinematic.camera_movement)
    if analysis.cinematic.lighting:
        tags.append(f"{analysis.cinematic.lighting} lighting")
    if analysis.cinematic.visual_style:
        tags.append(analysis.cinematic.visual_style)

    tags.extend(["cinematic", "high quality", "detailed"])

    return ", ".join(tags)


def _format_comfyui(analysis: SceneAnalysis, answers: dict = None) -> str:
    """ComfyUI 使用 positive/negative prompt 格式。"""
    positive = []
    negative = ["low quality", "blurry", "deformed", "watermark", "text"]

    positive.append("masterpiece, best quality")
    positive.append(analysis.user_input)

    if analysis.cinematic.lighting:
        positive.append(f"{analysis.cinematic.lighting} lighting")
    if analysis.cinematic.visual_style:
        positive.append(analysis.cinematic.visual_style)

    positive.extend(["cinematic composition", "detailed"])

    return json.dumps({
        "positive": ", ".join(positive),
        "negative": ", ".join(negative),
        "steps": 25,
        "cfg_scale": 7.5,
        "sampler": "euler_ancestral",
    }, ensure_ascii=False, indent=2)


def _format_dalle(analysis: SceneAnalysis, answers: dict = None) -> str:
    """DALL-E 偏好详细的自然语言描述。"""
    parts = [
        f"A {analysis.cinematic.visual_style or 'photorealistic'} "
        f"{analysis.cinematic.shot_type or 'cinematic shot'} "
        f"of {analysis.user_input}.",
    ]

    if analysis.cinematic.lighting:
        parts.append(f"The scene is lit with {analysis.cinematic.lighting}.")
    if analysis.cinematic.color_grade:
        parts.append(f"{analysis.cinematic.color_grade} color palette.")

    parts.append("High detail, cinematic composition, professional photography.")

    return " ".join(parts)


def _format_generic(analysis: SceneAnalysis, answers: dict = None) -> str:
    """通用格式。"""
    return f"{analysis.user_input}. Cinematic quality, high detail."


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python prompt_engine.py <描述> [provider]")
        print("示例: python prompt_engine.py '两个机器人在城市中战斗' lumaai")
        sys.exit(1)

    description = sys.argv[1]
    provider = sys.argv[2] if len(sys.argv) > 2 else "lumaai"

    analysis = analyze_scene(description)

    print("=== 场景分析 ===")
    print(f"场景类型: {analysis.scene_type}")
    print(f"原始描述: {analysis.user_input}")
    print()

    if analysis.questions_for_user:
        print("=== 需要补充的信息 ===")
        for q in analysis.questions_for_user:
            print(f"  [{q['element']}] {q['question']}")
        print()

    print(f"=== 优化后 Prompt ({provider}) ===")
    print(format_for_provider(analysis, provider))
