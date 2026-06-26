#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
1688 素材优化 — 业务常量配置
"""

import os

# ── API 网关地址 ─────────────────────────────────────────────────────────────
# 优先从环境变量读取，读不到则使用默认值
BASE_URL = os.environ.get("BASE_URL", "https://skills-gateway.1688.com")

# ── 固定参数 ─────────────────────────────────────────────────────────────
DEFAULT_USER_ID = 0

# ── API 路径 ─────────────────────────────────────────────────────────────

# 图片优化（AI 生图）
API_IMAGE_OPTIMIZE = "/api/distribution_material_edit_image_by_jimeng/1.0.0"

# 图片优化结果轮询
API_IMAGE_STATUS = "/api/distribution_material_get_image_algo_status/1.0.0"

# 获取商品主图信息
API_IMAGE_INFO = "/api/distribution_material_get_image_info/1.0.0"

# 标题优化
API_TITLE_OPTIMIZE = "/api/distribution_material_generate_title/1.0.0"

# 卖点生成
API_SELLING_POINT = "/api/distribution_material_generate_selling_point/1.0.0"

# 抠图（生成白底图）
API_CUTOUT_IMAGE = "/api/fx_cutout_image/1.0.0"

# ── 图片优化轮询配置 ─────────────────────────────────────────────────────
POLL_INTERVAL_SECONDS = 10      # 每次轮询间隔（秒）
POLL_MAX_SECONDS = 180          # 最长轮询时间（秒）= 3 分钟

# ── 图片优化并发限制 ─────────────────────────────────────────────────────
MAX_CONCURRENT_IMAGES = 5       # 最多同时优化 5 张图片

# ── 输出比例枚举 ─────────────────────────────────────────────────────────
VALID_SIZES = ["1:1", "2:3", "9:16"]
