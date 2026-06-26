#!/usr/bin/env python3
"""
V10.5 图片生成模板系统 — 场景模板 + 风格词典 + 结构化Prompt Builder + 智能美化器

作者: 圆规
GitHub: https://github.com/xyva-yuangui/beauty-image
License: MIT

基于 PicoTrex/Awesome-Nano-Banana-images 110+模板 + YouMind 10000+提示词库研究
V10.5 升级: 40+场景 / 30+风格 / 智能Prompt美化器(啊哈时刻)
"""

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 风格词典 (Style Dictionary)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STYLE_DICT = {
    # ── 艺术风格 ──
    "赛博朋克": {
        "keywords": "赛博朋克风格, 霓虹灯光, 深色背景, 蓝紫粉渐变, 全息投影, 高科技未来感",
        "lighting": "霓虹灯混合光, 彩色边缘光, 逆光剪影",
        "negative": "白天, 明亮, 自然光, 田园, 温暖色调",
    },
    "浮世绘": {
        "keywords": "日式浮世绘风格, 粗细变化的墨笔轮廓线, 传统木版画配色, 戏剧性动态构图",
        "lighting": "平面化光照, 无阴影, 传统绘画光",
        "negative": "写实, 3D渲染, 照片, 现代, 数码感",
    },
    "水墨画": {
        "keywords": "中国传统水墨画风格, 留白, 墨色浓淡变化, 宣纸质感, 写意笔法",
        "lighting": "散射柔光, 自然天光, 无强烈阴影",
        "negative": "色彩饱和, 数码感, 3D, 写实, 西方油画",
    },
    "吉卜力": {
        "keywords": "吉卜力动画风格, 手绘质感, 温暖色调, 自然光, 细腻的背景细节, 宫崎骏美学",
        "lighting": "柔和的自然日光, 黄金时段, 温暖侧光",
        "negative": "暗色, 恐怖, 写实, 3D, 赛博朋克",
    },
    "像素风": {
        "keywords": "像素艺术风格, 8-bit/16-bit, 有限调色板, 清晰像素块, 复古游戏美学",
        "lighting": "平面光, 无柔和渐变",
        "negative": "写实, 高清, 柔和, 3D, 照片级",
    },
    "油画": {
        "keywords": "古典油画风格, 厚重的笔触纹理, 丰富的色彩层次, 画布质感, 文艺复兴构图",
        "lighting": "戏剧性的伦勃朗光, 明暗对比, 暖色调主光",
        "negative": "平面, 数码, 简笔画, 卡通, 现代",
    },
    "漫画": {
        "keywords": "日本漫画风格, 清晰的线条, 大眼睛, 动态表现, 网点/速度线效果",
        "lighting": "平面阴影, 明确的光影分区, 高对比",
        "negative": "写实, 油画, 水彩, 照片, 模糊",
    },
    "清明上河图": {
        "keywords": "传统中国水墨彩绘手卷, 古旧绢本质感, 张择端散点透视, 界画建筑绘画技法",
        "lighting": "柔和复古大地色调, 传统绘画均匀光",
        "negative": "现代, 写实照片, 3D, 鲜艳色彩, 数码",
    },
    "波普艺术": {
        "keywords": "波普艺术风格, 大胆鲜艳色彩, 网点印刷效果, 安迪沃霍尔, 高对比重复图案",
        "lighting": "均匀平面光, 无阴影, 高饱和",
        "negative": "暗色, 柔和, 自然, 写实, 水墨",
    },

    # ── 材质风格 ──
    "水晶": {
        "keywords": "透明玻璃或水晶材质, 照片级真实, 高抛光, 折射效果, 圆润倒角, 光滑曲面",
        "lighting": "明亮干净的专业棚拍光, 锐利高光, 微妙折射, 光线穿透产生折射弯曲",
        "negative": "哑光, 粗糙, 木质, 金属, 暗色",
    },
    "毛绒": {
        "keywords": "柔软蓬松的毛绒质感, 超逼真毛发纹理, 柔和阴影, 漂浮于浅灰色背景",
        "lighting": "摄影棚灯光, 柔和散射, 温暖",
        "negative": "光滑, 金属, 坚硬, 锋利, 冰冷",
    },
    "充气": {
        "keywords": "充气玩具材质, 气球般圆润, 柔软光泽, 鲜艳色彩, 可爱",
        "lighting": "柔和均匀光, 微微反光, 童趣",
        "negative": "写实, 暗色, 恐怖, 金属, 锋利",
    },
    "乐高": {
        "keywords": "乐高积木风格, 方块化造型, 鲜艳塑料色彩, 乐高小人, 微缩场景",
        "lighting": "明亮均匀, 棚拍, 柔和阴影",
        "negative": "写实, 有机形态, 柔软, 自然",
    },
    "黏土": {
        "keywords": "黏土/橡皮泥风格, 手工捏制质感, 柔和的指纹痕迹, 饱和色彩, 定格动画美学",
        "lighting": "柔和的顶光, 微妙阴影, 温暖",
        "negative": "写实, 金属, 光滑, 数码, 锋利",
    },

    # ── 摄影风格 ──
    "电影感": {
        "keywords": "电影画面质感, 2.39:1宽银幕, 胶片颗粒, 电影调色, 浅景深",
        "lighting": "戏剧性侧光, 明暗对比, 伦勃朗光",
        "negative": "平面, 明亮均匀, 过曝, 数码感",
    },
    "产品摄影": {
        "keywords": "专业产品摄影, 干净白底/渐变背景, 精致布光, 商业级后期",
        "lighting": "三点布光, 柔和主光, 轮廓光, 反射板补光",
        "negative": "杂乱背景, 自然光, 噪点, 暗角, 低画质",
    },
    "街拍": {
        "keywords": "街头摄影风格, 自然随性, 城市背景, 浅景深, 35mm镜头感",
        "lighting": "自然光, 侧逆光, 黄金时段",
        "negative": "棚拍, 白底, 摆拍, 过度修饰",
    },
    "胶片": {
        "keywords": "复古胶片摄影, Kodak Portra色调, 柔和颗粒, 微微褪色, 温暖偏色",
        "lighting": "自然光, 柔和, 温暖色温",
        "negative": "数码感, 过于锐利, 高饱和, HDR, 冷色",
    },

    # ── 3D风格 ──
    "等距微缩": {
        "keywords": "等距3D微缩场景, 45°俯视视角, 精细建模, PBR材质, 卡通渲染",
        "lighting": "柔和全局光照, 环境光遮蔽, 微妙阴影",
        "negative": "平面, 写实, 照片, 第一人称, 俯拍",
    },
    "3D渲染": {
        "keywords": "高品质3D渲染, C4D/Blender风格, 光滑表面, 柔和渐变, 现代设计感",
        "lighting": "HDRI环境光, 柔和反射, 玻璃/金属质感",
        "negative": "平面, 粗糙, 噪点, 低多边形",
    },

    # ── V10.5 新增风格 (YouMind研究) ──
    "水彩": {
        "keywords": "水彩画风格, 透明色彩层叠, 湿润渗透效果, 画纸纹理, 自然水痕边缘, 柔和色彩过渡",
        "lighting": "柔和自然光, 透光感, 轻盈",
        "negative": "厚重, 油画, 数码, 锐利边缘, 高饱和",
    },
    "素描线稿": {
        "keywords": "铅笔素描风格, 精细线条, 交叉阴影线, 纸张纹理, 黑白灰层次, 手绘质感",
        "lighting": "单向定向光, 明确光影分区, 铅笔交叉线表达阴影",
        "negative": "彩色, 数码, 3D, 照片, 模糊",
    },
    "Q版萌系": {
        "keywords": "Q版风格, 超大头身比(2-3头身), 圆润可爱, 大眼睛, 简化肢体, 鲜艳配色, 萌系设计",
        "lighting": "明亮均匀, 无重阴影, 轻快",
        "negative": "写实, 恐怖, 暗色, 复杂, 细长比例",
    },
    "复古怀旧": {
        "keywords": "复古怀旧风格, 褪色胶片色调, 暖黄偏色, 老照片颗粒, 柔和边缘暗角, 60-80年代美学",
        "lighting": "温暖日光, 柔和侧光, 略微过曝",
        "negative": "数码感, 冷色, 高饱和, 现代, 锐利",
    },
    "极简主义": {
        "keywords": "极简主义设计, 大量留白, 几何形状, 有限色彩(2-3色), 克制构图, 高级感",
        "lighting": "均匀柔光, 无戏剧性阴影, 干净",
        "negative": "杂乱, 过度装饰, 多色, 复杂纹理, 繁琐",
    },
    "电影剧照": {
        "keywords": "电影剧照级画面, 宽银幕2.39:1, 电影调色LUT, 浅景深散焦光斑, 胶片颗粒, 戏剧张力",
        "lighting": "伦勃朗光/蝴蝶光, 面部高对比, 背光轮廓, 实际光源(practicals)",
        "negative": "平面光, 明亮均匀, 卡通, 过曝, 手机拍摄感",
    },
    "动漫插画": {
        "keywords": "日系动漫插画, 精致上色, 明亮色彩, 清晰线稿, 光影细腻, 背景氛围感强",
        "lighting": "逆光轮廓, 柔和面部光, 环境色反射, 丁达尔光线",
        "negative": "写实, 油画, 粗糙, 低画质, 变形",
    },
    "水墨插画": {
        "keywords": "现代水墨插画风格, 传统水墨与现代设计融合, 大胆留白, 笔触飞白, 点缀金色或朱红",
        "lighting": "散射天光, 空灵, 意境深远",
        "negative": "西方油画, 3D, 数码感, 高饱和, 杂乱",
    },
    "液态玻璃": {
        "keywords": "Apple液态玻璃风格, 85-90%透明度, 极细边框, 微妙投影, 浮动深度, 毛玻璃模糊背景, 现代UI美学",
        "lighting": "柔和环境光, 玻璃折射高光, 微妙焦散, 背景色反射",
        "negative": "不透明, 粗边框, 老旧, 粗糙, 暗色",
    },
    "全息镭射": {
        "keywords": "全息镭射效果, 彩虹色光谱, 金属材质底色, 光线角度变化产生色彩变幻, 高级感闪卡质感",
        "lighting": "多角度点光源, 彩虹反射, 高亮镜面",
        "negative": "哑光, 暗色, 自然, 朴素, 纸质",
    },
}

