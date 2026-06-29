"""
抖音评论管理助手 - 配置管理模块
"""

import os
import json
from pathlib import Path

# 项目根目录（skill 根目录）
PROJECT_DIR = Path(__file__).resolve().parent.parent

# 输出目录
OUTPUT_DIR = PROJECT_DIR / "output"

# Playwright 配置
PLAYWRIGHT_DIR = PROJECT_DIR / ".playwright"
PROFILE_DIR = PLAYWRIGHT_DIR / "douyin-profile"

# 抖音创作者中心 URL
DOUYIN_LOGIN_URL = "https://creator.douyin.com/"
DOUYIN_CREATOR_URL = "https://creator.douyin.com/creator-micro/home"
DOUYIN_CONTENT_URL = "https://creator.douyin.com/creator-micro/content/manage"
DOUYIN_COMMENT_URL = "https://creator.douyin.com/creator-micro/content/comment"

# 默认配置
DEFAULT_CONFIG = {
    "headless": False,          # 是否无头模式（登录阶段必须 False）
    "viewport": {"width": 1280, "height": 900},
    "locale": "zh-CN",
    "timezone_id": "Asia/Shanghai",
    "slow_mo": 50,              # 操作间隔（毫秒）
    "max_comments_per_video": 500,
    "reply_delay_min": 3,       # 回复间隔最小值（秒）
    "reply_delay_max": 8,       # 回复间隔最大值（秒）
    "max_replies_per_run": 100, # 单次最大回复数
}

# 默认回复模板
DEFAULT_REPLY_TEMPLATES = {
    "templates": [
        {
            "keywords": ["谢谢", "感谢", "支持", "加油", "太棒了", "厉害"],
            "reply": "感谢你的支持和鼓励！❤️"
        },
        {
            "keywords": ["问题", "怎么", "如何", "请问", "能不能", "可以吗"],
            "reply": "可以私信我详细沟通，看到都会回复的～"
        },
        {
            "keywords": ["多少钱", "价格", "怎么卖", "哪里买", "购买"],
            "reply": "点击主页链接了解更多详情哦～"
        },
        {
            "keywords": ["好看", "漂亮", "美", "帅", "喜欢", "爱了"],
            "reply": "谢谢夸奖！😊"
        },
        {
            "keywords": ["？", "?"],
            "reply": "可以在评论区详细描述一下你的问题，我会认真看的！"
        },
    ],
    "default_reply": "感谢评论！💕",
}

# 违规内容检测关键词
BLOCKED_KEYWORDS = [
    "加微信", "加V", "vx", "VX", "QQ", "qq",
    "电话", "手机号", "链接", "http", "www",
    "私聊", "免费领取", "点击", "下载",
]


def ensure_dirs():
    """确保所需目录存在"""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    PLAYWRIGHT_DIR.mkdir(parents=True, exist_ok=True)
    PROFILE_DIR.mkdir(parents=True, exist_ok=True)


def load_config():
    """加载配置文件"""
    config = dict(DEFAULT_CONFIG)
    config_file = PROJECT_DIR / "config.json"
    if config_file.exists():
        with open(config_file, "r", encoding="utf-8") as f:
            user_config = json.load(f)
            config.update(user_config)
    return config


def load_reply_templates(path=None):
    """加载回复模板"""
    if path:
        template_file = Path(path)
    else:
        template_file = PROJECT_DIR / "reply_templates.json"
    
    if template_file.exists():
        with open(template_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return DEFAULT_REPLY_TEMPLATES


def contains_blocked_content(text):
    """检查文本是否包含违规内容"""
    text_lower = text.lower()
    for kw in BLOCKED_KEYWORDS:
        if kw.lower() in text_lower:
            return True, kw
    return False, None


def match_template(content, templates):
    """根据评论内容匹配回复模板"""
    if not content:
        return templates.get("default_reply", "感谢评论！💕")
    
    template_list = templates.get("templates", [])
    for tpl in template_list:
        for kw in tpl.get("keywords", []):
            if kw in content:
                return tpl["reply"]
    
    return templates.get("default_reply", "感谢评论！💕")
