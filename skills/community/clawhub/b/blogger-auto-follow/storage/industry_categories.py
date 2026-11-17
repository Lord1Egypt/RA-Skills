# -*- coding: utf-8 -*-
"""
全行业/多领域分类管理与智能归类引擎
涵盖：科技数码、商业财经、设计创意、影视摄影、职场效率、知识科普、运营电商、泛生活等
"""

from typing import Dict, List, Tuple


# 标准一级行业大类及图标与关键词映射
INDUSTRY_DEFINITIONS: Dict[str, Dict] = {
    "科技 · 数码 · 编程": {
        "icon": "💻",
        "default_subcategories": ["AI技术与工具", "AIGC创作", "编程开发/实操", "数码测评", "前沿科技", "开源软件/硬件"],
        "keywords": [
            "ai", "aigc", "代码", "编程", "开发", "技术", "软件", "数码", "硬件", "算法", "大模型",
            "gpt", "python", "javascript", "git", "测评", "数码控", "自动化", "程序员", "极客",
            "科技", "linux", "prompt", "提示词", "stable diffusion", "midjourney"
        ]
    },
    "商业 · 财经 · 创业": {
        "icon": "📈",
        "default_subcategories": ["商业认知", "投资理财", "一人公司/独立开发", "出海创业", "宏观经济", "商业模式拆解"],
        "keywords": [
            "商业", "财经", "理财", "股票", "基金", "投资", "创业", "搞钱", "一人公司", "出海",
            "经济", "商业模式", "认知", "财报", "资产", "财富", "副业", "自由职业", "商业观察", "增长"
        ]
    },
    "设计 · 视觉 · 创意": {
        "icon": "🎨",
        "default_subcategories": ["UI/UX设计", "平面设计/排版", "3D建模/渲染", "动效设计", "插画/概念艺术", "品牌视觉"],
        "keywords": [
            "设计", "ui", "ux", "平面", "美学", "排版", "配色", "3d", "blender", "c4d", "插画",
            "动效", "视觉", "品牌", "海报", "艺术", "创意", "figma", "样机", "字体"
        ]
    },
    "影视 · 摄影 · 剪辑": {
        "icon": "🎬",
        "default_subcategories": ["摄影摄像", "后期剪辑/调色", "影视解说/拉片", "短剧/视效创作", "导演视听语言"],
        "keywords": [
            "摄影", "摄像", "剪辑", "调色", "影视", "电影", "短剧", "镜头", "相机", "达芬奇",
            "premiere", "final cut", "视听", "解说", "航拍", "布光", "故事片", "微电影"
        ]
    },
    "职场 · 效率 · 成长": {
        "icon": "🎯",
        "default_subcategories": ["办公提效/生产力", "个人成长/自律", "Notion/飞书/知识库", "时间管理", "职场晋升/沟通"],
        "keywords": [
            "职场", "提效", "生产力", "效率", "excel", "ppt", "notion", "飞书", "时间管理",
            "自律", "习惯", "成长", "沟通", "汇报", "方法论", "思维导图", "知识管理"
        ]
    },
    "知识 · 人文 · 科普": {
        "icon": "📚",
        "default_subcategories": ["硬核科普", "历史人文", "深度阅读/拆书", "心理学", "通识教育", "哲学社会学"],
        "keywords": [
            "科普", "历史", "人文", "读书", "拆书", "心理学", "哲学", "社会学", "文献", "通识",
            "硬核", "地理", "天文", "科学", "深度思考", "脑洞"
        ]
    },
    "运营 · 营销 · 电商": {
        "icon": "🛍️",
        "default_subcategories": ["短视频/内容运营", "私域流量", "品牌营销", "跨境电商/带货", "文案策略"],
        "keywords": [
            "运营", "营销", "带货", "电商", "私域", "流量", "文案", "爆款", "转化", "投流",
            "品牌", "跨境", "亚马逊", "选品", "社群", "裂变"
        ]
    },
    "泛生活 · 娱乐 · 兴趣": {
        "icon": "🍳",
        "default_subcategories": ["美食烹饪", "旅行探店", "游戏动漫", "生活Vlog", "音乐潮流", "健康健身"],
        "keywords": [
            "生活", "美食", "旅行", "探店", "游戏", "二次元", "动漫", "vlog", "音乐", "健身",
            "运动", "烹饪", "穿搭", "萌宠", "潮流"
        ]
    },
    "综合 · 其他": {
        "icon": "🌐",
        "default_subcategories": ["综合推荐", "未分类"],
        "keywords": []
    }
}


def infer_industry(name: str = "", raw_category: str = "", bio: str = "") -> str:
    """
    根据博主名称、原始分类、简介智能推断其所属的一级行业大类
    """
    text = f"{name} {raw_category} {bio}".lower()

    # 优先精确匹配行业名称
    for industry_name in INDUSTRY_DEFINITIONS.keys():
        clean_name = industry_name.replace(" · ", "").replace(" ", "").lower()
        if clean_name in raw_category.replace(" ", "").lower():
            return industry_name

    # 基于关键词打分匹配
    scores = {}
    for industry, config in INDUSTRY_DEFINITIONS.items():
        if industry == "综合 · 其他":
            continue
        score = 0
        for kw in config["keywords"]:
            if kw in text:
                # 原始分类中的关键词权重更高
                if kw in raw_category.lower():
                    score += 3
                else:
                    score += 1
        if score > 0:
            scores[industry] = score

    if scores:
        best_industry = max(scores.items(), key=lambda x: x[1])[0]
        return best_industry

    return "综合 · 其他"


def get_all_industries() -> List[Dict]:
    """获取所有行业大类列表及其图标"""
    result = []
    for industry_name, config in INDUSTRY_DEFINITIONS.items():
        result.append({
            "name": industry_name,
            "icon": config["icon"],
            "subcategories": config["default_subcategories"]
        })
    return result
