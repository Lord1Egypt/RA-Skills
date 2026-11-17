#!/usr/bin/env python3
"""
公共常量定义
"""

# API 配置
API_URL = "https://scan-business.quark.cn/vision"

# 文件配置
ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".tiff", ".tif"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

# 请求配置
REQUEST_TIMEOUT = 120  # 秒

# HTTP 状态码
HTTP_OK = 200

# 错误消息最大截取长度
ERROR_MSG_MAX_LENGTH = 200

# API 成功响应码
SUCCESS_CODE = "00000"

# 错误码消息常量
ERR_MSG_A0211_QUOTA_INSUFFICIENT = (
    "请前往https://scan.quark.cn/business，登录开发者后台，"
    "选择需要的套餐进行充值（请注意购买Skill专用套餐）"
)
