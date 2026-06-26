#!/usr/bin/env python3
"""
V10.4 图片生成意图解析器 — 从用户自然语言提取结构化图片生成意图

作者: 圆规
GitHub: https://github.com/xyva-yuangui/beauty-image
License: MIT

支持两种模式:
  1. 规则快速路径: 关键词匹配 (<1ms)
  2. LLM深度解析: DeepSeek结构化分析 (可选, 需DEEPSEEK_API_KEY)
"""

import json
import re
from typing import Optional

from image_prompt_templates import SCENE_ALIASES, STYLE_ALIASES, SCENE_TEMPLATES, STYLE_DICT


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 规则快速路径 (Rule-based Fast Path)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# 场景关键词 → 场景ID (优先级从高到低)
_SCENE_RULES = [
    # 商务
    (r"(名片|business\s*card)", "biz_card"),
    (r"(海报|poster|宣传图|宣传画)", "biz_poster"),
    (r"(产品图|产品照|产品摄影|product\s*photo)", "biz_product"),
    # 社交
    (r"(头像|avatar|个人形象|IP形象|ip形象)", "social_avatar"),
    (r"(表情包|emoji|sticker|表情)", "social_emoji"),
    (r"(金句|语录|quote|名言).{0,5}(卡片|图|card)?", "social_card"),
    # 3D/材质
    (r"(水晶|crystal|玻璃|透明).{0,5}(质感|风格|效果|材质)?", "3d_crystal"),
    (r"(毛绒|plush|蓬松|绒毛).{0,5}(玩具|风格|效果|版)?", "3d_plush"),
    (r"(充气|inflatable|气球).{0,5}(玩具|风格|效果|版)?", "3d_inflatable"),
    (r"(微缩|miniature|等距|isometric|小场景|小房间|diorama)", "3d_miniature"),
    # 实用
    (r"(天气|weather).{0,5}(卡片|图|card)?", "util_weather"),
    (r"(冰箱贴|fridge\s*magnet|磁贴)", "util_fridge_magnet"),
    (r"(美食地图|food\s*map|食物地图)", "util_food_map"),
    (r"(分镜|storyboard|镜头脚本)", "util_storyboard"),
    # 设计
    (r"(PPT|ppt|幻灯片|slide)", "design_ppt"),
    (r"(logo|LOGO|标志|商标|徽标)", "design_logo"),
    (r"(包装|packaging|盒子设计)", "design_packaging"),
    # 人物
    (r"(肖像|portrait|写真|证件照)", "person_portrait"),
    (r"(手办|figure|模型|action\s*figure)", "person_action_figure"),
    # 场景
    (r"(黑板|chalkboard|粉笔画|粉笔)", "scene_chalkboard"),
    # 电商
    (r"(电商|主图|白底图|产品主图|淘宝|天猫).{0,5}(图|照)?", "ecom_main"),
    (r"(横幅|banner|促销图|活动图)", "ecom_banner"),
    # 内容
    (r"(小红书|xhs|种草).{0,5}(配图|图片|图)?", "content_xhs"),
    (r"(头图|封面图|blog|公众号|文章).{0,5}(配图|头图|封面)?", "content_blog"),
    # 特色
    (r"(浮世绘|ukiyo).{0,5}(闪卡|卡|卡牌|card)?", "art_ukiyoe_card"),
]

# 风格关键词 → 风格名称
_STYLE_RULES = [
    (r"赛博朋克|cyberpunk|科幻未来", "赛博朋克"),
    (r"浮世绘|ukiyo|日式传统", "浮世绘"),
    (r"水墨|国画|中国画|ink\s*wash", "水墨画"),
    (r"吉卜力|ghibli|宫崎骏|gibli", "吉卜力"),
    (r"像素|pixel|8.?bit|16.?bit|复古游戏", "像素风"),
    (r"油画|古典|文艺复兴|伦勃朗", "油画"),
    (r"漫画|manga|anime|动漫", "漫画"),
    (r"波普|pop\s*art|安迪沃霍尔", "波普艺术"),
    (r"水晶|crystal|玻璃质感|透明质感", "水晶"),
    (r"毛绒|plush|蓬松|绒毛", "毛绒"),
    (r"充气|inflatable|气球", "充气"),
    (r"乐高|lego|积木", "乐高"),
    (r"黏土|clay|橡皮泥|定格动画", "黏土"),
    (r"电影感|cinematic|电影画面", "电影感"),
    (r"产品摄影|产品照|白底|棚拍", "产品摄影"),
    (r"街拍|street|抓拍", "街拍"),
    (r"胶片|film|kodak|复古", "胶片"),
    (r"等距|isometric|微缩|3d微缩", "等距微缩"),
    (r"3d渲染|c4d|blender|三维", "3D渲染"),
    (r"清明上河图", "清明上河图"),
    (r"极简|minimalist|简约", None),  # 通用风格, 不映射到特定词典
    (r"ins风|instagram|小清新", None),
]

