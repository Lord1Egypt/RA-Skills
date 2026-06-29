#!/usr/bin/env python3
"""
paths.py - 集中管理 douyin-search skill 的所有路径
=================================================

路径解析优先级(从高到低):
1. 环境变量 DOUYIN_DATA_DIR
2. 老的 /tmp/douyin/(向后兼容,如果新路径不存在但老的在)
3. 默认 <skill 目录>/data/

这样 skill 可以:
- git clone 到任何位置都能用(自包含)
- 跨设备部署(每台机器只需导一次 cookies)
- 老的 /tmp/douyin/ 数据自动迁移(无需手工)
"""
import os
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent
LEGACY_DIR = Path("/tmp/douyin")


def _resolve_data_dir() -> Path:
    """解析 data 目录"""
    env = os.environ.get("DOUYIN_DATA_DIR")
    if env:
        return Path(env).expanduser().resolve()
    # 老的 /tmp/douyin/ 兼容:存在就用老的
    if (LEGACY_DIR / "cookies.txt").exists():
        return LEGACY_DIR
    # 默认 skill 目录
    return SKILL_DIR / "data"


def _ensure_dir(p: Path) -> Path:
    """确保目录存在"""
    p.mkdir(parents=True, exist_ok=True)
    return p


# ===== 核心路径(其他模块用这些)=====
DATA_DIR   = _resolve_data_dir()
COOKIE_RAW = DATA_DIR / "cookies-raw.txt"
COOKIE_FILE = DATA_DIR / "cookies.txt"
STATE_DIR  = _ensure_dir(DATA_DIR / "state")
STATE_FILE = STATE_DIR / "douyin.state"
EXPORTS_DIR = _ensure_dir(DATA_DIR / "exports")

# 临时文件目录(harvest 过程的中间文件,放系统 /tmp)
TMP_DIR = Path("/tmp/douyin")
_ensure_dir(TMP_DIR)


def report() -> str:
    """返回当前路径配置(供 keepalive.py / comments-harvest.py 启动时打印)"""
    lines = [
        "📁 douyin-search skill 路径配置:",
        f"  skill 目录:    {SKILL_DIR}",
        f"  data 目录:     {DATA_DIR}",
        f"  cookies:       {COOKIE_FILE}",
        f"  cookies-raw:   {COOKIE_RAW}",
        f"  state:         {STATE_FILE}",
        f"  默认导出:      {EXPORTS_DIR}",
    ]
    if DATA_DIR == LEGACY_DIR:
        lines.append("  ⚠️  使用老路径 /tmp/douyin/ (向后兼容)")
        lines.append("     建议: 跑 setup 切到新路径;或设 DOUYIN_DATA_DIR 环境变量")
    return "\n".join(lines)
