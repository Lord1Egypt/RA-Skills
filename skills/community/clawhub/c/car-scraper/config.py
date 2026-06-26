"""
万能反爬 Skill - 通用配置
支持大搜车、懂车帝、汽车之家的车辆信息采集
"""

import os
from dataclasses import dataclass, field
from typing import Optional

# ─── 基础配置 ─────────────────────────────────────────

# 请求间隔 (秒)，避免触发反爬
REQUEST_DELAY_MIN = 2.0
REQUEST_DELAY_MAX = 5.0

# 最大重试次数
MAX_RETRIES = 3

# 请求超时 (秒)
REQUEST_TIMEOUT = 30

# 并发请求数 (保持低并发以减少封禁风险)
MAX_CONCURRENT = 2

# 数据输出目录
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ─── 代理配置 ─────────────────────────────────────────

# 代理列表（按需填写）
PROXY_LIST: list[str] = [
    # "http://user:pass@proxy1:port",
    # "http://user:pass@proxy2:port",
]

# 启用代理轮换
PROXY_ROTATION_ENABLED = False


# ─── 目标站点配置 ──────────────────────────────────────

@dataclass
class SiteConfig:
    """站点采集配置"""
    name: str
    base_url: str
    list_url: str
    detail_url_pattern: str
    encoding: str = "utf-8"
    pages_to_scrape: int = 10
    extra_headers: dict = field(default_factory=dict)


# 大搜车（弹个车/大搜车好车）
DASOUCHE_CONFIG = SiteConfig(
    name="大搜车",
    base_url="https://www.souche.com",
    list_url="https://www.souche.com/buycar/list",
    detail_url_pattern="https://www.souche.com/buycar/detail/{car_id}",
    pages_to_scrape=10,
    extra_headers={
        "Accept": "application/json, text/plain, */*",
    }
)

# 懂车帝
DONGCHEDI_CONFIG = SiteConfig(
    name="懂车帝",
    base_url="https://www.dongchedi.com",
    list_url="https://www.dongchedi.com/usedcar/x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x",
    detail_url_pattern="https://www.dongchedi.com/usedcar/{car_id}",
    pages_to_scrape=10,
    extra_headers={
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    }
)

# 汽车之家
AUTOHOME_CONFIG = SiteConfig(
    name="汽车之家",
    base_url="https://www.autohome.com.cn",
    list_url="https://www.che168.com/list/",
    detail_url_pattern="https://www.che168.com/dealer/{car_id}.html",
    encoding="gb2312",
    pages_to_scrape=10,
    extra_headers={
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    }
)


# ─── OpenClaw 输出配置 ─────────────────────────────────

OPENCLAW_OUTPUT_FORMAT = "json"  # json / csv / both
OPENCLAW_OUTPUT_DIR = os.path.join(OUTPUT_DIR, "openclaw")
os.makedirs(OPENCLAW_OUTPUT_DIR, exist_ok=True)