# 预编译正则
_COMPILED_SCENE_RULES = [(re.compile(p, re.IGNORECASE), sid) for p, sid in _SCENE_RULES]
_COMPILED_STYLE_RULES = [(re.compile(p, re.IGNORECASE), sname) for p, sname in _STYLE_RULES]


def parse_intent_fast(user_input: str) -> dict:
    """规则快速路径: 从用户输入提取场景和风格 (<1ms)

    返回:
        {
            "scene_id": str | None,
            "style": str | None,
            "subject": str,        # 提取的主体描述
            "fields": dict,        # 可填充的字段
            "missing_fields": list, # 还需要确认的必填字段
            "confidence": float,   # 0-1
        }
    """
    text = user_input.strip()

    # 场景匹配
    scene_id = None
    scene_confidence = 0.0
    for pattern, sid in _COMPILED_SCENE_RULES:
        if pattern.search(text):
            scene_id = sid
            scene_confidence = 0.8
            break

    # 风格匹配
    style_name = None
    for pattern, sname in _COMPILED_STYLE_RULES:
        if pattern.search(text):
            style_name = sname
            break

    # 提取主体 (去掉场景关键词和风格关键词后的核心描述)
    subject = text
    # 去掉常见的动词前缀
    subject = re.sub(r'^(帮我|请|给我|我要|我想|来一张?|做一张?|画一张?|生成一张?|创建一张?)', '', subject)
    # 去掉尾部动词
    subject = re.sub(r'(的图片?|的图|的照片|的设计)$', '', subject)
    subject = subject.strip()

    # 构建字段
    fields = {"subject": subject}

    # 特定场景的字段提取
    if scene_id == "biz_card":
        # 尝试从输入中提取名字
        name_match = re.search(r'(姓名|名字|叫|我是)[：:\s]*([^\s,，。]+)', text)
        if name_match:
            fields["name"] = name_match.group(2)
    elif scene_id == "util_weather":
        city_match = re.search(r'([\u4e00-\u9fff]{2,6})(的?天气|weather)', text)
        if city_match:
            fields["city"] = city_match.group(1)
    elif scene_id == "social_card":
        # 提取引号中的金句
        quote_match = re.search(r'[""「」『』](.*?)[""」」』』]', text)
        if quote_match:
            fields["text"] = quote_match.group(1)

    # 计算缺失字段
    missing_fields = []
    if scene_id and scene_id in SCENE_TEMPLATES:
        template = SCENE_TEMPLATES[scene_id]
        for field in template.get("required_fields", []):
            if field not in fields or not fields[field]:
                missing_fields.append(field)

    confidence = scene_confidence
    if style_name:
        confidence = min(confidence + 0.1, 1.0)
    if not scene_id and not style_name:
        confidence = 0.3  # 低置信, 可能需要LLM解析

    return {
        "scene_id": scene_id,
        "style": style_name,
        "subject": subject,
        "fields": fields,
        "missing_fields": missing_fields,
        "confidence": confidence,
    }


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# LLM深度解析 (DeepSeek)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

INTENT_PARSE_SYSTEM = """你是图片生成意图解析专家。分析用户的图片需求,输出JSON。

可用场景ID:
biz_card(名片), biz_poster(海报), biz_product(产品照), social_avatar(头像),
social_emoji(表情包), social_card(金句卡片), art_general(艺术创作),
3d_crystal(水晶质感), 3d_plush(毛绒), 3d_inflatable(充气), 3d_miniature(微缩场景),
util_weather(天气卡片), util_fridge_magnet(冰箱贴), util_food_map(美食地图),
util_storyboard(分镜), design_ppt(PPT), design_logo(Logo), design_packaging(包装),
person_portrait(肖像), person_action_figure(手办), scene_chalkboard(黑板粉笔画),
ecom_main(电商主图), ecom_banner(横幅), content_xhs(小红书配图),
content_blog(头图), art_ukiyoe_card(浮世绘闪卡)

可用风格: 赛博朋克, 浮世绘, 水墨画, 吉卜力, 像素风, 油画, 漫画, 波普艺术,
水晶, 毛绒, 充气, 乐高, 黏土, 电影感, 产品摄影, 街拍, 胶片, 等距微缩, 3D渲染, 清明上河图"""

