"""
抖音发布技能配置文件
"""

# 技能基本信息
SKILL_NAME = "douyin-upload"
SKILL_VERSION = "1.0.0"
SKILL_DESCRIPTION = "自动发布抖音文章内容"

# 内容生成配置
CONTENT_GENERATION = {
    "model": "gpt-4",  # 可选：gpt-4, gpt-3.5-turbo, claude-3-opus, claude-3-sonnet
    "max_tokens": 1000,
    "temperature": 0.7,
    "language": "zh-CN"
}

# 图片生成配置
IMAGE_GENERATION = {
    "model": "dall-e-3",  # 可选：dall-e-2, dall-e-3, 或其他图像生成API
    "size": "1024x1024",
    "quality": "standard"
}

# 发布配置
PUBLISH_CONFIG = {
    "sau_command": "sau",
    "platform": "douyin",
    "account_name": "xiaoA",
    "default_publish_type": 0,  # 0: 立即发布, 1: 定时发布
    "default_tags": ["#科技", "#分享", "#内容创作"]
}

# 工作目录配置
WORKSPACE_DIR = "/Users/yiwanjun/.openclaw/workspace"
ARTICLES_DIR = f"{WORKSPACE_DIR}/articles"
IMAGES_DIR = f"{WORKSPACE_DIR}/images"
TEMP_DIR = f"{WORKSPACE_DIR}/temp"

# 预设主题分类
THEME_CATEGORIES = {
    "科技": ["人工智能", "科技", "数码", "创新", "技术"],
    "生活": ["生活", "日常", "习惯", "健康", "有趣", "生活技巧"],
    "学习": ["学习", "教育", "经验", "技能", "知识", "成长"],
    "旅游": ["旅游", "旅行", "风景", "景点", "探索"],
    "美食": ["美食", "烹饪", "食谱", "推荐", "体验"],
    "娱乐": ["娱乐", "搞笑", "生活", "分享", "有趣内容"],
    "职场": ["职场", "工作", "经验", "职场技巧", "人脉", "成长"],
    "情感": ["情感", "生活", "思考", "感悟", "人生", "情感故事"]
}

# 预设封面风格
COVER_STYLES = [
    "科技感",
    "简洁现代", 
    "温馨生活",
    "自然风景",
    "创意抽象",
    "商务专业",
    "活泼有趣",
    "艺术感"
]