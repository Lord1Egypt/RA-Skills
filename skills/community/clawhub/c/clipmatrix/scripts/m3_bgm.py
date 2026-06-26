"""
BGM匹配模块 — 本地固定曲库，用得最少的优先
"""
import os
import json
import random
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

BGM_DIR = Path(__file__).parent / "sounds"
BGM_USAGE_FILE = Path(__file__).parent / "config" / "bgm_usage.json"


def get_bgm_list() -> list:
    """获取所有可用BGM文件"""
    bgm_dir = BGM_DIR
    if not bgm_dir.exists():
        bgm_dir.mkdir(parents=True, exist_ok=True)
        logger.warning(f"BGM directory created at {bgm_dir}, add audio files")
        return []

    bgm_files = []
    for f in bgm_dir.iterdir():
        if f.suffix.lower() in (".mp3", ".wav", ".m4a", ".aac", ".ogg", ".flac"):
            if f.stat().st_size > 1000:  # 有效音频
                bgm_files.append(str(f))
    return sorted(bgm_files)


def load_usage() -> dict:
    """加载BGM使用记录"""
    if BGM_USAGE_FILE.exists():
        try:
            with open(BGM_USAGE_FILE) as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    return {}


def save_usage(usage: dict):
    """保存BGM使用记录"""
    BGM_USAGE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(BGM_USAGE_FILE, "w") as f:
        json.dump(usage, f, indent=2)


def select_bgm() -> str:
    """选择用得最少的BGM"""
    bgm_list = get_bgm_list()
    if not bgm_list:
        logger.warning("No BGM files available")
        return ""

    usage = load_usage()
    # 按使用次数排序，最少优先
    scored = []
    for bgm in bgm_list:
        name = os.path.basename(bgm)
        count = usage.get(name, 0)
        scored.append((count, bgm))

    scored.sort(key=lambda x: x[0])

    # 从使用次数最低的前5首里，排除最近2次用过的
    candidates = scored[:min(5, len(scored))]
    recent_names = [k for k, _ in sorted(usage.items(), key=lambda x: -x[1])[:2]]
    fresh = [(c, b) for c, b in candidates if os.path.basename(b) not in recent_names]
    if not fresh:
        fresh = candidates  # 兜底
    chosen = random.choice(fresh)[1]

    # 记录使用
    chosen_name = os.path.basename(chosen)
    usage[chosen_name] = usage.get(chosen_name, 0) + 1
    save_usage(usage)

    logger.info(f"Selected BGM: {chosen_name} (used {usage[chosen_name]} times)")
    return chosen


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    bgm = select_bgm()
    print(f"Selected: {bgm}")