# 风格别名映射 (用户可能用的不同叫法)
STYLE_ALIASES = {
    "cyberpunk": "赛博朋克", "赛博": "赛博朋克", "科幻": "赛博朋克",
    "ukiyo-e": "浮世绘", "日式": "浮世绘",
    "ink": "水墨画", "国画": "水墨画", "中国画": "水墨画", "水墨": "水墨画",
    "ghibli": "吉卜力", "宫崎骏": "吉卜力", "动画": "吉卜力",
    "pixel": "像素风", "8bit": "像素风", "复古游戏": "像素风",
    "crystal": "水晶", "玻璃": "水晶", "透明": "水晶",
    "plush": "毛绒", "蓬松": "毛绒", "绒毛": "毛绒",
    "inflatable": "充气", "气球": "充气",
    "lego": "乐高", "积木": "乐高",
    "clay": "黏土", "橡皮泥": "黏土", "定格动画": "黏土",
    "cinematic": "电影感", "电影": "电影感",
    "product": "产品摄影", "产品": "产品摄影", "白底": "产品摄影",
    "street": "街拍", "抓拍": "街拍",
    "film": "胶片", "复古": "胶片",
    "isometric": "等距微缩", "微缩": "等距微缩", "小场景": "等距微缩",
    "3d": "3D渲染", "c4d": "3D渲染", "blender": "3D渲染",
    "油画": "油画", "古典": "油画",
    "manga": "漫画", "动漫": "漫画", "anime": "漫画",
    "pop art": "波普艺术", "波普": "波普艺术",
    "清明上河图": "清明上河图",
    "watercolor": "水彩", "水彩画": "水彩",
    "sketch": "素描线稿", "素描": "素描线稿", "线稿": "素描线稿", "pencil": "素描线稿",
    "chibi": "Q版萌系", "q版": "Q版萌系", "萌": "Q版萌系", "可爱": "Q版萌系",
    "retro": "复古怀旧", "vintage": "复古怀旧", "怀旧": "复古怀旧", "旧照片": "复古怀旧",
    "minimal": "极简主义", "极简": "极简主义", "简约": "极简主义",
    "film still": "电影剧照", "剧照": "电影剧照", "电影截图": "电影剧照",
    "anime": "动漫插画", "动漫": "动漫插画", "二次元": "动漫插画",
    "ink illustration": "水墨插画", "现代水墨": "水墨插画",
    "glass": "液态玻璃", "glassmorphism": "液态玻璃", "毛玻璃": "液态玻璃",
    "holographic": "全息镭射", "镭射": "全息镭射", "闪卡": "全息镭射", "彩虹": "全息镭射",
}


