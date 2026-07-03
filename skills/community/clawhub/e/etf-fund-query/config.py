"""ETF信息查询 — 统一配置（对外版本）.

鉴权方式（优先级从高到低）：
  1. 环境变量 ETF_API_KEY（推荐）
  2. 修改本文件的 _FALLBACK_KEY（fallback）

安装时两处同时写入，确保任一方式均可独立生效。
"""

import os

BASE_URL = "https://www.etf.com.cn/api/etf-api-service"
_FALLBACK_KEY = ""  # 无环境变量时使用，可直接在此填入 key
API_KEY = os.environ.get("ETF_API_KEY") or _FALLBACK_KEY

CALLER_TYPE = "external"  

# 请求头固定配置
# 认证格式：Authorization: Bearer <API_KEY>
# 请求来源标识：X-Caller-Type: external

if not API_KEY:
    raise RuntimeError(
        "未找到 API Key。请访问以下链接获取：\n"
        "https://cdn.efunds.com.cn/eda/h5/itcenter/pd/ai-skills-doc/readme.pdf\n"
        "请输入获取到的 key："
    )
