"""
paths.py — bilibili-search skill 的路径统一管理

设计目标:
  1. skill 自包含 — 默认 $SKILL/data/,git clone 即用
  2. env 覆盖 — BI_DATA_DIR / BI_COOKIE_FILE 给 docker / CI 用
  3. 老路径兼容 — /tmp/bilibili/ 还在的话自动用 (向下兼容)
  4. 自动创建 — 子目录不存在时自动建,所有子脚本不用 mkdir

路径解析优先级 (从高到低):
  1. 环境变量 BI_DATA_DIR           (覆盖整个 data 目录)
  2. 环境变量 BI_COOKIE_FILE        (单独覆盖 cookie 路径)
  3. 老的 /tmp/bilibili/            (如果存在,优先用;向后兼容)
  4. 默认 $SKILL/data/

用法:
  from paths import DATA_DIR, COOKIE_FILE, HARVESTS_DIR
  # 然后直接用,不用关心在哪

注意: B 站抓取**不强制需要 cookie** — 大部分公开 API 在未登录态都能用。
       cookie 文件主要是给"已登录用户想拿到完整数据"的可选通道,
       以及给 agent-browser 注入保持登录态(避免偶尔 captcha)用。
"""

import os
from pathlib import Path

# 老的 /tmp/bilibili/ 路径 (向后兼容)
LEGACY_DIR = Path("/tmp/bilibili")
LEGACY_COOKIE = LEGACY_DIR / "cookies.txt"
LEGACY_COOKIE_RAW = LEGACY_DIR / "cookies-raw.txt"

# env 覆盖
_env_data_dir = os.environ.get("BI_DATA_DIR")
_env_cookie = os.environ.get("BI_COOKIE_FILE")

# 决定 DATA_DIR
if _env_data_dir:
    DATA_DIR = Path(_env_data_dir)
elif LEGACY_DIR.exists():
    # 老路径存在 → 用老路径 (向后兼容)
    DATA_DIR = LEGACY_DIR
else:
    # 默认: 当前文件所在目录的 data/ 子目录
    DATA_DIR = Path(__file__).parent / "data"

# 子目录
COOKIE_RAW = DATA_DIR / "cookies-raw.txt"
COOKIE_FILE = DATA_DIR / "cookies.txt"
STATE_DIR = DATA_DIR / "state"
STATE_FILE = STATE_DIR / "bili.state"
EXPORTS_DIR = DATA_DIR / "exports"
CACHE_DIR = DATA_DIR / "cache"
USERS_DIR = DATA_DIR / "users"
VIDEOS_DIR = DATA_DIR / "videos"
HARVESTS_DIR = DATA_DIR / "harvests"

# 自动创建子目录
for _d in (DATA_DIR, STATE_DIR, EXPORTS_DIR, CACHE_DIR, USERS_DIR, VIDEOS_DIR, HARVESTS_DIR):
    _d.mkdir(parents=True, exist_ok=True)

# 覆盖 cookie 路径 (如果 env 设了)
if _env_cookie:
    COOKIE_FILE = Path(_env_cookie)


def report():
    """打印当前路径配置 (供 debug / paths 命令用)"""
    print("=== bilibili-search 路径配置 ===")
    print(f"  DATA_DIR     = {DATA_DIR}")
    print(f"  COOKIE_FILE  = {COOKIE_FILE}  (exists: {COOKIE_FILE.exists()})")
    print(f"  COOKIE_RAW   = {COOKIE_RAW}  (exists: {COOKIE_RAW.exists()})")
    print(f"  STATE_FILE   = {STATE_FILE}")
    print(f"  EXPORTS_DIR  = {EXPORTS_DIR}")
    print(f"  USERS_DIR    = {USERS_DIR}")
    print(f"  VIDEOS_DIR   = {VIDEOS_DIR}")
    print(f"  HARVESTS_DIR = {HARVESTS_DIR}")
    print(f"  老的 /tmp/bilibili/ = {LEGACY_DIR}  (exists: {LEGACY_DIR.exists()})")
    print(f"  ENV 覆盖: BI_DATA_DIR={_env_data_dir!r}, BI_COOKIE_FILE={_env_cookie!r}")


if __name__ == "__main__":
    report()