def resolve_style(style_name: str) -> dict | None:
    """解析风格名称, 返回风格词典条目"""
    if not style_name:
        return None
    name = style_name.strip().lower()
    # 直接匹配
    for key, val in STYLE_DICT.items():
        if key.lower() == name:
            return val
    # 别名匹配
    canonical = STYLE_ALIASES.get(name)
    if canonical and canonical in STYLE_DICT:
        return STYLE_DICT[canonical]
    # 模糊匹配 (包含关键词)
    for key, val in STYLE_DICT.items():
        if name in key.lower() or key.lower() in name:
            return val
    return None


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 场景模板 (Scene Templates)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SCENE_TEMPLATES = {
    # ── 商务 ──
    "biz_card": {
        "name": "名片设计",
        "category": "商务",
        "template": (
            "一张逼真的{style_desc}名片照片：左手拿着一张横向的亚克力无边框名片，"
            "尺寸与标准名片相同（3.5英寸×2英寸），几乎占据了整个画面。"
            "名片采用简洁的个人名片布局，没有任何横幅或背景图片。"
            "{style_detail}"
            "最终的名片应布局均衡、线条简洁、视觉层次清晰，适合专业印刷。"
            "姓名：{name} 职称：{title} 公司名称：{company}"
            "联系方式：{contact}"
        ),
        "required_fields": ["name"],
        "optional_fields": ["title", "company", "contact", "style"],
        "defaults": {"style": "赛博朋克", "title": "创始人", "company": "", "contact": ""},
        "engine": "seedream5", "fallback_engine": "seedream4",
        "size": "2K_16:9",
        "style_variants": {
            "赛博朋克": "它拥有光滑圆润的边缘，散发出柔和的霓虹光芒，并带有蓝色、粉色和紫色的渐变效果。背景采用深色虚化处理，以突出发光的边缘，营造出高科技的全息氛围。",
            "极简": "采用纯白色底色, 黑色文字, 极简主义设计, 大量留白, 仅保留必要信息。背景为干净的浅灰色。",
            "金属": "采用拉丝金属质感, 银色或深灰色底色, 压印凸起的文字, 边缘有精致的金色或银色线条。背景为暗色大理石桌面。",
        },
    },
    "biz_poster": {
        "name": "商业海报",
        "category": "商务",
        "template": (
            "一张专业的商业宣传海报设计，{style_desc}风格。"
            "主题：{subject}。"
            "海报采用{layout}布局，视觉层次清晰。"
            "主色调为{color_scheme}，搭配{mood}的整体氛围。"
            "{text_element}"
            "画面精致, 适合印刷和数字展示。"
        ),
        "required_fields": ["subject"],
        "optional_fields": ["style", "layout", "color_scheme", "mood", "text_element"],
        "defaults": {"style": "现代", "layout": "上图下文", "color_scheme": "品牌色", "mood": "专业", "text_element": ""},
        "engine": "seedream5", "fallback_engine": "seedream4",
        "size": "2K_9:16",
    },
    "biz_product": {
        "name": "产品摄影",
        "category": "商务",
        "template": (
            "一张专业级产品摄影照片，主体是{subject}。"
            "干净的{background}背景，产品位于画面中央。"
            "三点布光：柔和主光从左上方照射，轮廓光勾勒产品边缘，"
            "反射板从右下方补光，消除死角阴影。"
            "产品表面纹理清晰可见，材质质感真实。"
            "浅景深突出产品，背景柔和虚化。"
            "商业级后期调色，色彩准确还原。"
        ),
        "required_fields": ["subject"],
        "optional_fields": ["background"],
        "defaults": {"background": "纯白渐变"},
        "engine": "seedream4", "fallback_engine": "wanx",
        "size": "2K",
    },

    # ── 社交 ──
    "social_avatar": {
        "name": "头像/IP形象",
        "category": "社交",
        "template": (
            "一个精致的个人头像/IP形象设计，{style_desc}风格。"
            "人物描述：{subject}。"
            "表情{expression}，姿态自然。"
            "背景：{background}。"
            "整体风格统一，色彩和谐，适合社交媒体头像使用。"
            "高清细腻，细节丰富。"
        ),
        "required_fields": ["subject"],
        "optional_fields": ["style", "expression", "background"],
        "defaults": {"style": "3D渲染", "expression": "微笑, 友好", "background": "柔和纯色渐变"},
        "engine": "seedream4", "fallback_engine": "wanx",
        "size": "2K",
    },
    "social_emoji": {
        "name": "表情包",
        "category": "社交",
        "template": (
            "一个可爱的表情包设计：{subject}，"
            "表情为{expression}。"
            "风格：{style_desc}，夸张有趣。"
            "纯色背景，主体突出。"
            "适合作为聊天表情使用。"
        ),
        "required_fields": ["subject", "expression"],
        "optional_fields": ["style"],
        "defaults": {"style": "卡通"},
        "engine": "wanx", "fallback_engine": "seedream4",
        "size": "wanx_1:1",
    },
    "social_card": {
        "name": "金句卡片",
        "category": "社交",
        "template": (
            "一张精致的金句卡片设计。"
            "卡片上用优雅的字体写着：\"{text}\"。"
            "背景：{background}，配色{color_scheme}。"
            "排版精美, 文字清晰可读, 适合社交媒体分享。"
            "整体风格{mood}, 有质感。"
        ),
        "required_fields": ["text"],
        "optional_fields": ["background", "color_scheme", "mood"],
        "defaults": {"background": "渐变色或纹理底", "color_scheme": "温暖和谐", "mood": "文艺"},
        "engine": "wanx", "fallback_engine": "seedream4",
        "size": "wanx_1:1",
    },

    # ── 创意艺术 ──
    "art_general": {
        "name": "艺术创作",
        "category": "创意",
        "template": (
            "{style_desc}风格的艺术作品。"
            "主体：{subject}。"
            "{detail}"
            "{lighting_desc}"
            "画面精致，艺术感强烈，细节丰富。"
        ),
        "required_fields": ["subject"],
        "optional_fields": ["style", "detail"],
        "defaults": {"style": "油画", "detail": ""},
        "engine": "seedream5", "fallback_engine": "seedream4",
        "size": "2K",
    },

    # ── 3D/材质 ──
    "3d_crystal": {
        "name": "水晶质感",
        "category": "3D",
        "template": (
            "一幅照片级真实、细节高度丰富的图像，主体是{subject}，"
            "以清澈、抛光度极高的透明玻璃或水晶材质渲染而成。"
            "所有边缘采用圆润倒角与光滑曲面处理，在光线下产生优雅的折射效果。"
            "主体略微倾斜摆放，仿佛漂浮在洁净的淡米白色棚拍背景上方。"
            "照明为明亮、干净的专业棚拍光，重点突出玻璃材质的透明性、镜面反射与折射特性。"
            "高调光感与浅景深处理，主体保持绝对清晰焦点，背景柔和虚化。"
        ),
        "required_fields": ["subject"],
        "optional_fields": [],
        "defaults": {},
        "engine": "seedream5", "fallback_engine": "seedream4",
        "size": "2K",
    },
    "3d_plush": {
        "name": "毛绒玩具",
        "category": "3D",
        "template": (
            "将{subject}转换成一个柔软蓬松的3D立体物体。"
            "使用原有颜色。该物体完全被毛发覆盖，"
            "拥有超逼真的毛发纹理和柔和的阴影。"
            "它位于干净的浅灰色背景中央，轻柔地漂浮在空中。"
            "风格超现实、触感丰富且现代，营造出舒适和趣味盎然的感觉。"
            "采用摄影棚灯光和高分辨率渲染。"
        ),
        "required_fields": ["subject"],
        "optional_fields": [],
        "defaults": {},
        "engine": "seedream4", "fallback_engine": "seedream5",
        "size": "2K",
    },
    "3d_inflatable": {
        "name": "充气玩具",
        "category": "3D",
        "template": (
            "将{subject}转换成一个可爱的充气玩具风格3D物体。"
            "材质为光滑的气球般质感, 圆润饱满, 色彩鲜艳。"
            "物体略微漂浮在空中, 带有轻微的反光。"
            "背景为干净的纯色, 柔和的环境光照。"
            "整体风格可爱、趣味十足, 高分辨率渲染。"
        ),
        "required_fields": ["subject"],
        "optional_fields": [],
        "defaults": {},
        "engine": "seedream4", "fallback_engine": "seedream5",
        "size": "2K",
    },
    "3d_miniature": {
        "name": "等距微缩房间",
        "category": "3D",
        "template": (
            "一个等距3D立方体微缩房间（浅切面真立方体；所有物品均严格包含在立方体内）。"
            "房间描述：{room_description}。"
            "{character_desc}"
            "光照：{atmosphere}；逼真的反射和彩色阴影。"
            "视角：略微抬高的等距四分之三视角，立方体正面边缘居中；"
            "没有任何元素突出于立方体之外。"
            "照片级材质，细节丰富；中性背景。无水印。"
        ),
        "required_fields": ["room_description"],
        "optional_fields": ["character_desc", "atmosphere"],
        "defaults": {"character_desc": "", "atmosphere": "温暖日光"},
        "engine": "seedream5", "fallback_engine": "seedream4",
        "size": "2K",
    },

    # ── 实用 ──
    "util_weather": {
        "name": "城市天气卡片",
        "category": "实用",
        "template": (
            "呈现一个清晰的45°俯视视角，垂直（9:16）等距3D微缩卡通场景，"
            "突出画面中心{city}的标志性地标，展现精细的建模。"
            "场景采用柔和细腻的纹理，搭配逼真的PBR材质和柔和逼真的光影效果。"
            "天气元素巧妙地融入城市建筑，营造身临其境的天气氛围。"
            "使用简洁统一的构图，采用极简主义美学，柔和纯色背景。"
            "在顶部中心醒目位置显示天气图标，下方显示日期和温度范围。"
            "城市名称({city})位于天气图标正上方。"
        ),
        "required_fields": ["city"],
        "optional_fields": [],
        "defaults": {},
        "engine": "seedream5", "fallback_engine": "seedream4",
        "size": "2K_9:16",
    },
    "util_fridge_magnet": {
        "name": "城市冰箱贴",
        "category": "实用",
        "template": (
            "展示一张清晰的俯视图，照片内容为{city}地标建筑的3D磁贴，"
            "磁贴需整齐排列成平行线和直角，呈小山状。"
            "这些磁贴需为逼真的微缩模型。"
            "在顶部中央放置一个印有城市名称的纪念磁贴，"
            "以及一张手写便签，上面写着温度和天气状况。"
            "所有物品不得重复。"
        ),
        "required_fields": ["city"],
        "optional_fields": [],
        "defaults": {},
        "engine": "seedream5", "fallback_engine": "seedream4",
        "size": "2K",
    },
    "util_food_map": {
        "name": "美食地图",
        "category": "实用",
        "template": (
            "制作一张{region}地图，地图上每个区域都用该区域最著名的食物来构成"
            "（各区域地图上的图案应该看起来像是由食物组成的，而不是食物的图片）。"
            "仔细检查，确保每个区域都正确无误。"
            "色彩丰富, 细节精致, 俯视视角。"
        ),
        "required_fields": ["region"],
        "optional_fields": [],
        "defaults": {},
        "engine": "seedream5", "fallback_engine": "seedream4",
        "size": "2K",
    },
    "util_storyboard": {
        "name": "电影分镜",
        "category": "实用",
        "template": (
            "使用宽屏面板，为{title}创作电影分镜脚本。"
            "场景描述：{scene_description}。"
            "包含{panel_count}个分镜格子，每格标注镜头类型。"
            "风格为黑白铅笔素描，带简要的镜头说明文字。"
        ),
        "required_fields": ["title"],
        "optional_fields": ["scene_description", "panel_count"],
        "defaults": {"scene_description": "开场场景", "panel_count": "6"},
        "engine": "seedream5", "fallback_engine": "seedream4",
        "size": "2K_16:9",
    },

    # ── 设计 ──
    "design_ppt": {
        "name": "PPT页面",
        "category": "设计",
        "template": (
            "一页精美的PPT幻灯片设计。"
            "内容主题：{subject}。"
            "设计风格：{style_desc}。"
            "背景使用{background}，"
            "标题使用优雅的字体，正文使用现代无衬线体。"
            "配色：{color_scheme}。"
            "视觉元素：注重排版的网格布局，关键信息使用卡片布局。"
            "一页一张图，不要将PPT变成一整张图片。"
        ),
        "required_fields": ["subject"],
        "optional_fields": ["style", "background", "color_scheme"],
        "defaults": {"style": "温暖学术", "background": "暖米色/奶油色底色", "color_scheme": "赤陶红+芥末黄+深海军蓝"},
        "engine": "seedream5", "fallback_engine": "seedream4",
        "size": "2K_16:9",
    },
    "design_logo": {
        "name": "Logo设计",
        "category": "设计",
        "template": (
            "一个专业的Logo设计，品牌名称：{brand_name}。"
            "风格：{style_desc}，{mood}。"
            "配色：{color_scheme}。"
            "Logo应简洁易识别，适合多种尺寸使用。"
            "纯白色背景，高清矢量感。"
        ),
        "required_fields": ["brand_name"],
        "optional_fields": ["style", "mood", "color_scheme"],
        "defaults": {"style": "极简现代", "mood": "专业可信赖", "color_scheme": "品牌色"},
        "engine": "wanx", "fallback_engine": "seedream4",
        "size": "wanx_1:1",
    },
    "design_packaging": {
        "name": "包装设计",
        "category": "设计",
        "template": (
            "一个精美的产品包装设计，产品：{subject}。"
            "包装风格：{style_desc}。"
            "展示方式：{display}，能看到包装的多个面。"
            "材质：{material}，印刷品质感。"
            "配色：{color_scheme}，整体协调。"
        ),
        "required_fields": ["subject"],
        "optional_fields": ["style", "display", "material", "color_scheme"],
        "defaults": {"style": "现代简约", "display": "45°角立体展示", "material": "哑光纸盒", "color_scheme": "清新自然"},
        "engine": "seedream5", "fallback_engine": "seedream4",
        "size": "2K",
    },

    # ── 人物 ──
    "person_portrait": {
        "name": "写实肖像",
        "category": "人物",
        "template": (
            "一张专业的人物肖像摄影，{subject}。"
            "光照：{lighting}。"
            "背景：{background}。"
            "表情自然，眼神有神，皮肤纹理真实。"
            "浅景深, 焦点在眼睛上, 专业后期调色。"
        ),
        "required_fields": ["subject"],
        "optional_fields": ["lighting", "background"],
        "defaults": {"lighting": "柔和的窗户侧光, 自然暖调", "background": "虚化的室内环境"},
        "engine": "seedream5", "fallback_engine": "seedream4",
        "size": "2K_3:4",
    },
    "person_action_figure": {
        "name": "手办/模型",
        "category": "人物",
        "template": (
            "一个精致的手办/模型设计，角色：{subject}。"
            "材质为哑光PVC，头部较大，身体较小，Q版/手办风格。"
            "动作：{action}，表情：{expression}。"
            "底座：{base}。"
            "摄影棚灯光，高分辨率，产品级展示。"
        ),
        "required_fields": ["subject"],
        "optional_fields": ["action", "expression", "base"],
        "defaults": {"action": "站立", "expression": "微笑", "base": "圆形黑色底座"},
        "engine": "seedream5", "fallback_engine": "seedream4",
        "size": "2K",
    },

    # ── 场景 ──
    "scene_chalkboard": {
        "name": "黑板粉笔画",
        "category": "场景",
        "template": (
            "将{subject}用粉笔在黑板上绘制，使用彩色粉笔。"
            "从某个角度拍摄了黑板，场景来自{setting}。"
            "黑板靠墙放置，{surroundings}在旁边。"
            "插图旁边用粉笔写着\"{text}\"。"
            "粉笔画风格保持手绘感，有适度的粉笔粉末飞散效果。"
        ),
        "required_fields": ["subject"],
        "optional_fields": ["setting", "surroundings", "text"],
        "defaults": {"setting": "教室", "surroundings": "老师的桌子", "text": ""},
        "engine": "seedream4", "fallback_engine": "seedream5",
        "size": "2K_16:9",
    },

    # ── 电商 ──
    "ecom_main": {
        "name": "电商主图",
        "category": "电商",
        "template": (
            "一张电商产品主图，产品：{subject}。"
            "纯白色背景，产品居中，占画面70%左右。"
            "柔和均匀的布光，消除硬阴影。"
            "产品细节清晰，色彩还原准确。"
            "适合电商平台展示的专业产品照片。"
        ),
        "required_fields": ["subject"],
        "optional_fields": [],
        "defaults": {},
        "engine": "wanx", "fallback_engine": "seedream4",
        "size": "wanx_1:1",
    },
    "ecom_banner": {
        "name": "电商横幅",
        "category": "电商",
        "template": (
            "一张电商促销横幅设计，主题：{subject}。"
            "包含产品展示和{text}促销文字。"
            "配色：{color_scheme}，整体风格{mood}。"
            "横幅比例16:9，适合店铺首页展示。"
        ),
        "required_fields": ["subject"],
        "optional_fields": ["text", "color_scheme", "mood"],
        "defaults": {"text": "限时优惠", "color_scheme": "红金/品牌色", "mood": "热烈喜庆"},
        "engine": "wanx", "fallback_engine": "seedream4",
        "size": "wanx_16:9",
    },

    # ── 内容创作 ──
    "content_xhs": {
        "name": "小红书配图",
        "category": "内容",
        "template": (
            "一张精致的Instagram/小红书风格配图，"
            "主题：{subject}。"
            "整体色调温暖柔和，带有轻微的胶片颗粒感。"
            "构图采用{composition}，突出主体。"
            "画面散发出{mood}的氛围。"
            "色彩倾向于{color_scheme}，搭配自然柔光。"
            "适合社交媒体分享的高质量画面。"
        ),
        "required_fields": ["subject"],
        "optional_fields": ["composition", "mood", "color_scheme"],
        "defaults": {"composition": "居中或三分法", "mood": "温暖治愈", "color_scheme": "奶茶色系/莫兰迪色"},
        "engine": "seedream4", "fallback_engine": "wanx",
        "size": "2K_3:4",
    },
    "content_blog": {
        "name": "文章头图",
        "category": "内容",
        "template": (
            "一张文章头图设计，主题：{subject}。"
            "风格简洁现代，{style_desc}。"
            "画面有足够的留白空间可放置标题文字。"
            "配色：{color_scheme}。"
            "横幅比例16:9, 适合博客/公众号头图。"
        ),
        "required_fields": ["subject"],
        "optional_fields": ["style", "color_scheme"],
        "defaults": {"style": "扁平插画", "color_scheme": "蓝绿渐变"},
        "engine": "wanx", "fallback_engine": "seedream4",
        "size": "wanx_16:9",
    },

    # ── V10.5 新增场景 (YouMind研究) ──
    "info_bento": {
        "name": "Bento产品信息图",
        "category": "信息图",
        "template": (
            "创建一个包含8个模块的高品质液态玻璃Bento网格产品信息图。"
            "产品：{subject}。"
            "调色板源自产品的自然主色调，强调色为完全饱和的主色调。"
            "视觉风格：主打产品以真实摄影呈现，占28-30%面积。"
            "卡片采用Apple液态玻璃效果(85-90%透明)，带极细边框和微妙阴影，营造浮动深度。"
            "背景为产品精髓的柔和焦散或抽象光晕，高度模糊。"
            "8个模块：M1主打产品展示+名称，M2核心优势(4点+图标)，"
            "M3使用方法(4种+图标)，M4关键指标(5个数据点)，"
            "M5适用人群(4推荐+3注意)，M6重要提示(4项+警告图标)，"
            "M7快速参考，M8趣味知识(3个事实)。"
            "不对称Bento网格，16:9横向，超高品质液态玻璃信息图。"
        ),
        "required_fields": ["subject"],
        "optional_fields": [],
        "defaults": {},
        "engine": "seedream5", "fallback_engine": "seedream4",
        "size": "2K_16:9",
    },
    "info_comparison": {
        "name": "对比信息图",
        "category": "信息图",
        "template": (
            "一张精美的对比信息图，主题：{subject}。"
            "左右分栏设计，左侧展示{option_a}，右侧展示{option_b}。"
            "中间用VS或分隔线区分。"
            "每侧包含关键数据、优势图标和简要说明。"
            "整体配色：左侧{color_a}，右侧{color_b}。"
            "底部有总结推荐。16:9横向，信息层次清晰。"
        ),
        "required_fields": ["subject", "option_a", "option_b"],
        "optional_fields": ["color_a", "color_b"],
        "defaults": {"color_a": "蓝色系", "color_b": "橙色系"},
        "engine": "seedream5", "fallback_engine": "seedream4",
        "size": "2K_16:9",
    },
    "social_quote_portrait": {
        "name": "肖像金句卡",
        "category": "社交",
        "template": (
            "一张宽幅引言卡片，上面印有一位名人的肖像。"
            "背景为{bg_color}，引言文字为浅金色衬线字体："
            "\"{text}\"，下方是较小的文字：\"—{author}\"。"
            "文字前面有一个大而柔和的引号。"
            "人物肖像在左侧，文字在右侧。"
            "文字占据图片的三分之二，肖像占据三分之一，"
            "肖像部分带有轻微的渐变过渡效果。"
            "人物描述：{subject}。"
        ),
        "required_fields": ["text"],
        "optional_fields": ["author", "subject", "bg_color"],
        "defaults": {"author": "", "subject": "一位睿智的思想家", "bg_color": "深棕色"},
        "engine": "seedream5", "fallback_engine": "seedream4",
        "size": "2K_16:9",
    },
    "social_youtube_thumb": {
        "name": "YouTube缩略图",
        "category": "社交",
        "template": (
            "一张引人注目的YouTube视频缩略图，16:9比例。"
            "主题：{subject}。"
            "画面左侧是{person_desc}，表情夸张{expression}。"
            "右侧有大号粗体文字\"{title_text}\"，"
            "字体颜色{text_color}，带有描边和阴影效果。"
            "背景使用{background}，整体色彩鲜艳饱和，"
            "视觉冲击力强，能在小尺寸下吸引点击。"
        ),
        "required_fields": ["subject"],
        "optional_fields": ["person_desc", "expression", "title_text", "text_color", "background"],
        "defaults": {"person_desc": "一位博主", "expression": "惊讶张嘴", "title_text": "", "text_color": "黄色", "background": "渐变色+光效"},
        "engine": "seedream5", "fallback_engine": "seedream4",
        "size": "2K_16:9",
    },
    "photo_food": {
        "name": "美食摄影",
        "category": "摄影",
        "template": (
            "一张令人垂涎的美食摄影照片，菜品：{subject}。"
            "45°俯视角度，浅景深对焦在菜品主体。"
            "餐具和摆盘精致考究，{tableware}。"
            "背景为{background}，自然光从窗户侧面照射。"
            "菜品色泽饱满诱人，能看到食物的纹理和热气。"
            "色调温暖，整体氛围{mood}。"
            "专业美食摄影级画质，ISO低，锐度高。"
        ),
        "required_fields": ["subject"],
        "optional_fields": ["tableware", "background", "mood"],
        "defaults": {"tableware": "白色陶瓷餐盘搭配木质餐垫", "background": "木质桌面搭配绿植", "mood": "温馨家常"},
        "engine": "seedream4", "fallback_engine": "seedream5",
        "size": "2K",
    },
    "photo_fashion": {
        "name": "时尚大片",
        "category": "摄影",
        "template": (
            "一张高端时尚杂志级人像大片。"
            "模特描述：{subject}。"
            "穿着{outfit}，姿态{pose}。"
            "拍摄场景：{location}。"
            "光照：{lighting}。"
            "风格参考：Vogue/ELLE杂志封面级别。"
            "浅景深，肤色通透，妆容精致，画面有张力。"
        ),
        "required_fields": ["subject"],
        "optional_fields": ["outfit", "pose", "location", "lighting"],
        "defaults": {"outfit": "高级定制时装", "pose": "自信优雅", "location": "极简主义摄影棚", "lighting": "大型柔光箱主光+轮廓光"},
        "engine": "seedream5", "fallback_engine": "seedream4",
        "size": "2K_3:4",
    },
    "photo_landscape": {
        "name": "风光大片",
        "category": "摄影",
        "template": (
            "一张震撼的风光摄影大片。"
            "场景：{subject}。"
            "时间：{time_of_day}。"
            "天空状态：{sky}。"
            "前景有{foreground}引导视线。"
            "使用超广角16mm镜头感，极大景深，"
            "前景到远景都保持锐利。"
            "色彩丰富层次分明，光影戏剧性。"
            "风光摄影大师级构图，三分法或引导线构图。"
        ),
        "required_fields": ["subject"],
        "optional_fields": ["time_of_day", "sky", "foreground"],
        "defaults": {"time_of_day": "黄金时段日落", "sky": "火烧云", "foreground": "岩石或花丛"},
        "engine": "seedream5", "fallback_engine": "seedream4",
        "size": "2K_16:9",
    },
    "game_character": {
        "name": "游戏角色立绘",
        "category": "游戏",
        "template": (
            "一张高品质游戏角色立绘设计。"
            "角色：{subject}。"
            "职业/类型：{role}。"
            "装备/服饰：{outfit}。"
            "动作姿态：{pose}。"
            "画风：{style_desc}，色彩鲜明，线条流畅。"
            "角色占据画面主体，透明或简洁背景。"
            "适合作为游戏角色选择界面或卡牌使用。"
        ),
        "required_fields": ["subject"],
        "optional_fields": ["role", "outfit", "pose", "style"],
        "defaults": {"role": "战士", "outfit": "精致铠甲", "pose": "战斗准备", "style": "动漫插画"},
        "engine": "seedream5", "fallback_engine": "seedream4",
        "size": "2K_3:4",
    },
    "design_app_mockup": {
        "name": "App界面展示",
        "category": "设计",
        "template": (
            "一张精美的App界面设计展示图。"
            "App类型：{subject}。"
            "展示方式：{display}手机屏幕，{angle}角度。"
            "界面风格：{style_desc}，配色{color_scheme}。"
            "屏幕内容展示{screen_content}。"
            "背景为{background}，整体画面现代精致。"
            "适合产品发布或App Store展示。"
        ),
        "required_fields": ["subject"],
        "optional_fields": ["display", "angle", "style", "color_scheme", "screen_content", "background"],
        "defaults": {"display": "iPhone 16 Pro", "angle": "微微倾斜15°", "style": "极简主义", "color_scheme": "蓝紫渐变", "screen_content": "核心功能页面", "background": "柔和渐变色"},
        "engine": "seedream5", "fallback_engine": "seedream4",
        "size": "2K",
    },
    "content_comic": {
        "name": "漫画条",
        "category": "内容",
        "template": (
            "一条4格漫画，主题：{subject}。"
            "第1格：{panel1}。"
            "第2格：{panel2}。"
            "第3格：{panel3}。"
            "第4格：{panel4}。"
            "风格：{style_desc}，线条清晰，表情夸张有趣。"
            "每格有对话气泡，排版从左到右。"
            "整体横向排列，16:9比例。"
        ),
        "required_fields": ["subject"],
        "optional_fields": ["panel1", "panel2", "panel3", "panel4", "style"],
        "defaults": {"panel1": "日常场景", "panel2": "发生转折", "panel3": "出乎意料", "panel4": "搞笑结尾", "style": "漫画"},
        "engine": "seedream5", "fallback_engine": "seedream4",
        "size": "2K_16:9",
    },
    "design_invitation": {
        "name": "邀请函/贺卡",
        "category": "设计",
        "template": (
            "一张精美的{occasion}邀请函/贺卡设计。"
            "主要文字：\"{text}\"。"
            "风格：{style_desc}。"
            "装饰元素：{decoration}。"
            "配色：{color_scheme}。"
            "整体典雅有质感，印刷级品质。"
            "竖版3:4比例。"
        ),
        "required_fields": ["occasion"],
        "optional_fields": ["text", "style", "decoration", "color_scheme"],
        "defaults": {"text": "", "style": "现代典雅", "decoration": "花卉与金色线条", "color_scheme": "白色+金色+深绿"},
        "engine": "seedream4", "fallback_engine": "wanx",
        "size": "2K_3:4",
    },
    "design_book_cover": {
        "name": "书籍封面",
        "category": "设计",
        "template": (
            "一个专业的书籍封面设计。"
            "书名：\"{title}\"。"
            "作者：{author}。"
            "类型：{genre}。"
            "视觉主体：{subject}。"
            "风格：{style_desc}。"
            "封面构图：上方留白放书名(大号字体)，"
            "中间为视觉主体，底部放作者名。"
            "整体有文学气质，适合出版物使用。竖版2:3比例。"
        ),
        "required_fields": ["title"],
        "optional_fields": ["author", "genre", "subject", "style"],
        "defaults": {"author": "", "genre": "文学", "subject": "抽象艺术元素", "style": "极简主义"},
        "engine": "seedream5", "fallback_engine": "seedream4",
        "size": "2K_3:4",
    },
    "social_carousel": {
        "name": "社媒轮播图",
        "category": "社交",
        "template": (
            "一张适合社交媒体轮播的知识卡片，序号{slide_num}。"
            "主题：{subject}。"
            "本页内容：{content}。"
            "风格：{style_desc}，配色{color_scheme}。"
            "排版：大标题+分点内容+配图/图标。"
            "1:1正方形比例，文字清晰可读，"
            "视觉统一，适合Instagram/小红书轮播。"
        ),
        "required_fields": ["subject", "content"],
        "optional_fields": ["slide_num", "style", "color_scheme"],
        "defaults": {"slide_num": "1/5", "style": "现代简约", "color_scheme": "柔和渐变"},
        "engine": "wanx", "fallback_engine": "seedream4",
        "size": "wanx_1:1",
    },
    "content_meme": {
        "name": "表情包/梗图",
        "category": "内容",
        "template": (
            "一张搞笑的网络梗图/表情包。"
            "场景：{subject}。"
            "上方文字：\"{top_text}\"。"
            "下方文字：\"{bottom_text}\"。"
            "风格：{style_desc}，表情夸张，画面简洁有趣。"
            "白色粗体Impact字体，带黑色描边。"
            "1:1正方形比例。"
        ),
        "required_fields": ["subject"],
        "optional_fields": ["top_text", "bottom_text", "style"],
        "defaults": {"top_text": "", "bottom_text": "", "style": "写实搞笑"},
        "engine": "wanx", "fallback_engine": "seedream4",
        "size": "wanx_1:1",
    },

    # ── 浮世绘闪卡 (特色模板) ──
    "art_ukiyoe_card": {
        "name": "浮世绘闪卡",
        "category": "创意",
        "template": (
            "一张日式浮世绘风格的收藏级集换式卡牌设计，竖构图。"
            "插画风格紧密模仿传统浮世绘的视觉美学："
            "粗细变化的墨笔轮廓线、传统木版画的配色方案，以及戏剧性的动态构图。"
            "卡牌主角是{subject}，处于{pose}。"
            "周围环绕着{visual_effects}，以传统日式水墨画风格呈现。"
            "背景融合纹理化的镭射闪卡效果，在传统水墨元素下方闪烁。"
            "边框为日本传统纹样（青海波或麻叶纹）组成的装饰性边框。"
            "底部有风格化横幅，上面用古朴的书法写着\"{text}\"。"
        ),
        "required_fields": ["subject"],
        "optional_fields": ["pose", "visual_effects", "text"],
        "defaults": {"pose": "动态战斗姿势", "visual_effects": "火焰和能量光环", "text": ""},
        "engine": "seedream5", "fallback_engine": "seedream4",
        "size": "2K_3:4",
    },
}

