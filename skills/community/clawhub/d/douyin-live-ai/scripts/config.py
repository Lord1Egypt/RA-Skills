"""
抖音直播弹幕AI回复助手 - 配置文件
请在此处填写你的直播间信息和API Key
"""
import os

# ==================== 直播间配置 ====================
# 抖音直播间ID（URL最后的数字，如 https://live.douyin.com/349873582969）
ROOM_ID = "your_room_id_here"

# 直播类型: "ecommerce"(电商), "education"(教育), "entertainment"(娱乐)
LIVE_TYPE = "entertainment"

# ==================== 主播简介配置 ====================
# 主播名称
HOST_NAME = "你的主播名称"

# 主播简介 - 用于让AI了解主播背景和风格，填写越详细回复越准确
HOST_INTRO = """
请在这里填写主播简介，例如：
主播是英雄联盟游戏主播，专注于LOL游戏直播。
擅长各种英雄操作，经常分享游戏技巧、出装思路、对线细节。
直播风格幽默风趣，与观众互动频繁，乐于解答游戏相关问题。
"""

# 主播人设风格
HOST_PERSONA = "幽默风趣，技术过硬但平易近人，喜欢和观众互动"

# 回复风格: "professional"(专业), "friendly"(亲切), "humorous"(幽默)
REPLY_STYLE = "humorous"

# ==================== DeepSeek API 配置 ====================
# DeepSeek API Key（在 https://platform.deepseek.com/ 获取）
# 也可通过环境变量 DEEPSEEK_API_KEY 设置，避免明文写入代码
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY", "your_deepseek_api_key_here")

# DeepSeek API 地址
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"

# 使用的模型
DEEPSEEK_MODEL = "deepseek-chat"

# 温度参数 (0-2, 越高越 creative，建议 0.7)
TEMPERATURE = 0.7

# 最大token数
MAX_TOKENS = 500

# ==================== 缓存配置 ====================
# 获取脚本所在目录，缓存文件保存在同目录下
_BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 弹幕缓存文件路径
CACHE_FILE = os.path.join(_BASE_DIR, "danmu_cache.jsonl")

# 回复记录文件路径
REPLY_FILE = os.path.join(_BASE_DIR, "ai_replies.jsonl")

# ==================== 过滤配置 ====================
# 忽略的用户名列表 (如机器人、管理员)
IGNORED_USERS = ["管理员", "系统消息"]

# 忽略的关键词 (如纯表情、无意义内容)
IGNORED_KEYWORDS = ["666", "哈哈哈", "...", "???"]

# 最小消息长度 (小于此长度将忽略)
MIN_MESSAGE_LENGTH = 2
