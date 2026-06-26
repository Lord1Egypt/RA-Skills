#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
novel-auto-publish - 配置文件
"""

# 创作配置
DEFAULT_CHAPTER_COUNT = 5          # 默认生成章节数
PASSING_SCORE = 85                 # 评审通过分数
MAX_REVISIONS = 2                  # 最大修订次数
MIN_WORDS_PER_CHAPTER = 2000       # 每章最小字数
MAX_WORDS_PER_CHAPTER = 5000       # 每章最大字数

# 发布配置
PUBLISH_INTERVAL_SECONDS = 5       # 发布间隔（秒），避免频繁请求
AUTO_PUBLISH_AFTER_GENERATION = True  # 生成完成后自动发布

# 路径配置
# 依赖技能路径
OPEN_NOVEL_WRITING_PATH = "../../open-novel-writing"
FANQIE_PUBLISHER_PATH = "../../fanqie-publisher/scripts"

# 小说项目默认目录
DEFAULT_NOVEL_ROOT = "./novels"

# 番茄发布配置
FANQIE_COOKIES_PATH = "../../fanqie-publisher/scripts/fanqie_cookies.json"