# 场景别名映射
SCENE_ALIASES = {
    "名片": "biz_card", "business card": "biz_card", "card": "biz_card",
    "海报": "biz_poster", "poster": "biz_poster", "宣传图": "biz_poster",
    "产品图": "biz_product", "产品照": "biz_product", "product": "biz_product",
    "头像": "social_avatar", "avatar": "social_avatar", "ip": "social_avatar", "ip形象": "social_avatar",
    "表情包": "social_emoji", "emoji": "social_emoji", "sticker": "social_emoji",
    "金句": "social_card", "卡片": "social_card", "quote": "social_card",
    "水晶": "3d_crystal", "crystal": "3d_crystal", "玻璃": "3d_crystal",
    "毛绒": "3d_plush", "plush": "3d_plush", "蓬松": "3d_plush",
    "充气": "3d_inflatable", "inflatable": "3d_inflatable",
    "微缩": "3d_miniature", "miniature": "3d_miniature", "等距": "3d_miniature", "小房间": "3d_miniature",
    "天气": "util_weather", "weather": "util_weather",
    "冰箱贴": "util_fridge_magnet", "fridge": "util_fridge_magnet",
    "美食地图": "util_food_map", "food map": "util_food_map",
    "分镜": "util_storyboard", "storyboard": "util_storyboard",
    "ppt": "design_ppt", "幻灯片": "design_ppt",
    "logo": "design_logo", "标志": "design_logo",
    "包装": "design_packaging", "packaging": "design_packaging",
    "肖像": "person_portrait", "portrait": "person_portrait", "写真": "person_portrait",
    "手办": "person_action_figure", "模型": "person_action_figure", "figure": "person_action_figure",
    "黑板": "scene_chalkboard", "粉笔画": "scene_chalkboard",
    "电商": "ecom_main", "主图": "ecom_main", "白底图": "ecom_main",
    "横幅": "ecom_banner", "banner": "ecom_banner",
    "小红书": "content_xhs", "xhs": "content_xhs",
    "头图": "content_blog", "blog": "content_blog", "公众号": "content_blog",
    "浮世绘": "art_ukiyoe_card",
    "信息图": "info_bento", "bento": "info_bento", "产品介绍": "info_bento",
    "对比图": "info_comparison", "vs": "info_comparison", "对比": "info_comparison",
    "金句卡": "social_quote_portrait", "引言卡": "social_quote_portrait", "quote card": "social_quote_portrait",
    "缩略图": "social_youtube_thumb", "youtube": "social_youtube_thumb", "封面图": "social_youtube_thumb",
    "美食": "photo_food", "食物": "photo_food", "food": "photo_food", "菜品": "photo_food",
    "时尚": "photo_fashion", "fashion": "photo_fashion", "模特": "photo_fashion",
    "风景": "photo_landscape", "landscape": "photo_landscape", "风光": "photo_landscape",
    "游戏角色": "game_character", "立绘": "game_character", "角色": "game_character",
    "app": "design_app_mockup", "界面": "design_app_mockup", "mockup": "design_app_mockup",
    "漫画条": "content_comic", "四格漫画": "content_comic", "comic": "content_comic",
    "邀请函": "design_invitation", "贺卡": "design_invitation", "请柬": "design_invitation",
    "封面": "design_book_cover", "book": "design_book_cover", "书封": "design_book_cover",
    "轮播": "social_carousel", "carousel": "social_carousel", "知识卡片": "social_carousel",
    "梗图": "content_meme", "meme": "content_meme",
}