INTENT_PARSE_PROMPT = """分析用户的图片生成请求,提取以下信息(仅输出JSON,不要其他文字):
{{
  "scene_id": "场景ID(从可用列表选, 无匹配则null)",
  "style": "风格名称(从可用列表选, 无匹配则null)",
  "subject": "主体描述(用户想生成什么)",
  "fields": {{
    "name": "名字(如有)",
    "title": "职称(如有)",
    "company": "公司(如有)",
    "city": "城市(如有)",
    "text": "需要渲染的文字(如有)",
    "color_scheme": "配色偏好(如有)",
    "mood": "情绪基调(如有)"
  }},
  "missing_info": ["还需要向用户确认的信息"],
  "recommended_size": "推荐尺寸比例(1:1/16:9/9:16/3:4/4:3)"
}}

用户输入: {user_input}"""


def parse_intent_llm(user_input: str, api_key: str, base_url: str = "https://api.deepseek.com/v1") -> dict:
    """LLM深度解析: 使用DeepSeek分析用户意图

    需要 requests 库和 DeepSeek API Key
    """
    import requests

    prompt = INTENT_PARSE_PROMPT.format(user_input=user_input)
    body = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": INTENT_PARSE_SYSTEM},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.1,
        "max_tokens": 500,
        "response_format": {"type": "json_object"},
    }

    try:
        resp = requests.post(
            f"{base_url}/chat/completions",
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            json=body,
            timeout=(3, 10),
        )
        if resp.status_code != 200:
            return {"error": f"HTTP {resp.status_code}", "fallback": True}

        content = resp.json()["choices"][0]["message"]["content"]
        parsed = json.loads(content)

        # 清理空值
        fields = {k: v for k, v in parsed.get("fields", {}).items() if v}

        return {
            "scene_id": parsed.get("scene_id"),
            "style": parsed.get("style"),
            "subject": parsed.get("subject", user_input),
            "fields": fields,
            "missing_fields": parsed.get("missing_info", []),
            "confidence": 0.9,
            "recommended_size": parsed.get("recommended_size"),
        }
    except Exception as e:
        return {"error": str(e), "fallback": True}


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 统一入口
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def parse_intent(user_input: str, use_llm: bool = False,
                 api_key: str | None = None, base_url: str | None = None) -> dict:
    """统一意图解析入口

    策略:
      1. 先用规则快速路径
      2. 如果置信度低(<0.5) 且 use_llm=True, 调用LLM深度解析
      3. 合并结果

    返回:
        {
            "scene_id": str | None,
            "style": str | None,
            "subject": str,
            "fields": dict,
            "missing_fields": list,
            "confidence": float,
            "method": "rule" | "llm",
        }
    """
    # Step 1: 规则快速路径
    result = parse_intent_fast(user_input)
    result["method"] = "rule"

    # Step 2: 低置信时尝试LLM
    if result["confidence"] < 0.5 and use_llm and api_key:
        llm_result = parse_intent_llm(user_input, api_key, base_url or "https://api.deepseek.com/v1")
        if not llm_result.get("error"):
            # LLM结果覆盖规则结果
            result.update(llm_result)
            result["method"] = "llm"

    return result


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 用户交互消息生成
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

FIELD_QUESTIONS = {
    "name": "请提供姓名",
    "title": "请提供职称/头衔",
    "company": "请提供公司名称",
    "contact": "请提供联系方式 (电话/邮箱/网站)",
    "city": "请提供城市名称",
    "text": "请提供需要显示的文字内容",
    "subject": "请描述您想要生成的图片内容",
    "room_description": "请描述房间的主题和布置",
    "region": "请提供地区名称 (国家/省份)",
    "brand_name": "请提供品牌名称",
    "title": "请提供作品标题",
}


def generate_confirmation_message(intent: dict) -> str:
    """根据解析结果生成用户确认消息"""
    parts = []

    scene_id = intent.get("scene_id")
    style = intent.get("style")
    subject = intent.get("subject", "")

    if scene_id and scene_id in SCENE_TEMPLATES:
        scene = SCENE_TEMPLATES[scene_id]
        parts.append(f"识别到您想要生成: **{scene['name']}**")
    else:
        parts.append(f"识别到您想要生成图片")

    if style:
        parts.append(f"风格: **{style}**")

    if subject:
        parts.append(f"主题: {subject}")

    # 缺失字段
    missing = intent.get("missing_fields", [])
    if missing:
        parts.append("\n需要您提供以下信息:")
        for field in missing:
            question = FIELD_QUESTIONS.get(field, f"请提供{field}")
            parts.append(f"  - {question}")

    return "\n".join(parts)
