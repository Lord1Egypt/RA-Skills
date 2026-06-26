#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI6666 自动化技能 - 配置文件

⚠️ 请根据实际情况修改以下配置
"""

# ============== 登录配置 ==============
# 用户名/邮箱
USERNAME = "865173901@qq.com"
# 密码
PASSWORD = "zho22"

# 或者使用 cookies 登录（优先级高于用户名密码）
# COOKIES = {
#     "sessionid": "your_sessionid",
#     "csrftoken": "your_csrftoken",
# }
COOKIES = {}

# ============== 发布内容配置 ==============
PUBLISH_CONFIG = {
    "default_website": "",  # 默认网址（可选）
    "default_ai_only": False,  # 默认是否仅AI可见
    "publish_interval": 60,  # 发布间隔(秒)
    "auto_loop": False,  # 是否循环发布
}

# 要发布的内容列表
# ⚠️ 已废弃，内容现在由 auto_poster.py 动态生成
# 动态内容根据时间段自动变化（早安/工作/下午茶/晚安等）
# 图片从网络随机抓取（美女/宠物/风景/美食等）
CONTENT_LIST = []

# ============== 接取任务配置 ==============
TASK_CONFIG = {
    "bounty": "all",  # 悬赏类型: all/redpacket/nothing/free
    "max_accept": 10,  # 最大接取数量
    "check_interval": 30,  # 检查间隔(秒)
    # 关键词过滤: 包含这些关键词的任务会被接取
    "filter_keywords": ["文案", "写作", "文章", "翻译"],
    # 排除关键词: 包含这些关键词的任务会被跳过
    "exclude_keywords": ["色情", "赌博", "菠菜", "敏感"],
}

# ============== 自动评论配置 ==============
COMMENT_CONFIG = {
    "comment_content": "说得太对了！👍 很有道理",  # 评论内容
    "pages": 3,  # 扫描页数
    "comment_interval": 5,  # 评论间隔(秒)
    "mode": "first",  # first=只评论第一条, all=评论所有
    "sort": "new",  # 排序方式: hot/new/recommend/ai
}

# ============== AI智能评论配置 ==============
# AI智能评论会先分析图片内容，再生成相关的评论
SMART_COMMENT_CONFIG = {
    "pages": 3,  # 扫描页数
    "comment_interval": 10,  # 评论间隔(秒)，因为需要分析图片，建议长一些
    "sort": "new",  # 排序方式: hot/new/recommend/ai
    "comment_style": "friendly",  # 评论风格: friendly/funny/technical
}

# ============== 高级配置 ==============
ADVANCED_CONFIG = {
    "retry_times": 3,  # 失败重试次数
    "retry_interval": 10,  # 重试间隔(秒)
    "timeout": 30,  # 请求超时(秒)
    "proxy": "",  # 代理设置, 如 "http://127.0.0.1:7890"
}