def resolve_scene(scene_hint: str) -> dict | None:
    """根据场景提示解析模板"""
    if not scene_hint:
        return None
    hint = scene_hint.strip().lower()
    # 直接ID匹配
    if hint in SCENE_TEMPLATES:
        return SCENE_TEMPLATES[hint]
    # 别名匹配
    scene_id = SCENE_ALIASES.get(hint)
    if scene_id and scene_id in SCENE_TEMPLATES:
        return SCENE_TEMPLATES[scene_id]
    # 模糊匹配
    for alias, sid in SCENE_ALIASES.items():
        if alias in hint or hint in alias:
            return SCENE_TEMPLATES.get(sid)
    return None


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 通用负面提示词
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

BASE_NEGATIVE = "低分辨率，低画质，肢体畸形，手指畸形，蜡像感，构图混乱，文字模糊"

QUALITY_NEGATIVE = {
    "high": "低分辨率，低画质，肢体畸形，手指畸形，画面过饱和，蜡像感，人脸无细节，过度光滑，AI感明显，构图混乱，文字模糊扭曲，噪点，模糊，过曝，欠曝",
    "standard": BASE_NEGATIVE,
}

QUALITY_SUFFIX = {
    "high": {
        "zh": "，高清细腻，光影层次丰富，构图精美，色彩和谐，专业摄影级画质，8K超高清",
        "en": ", ultra high definition, rich lighting and shadows, exquisite composition, harmonious colors, professional photography quality, 8K UHD",
    },
    "standard": {
        "zh": "，画面清晰，构图合理",
        "en": ", clear image, good composition",
    },
}


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Prompt Builder
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def build_prompt(scene_id: str | None, style_name: str | None,
                 fields: dict, quality: str = "high") -> dict:
    """构建结构化prompt

    返回:
        {
            "prompt": str,          # 最终prompt
            "negative": str,        # 负面提示词
            "engine": str,          # 推荐引擎
            "fallback_engine": str, # 备选引擎
            "size": str,            # 推荐尺寸
            "scene_name": str,      # 场景名称
        }
    """
    scene = None
    if scene_id:
        scene = SCENE_TEMPLATES.get(scene_id) or resolve_scene(scene_id)

    style = resolve_style(style_name) if style_name else None

    # ── 有模板: 填充模板 ──
    if scene:
        template = scene["template"]
        # 准备字段 (defaults + user fields)
        merged = dict(scene.get("defaults", {}))
        merged.update({k: v for k, v in fields.items() if v})

        # 风格描述注入
        if style:
            merged.setdefault("style_desc", style["keywords"])
            merged.setdefault("lighting_desc", style["lighting"])
        else:
            merged.setdefault("style_desc", merged.get("style", "精美"))
            merged.setdefault("lighting_desc", "柔和自然光")

        # 处理名片风格变体
        if scene_id == "biz_card" and "style_variants" in scene:
            variant_style = merged.get("style", "赛博朋克")
            merged["style_detail"] = scene["style_variants"].get(
                variant_style, scene["style_variants"].get("赛博朋克", ""))

        # 填充模板
        try:
            prompt = template.format(**merged)
        except KeyError as e:
            # 缺少字段时, 用空字符串填充
            import re
            prompt = re.sub(r'\{(\w+)\}', lambda m: merged.get(m.group(1), ''), template)

        # 负面提示
        negative_parts = [QUALITY_NEGATIVE.get(quality, BASE_NEGATIVE)]
        if style and style.get("negative"):
            negative_parts.append(style["negative"])
        negative = "，".join(negative_parts)

        return {
            "prompt": prompt,
            "negative": negative,
            "engine": scene.get("engine", "seedream4"),
            "fallback_engine": scene.get("fallback_engine", "wanx"),
            "size": scene.get("size", "2K"),
            "scene_name": scene["name"],
        }

    # ── 无模板: 通用构建 ──
    subject = fields.get("subject", "")
    prompt_parts = []

    if style:
        prompt_parts.append(f"{style['keywords']}风格的作品。")
        prompt_parts.append(f"主体：{subject}。")
        prompt_parts.append(f"光照：{style['lighting']}。")
    else:
        prompt_parts.append(subject)

    # 质量后缀
    has_chinese = any('\u4e00' <= c <= '\u9fff' for c in subject)
    lang = "zh" if has_chinese else "en"
    suffix = QUALITY_SUFFIX.get(quality, QUALITY_SUFFIX["standard"])[lang]
    if "8K" not in subject and "高清" not in subject:
        prompt_parts.append(suffix)

    prompt = "".join(prompt_parts)

    negative_parts = [QUALITY_NEGATIVE.get(quality, BASE_NEGATIVE)]
    if style and style.get("negative"):
        negative_parts.append(style["negative"])
    negative = "，".join(negative_parts)

    return {
        "prompt": prompt,
        "negative": negative,
        "engine": "seedream4",
        "fallback_engine": "wanx",
        "size": "2K",
        "scene_name": "通用",
    }


def list_scenes() -> list[dict]:
    """列出所有可用场景模板"""
    result = []
    for sid, scene in SCENE_TEMPLATES.items():
        result.append({
            "id": sid,
            "name": scene["name"],
            "category": scene["category"],
            "required_fields": scene["required_fields"],
            "engine": scene["engine"],
            "size": scene["size"],
        })
    return result


def list_styles() -> list[str]:
    """列出所有可用风格"""
    return list(STYLE_DICT.keys())


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# V10.5 智能Prompt美化器 (啊哈时刻)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

_BEAUTIFY_DIMENSIONS = {
    "composition": [
        "三分法构图，主体位于黄金分割点",
        "居中对称构图，庄重感",
        "对角线引导构图，动态感",
        "前中后三层景深，空间感",
        "留白构图，呼吸感",
        "框架构图，通过自然框架聚焦主体",
    ],
    "lighting": [
        "黄金时段侧光，温暖长影",
        "柔和的窗户自然光，逆光轮廓",
        "戏剧性伦勃朗光，明暗对比强烈",
        "环境光+补光，柔和无硬阴影",
        "顶光+反射板，立体感",
        "丁达尔光线穿透，神圣氛围",
    ],
    "color_mood": [
        "暖色调为主，橙红金，温馨治愈",
        "冷色调为主，蓝紫银，静谧高级",
        "莫兰迪低饱和，灰调优雅",
        "高饱和鲜艳，活力张扬",
        "黑金配色，奢华质感",
        "马卡龙糖果色，甜美少女",
    ],
    "texture_detail": [
        "细腻肌理，可见微观纹理",
        "光滑丝绒质感，柔和过渡",
        "粗粝质感，颗粒与磨砂",
        "透明玻璃质感，折射光泽",
        "金属磨砂质感，冷冽高级",
        "有机自然纹理，木纹/石纹/水纹",
    ],
    "atmosphere": [
        "氛围感粒子，空气中的微尘/光斑",
        "薄雾弥漫，梦幻朦胧",
        "雨后清新，水珠反光",
        "夜景城市灯光，光斑散景",
        "阳光穿过树叶的斑驳光影",
        "飘落的花瓣/落叶/雪花",
    ],
}

_BEAUTIFY_QUALITY_TAGS = {
    "photo": "专业摄影级画质，超高分辨率，锐度极高，ISO 100，浅景深散焦光斑",
    "art": "大师级艺术品质，笔触/纹理细腻，色彩层次丰富，构图精美",
    "3d": "影视级3D渲染，PBR材质，全局光照，抗锯齿，高多边形",
    "design": "商业级设计品质，印刷级锐度，色彩管理精确，排版考究",
}

import re as _re
import hashlib as _hashlib


def beautify_prompt(raw_prompt: str, quality: str = "high",
                    seed: int | None = None) -> dict:
    """V10.5 智能Prompt美化器 — 将简单用户输入升级为专业级提示词

    核心理念: 用户说"画一只猫", 我们生成一段包含构图/光影/色调/纹理/氛围
    的丰富描述, 让用户体验到"啊哈, 原来AI可以画得这么好"的惊喜时刻。

    Args:
        raw_prompt: 用户原始输入
        quality: "high" or "standard"
        seed: 可选随机种子(用于稳定测试)

    Returns:
        {
            "original": str,       # 原始输入
            "beautified": str,     # 美化后的prompt
            "negative": str,       # 负面提示词
            "enhancements": list,  # 添加的增强维度
        }
    """
    import random
    if seed is not None:
        rng = random.Random(seed)
    else:
        h = int(_hashlib.md5(raw_prompt.encode()).hexdigest()[:8], 16)
        rng = random.Random(h)

    prompt = raw_prompt.strip()
    if not prompt:
        return {"original": "", "beautified": "", "negative": "", "enhancements": []}

    has_chinese = any('\u4e00' <= c <= '\u9fff' for c in prompt)
    is_already_detailed = len(prompt) > 150 or any(
        kw in prompt for kw in ["构图", "光照", "色调", "景深", "composition",
                                 "lighting", "bokeh", "depth of field"]
    )

    if is_already_detailed:
        suffix = QUALITY_SUFFIX.get(quality, QUALITY_SUFFIX["standard"])
        lang = "zh" if has_chinese else "en"
        if "8K" not in prompt and "高清" not in prompt and "UHD" not in prompt:
            prompt += suffix[lang]
        return {
            "original": raw_prompt,
            "beautified": prompt,
            "negative": QUALITY_NEGATIVE.get(quality, BASE_NEGATIVE),
            "enhancements": ["quality_suffix"],
        }

    enhancements = []
    parts = [prompt]

    category = _detect_category(prompt)

    comp = rng.choice(_BEAUTIFY_DIMENSIONS["composition"])
    parts.append(comp)
    enhancements.append(f"构图: {comp}")

    light = rng.choice(_BEAUTIFY_DIMENSIONS["lighting"])
    parts.append(light)
    enhancements.append(f"光照: {light}")

    color = rng.choice(_BEAUTIFY_DIMENSIONS["color_mood"])
    parts.append(color)
    enhancements.append(f"色调: {color}")

    if quality == "high":
        texture = rng.choice(_BEAUTIFY_DIMENSIONS["texture_detail"])
        parts.append(texture)
        enhancements.append(f"质感: {texture}")

        atmo = rng.choice(_BEAUTIFY_DIMENSIONS["atmosphere"])
        parts.append(atmo)
        enhancements.append(f"氛围: {atmo}")

    quality_tag = _BEAUTIFY_QUALITY_TAGS.get(category, _BEAUTIFY_QUALITY_TAGS["photo"])
    parts.append(quality_tag)
    enhancements.append(f"品质: {category}")

    sep = "，" if has_chinese else ", "
    beautified = sep.join(parts)

    return {
        "original": raw_prompt,
        "beautified": beautified,
        "negative": QUALITY_NEGATIVE.get(quality, BASE_NEGATIVE),
        "enhancements": enhancements,
    }


def _detect_category(prompt: str) -> str:
    """检测prompt的类别以选择合适的品质标签"""
    p = prompt.lower()
    if any(kw in p for kw in ["3d", "微缩", "水晶", "毛绒", "充气", "乐高", "黏土",
                               "render", "模型", "手办"]):
        return "3d"
    if any(kw in p for kw in ["设计", "logo", "ppt", "海报", "名片", "包装", "ui",
                               "app", "banner", "排版", "封面", "邀请"]):
        return "design"
    if any(kw in p for kw in ["画", "绘", "水墨", "油画", "水彩", "漫画", "插画",
                               "吉卜力", "像素", "浮世绘", "艺术"]):
        return "art"
    return "photo"
