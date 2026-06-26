#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run.py — 设计日报一键运行入口
用法：
  python run.py            # 正常运行，保存到 logs/
  python run.py --preview  # 预览模式，只打印不保存
"""

import json
import logging
import sys
from datetime import datetime
from pathlib import Path

import yaml

# ── 路径 ─────────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).parent
LOG_DIR  = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

# ── 自动加载 .env（setup.py 写入的 key）─────────────────────────────────────
def load_dotenv():
    env_path = BASE_DIR / ".env"
    if env_path.exists():
        import os
        for line in env_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())

load_dotenv()

# ── 解析参数 ──────────────────────────────────────────────────────────────────
PREVIEW_MODE = "--preview" in sys.argv

# ── 日志 ─────────────────────────────────────────────────────────────────────
today = datetime.now().strftime("%Y-%m-%d")

handlers = [logging.StreamHandler(sys.stdout)]
if not PREVIEW_MODE:
    handlers.append(logging.FileHandler(LOG_DIR / f"{today}.log", encoding="utf-8"))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=handlers,
)

if PREVIEW_MODE:
    logging.info("👀 预览模式：结果只打印，不保存文件")

# ── 合法岗位列表 ──────────────────────────────────────────────────────────────
ALL_VALID_ROLES = {
    "UI设计师", "UX设计师", "视觉设计师", "交互设计师", "服务设计师",
    "设计系统工程师", "动效设计师", "内容设计师", "可访问性设计师",
    "用户研究员", "增长设计师", "产品设计师",
    "AI产品设计师", "设计工程师", "零界面设计师", "空间计算设计师",
    "产品经理",
}


def load_config() -> dict:
    config_path = BASE_DIR / "config.yaml"
    if not config_path.exists():
        logging.error("❌ 找不到 config.yaml，请先运行 python setup.py")
        sys.exit(1)

    with open(config_path, encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    cfg.setdefault("roles",               ["UI设计师", "UX设计师"])
    cfg.setdefault("items_per_day",       3)
    cfg.setdefault("brief_title",         "设计日报")
    cfg.setdefault("time_range",          "1w")
    cfg.setdefault("favorite_designers",  [])

    # 校验岗位
    invalid = [r for r in cfg["roles"] if r not in ALL_VALID_ROLES]
    if invalid:
        logging.warning(f"⚠️  以下岗位无效，已忽略：{invalid}")
        cfg["roles"] = [r for r in cfg["roles"] if r in ALL_VALID_ROLES]

    if not cfg["roles"]:
        logging.error("❌ roles 列表为空，请在 config.yaml 中至少填写一个岗位")
        sys.exit(1)

    cfg["items_per_day"] = max(1, min(cfg["items_per_day"], 10))
    return cfg


def focus_hint(n: int) -> str:
    if n <= 2:
        return "聚焦模式"
    elif n <= 5:
        return "均衡模式"
    return "广覆盖模式"


def main():
    cfg           = load_config()
    roles              = cfg["roles"]
    items_per_day      = cfg["items_per_day"]
    brief_title        = cfg["brief_title"]
    time_range         = cfg["time_range"]
    favorite_designers = cfg["favorite_designers"]
    date_str           = datetime.now().strftime("%Y/%m/%d")

    # 时间范围可读标签
    time_label = {
        "24h": "过去 24 小时", "2d": "过去 2 天", "3d": "过去 3 天",
        "1w" : "过去 1 周",   "2w": "过去 2 周", "1m": "过去 1 个月",
    }.get(time_range, time_range)

    logging.info(f"🚀 开始生成「{brief_title}」{date_str}")
    logging.info(f"   岗位（{len(roles)}个，{focus_hint(len(roles))}）：{'、'.join(roles)}")
    logging.info(f"   每日条数：{items_per_day} | 时间范围：{time_label}")
    if favorite_designers:
        sep = "、"
        fav_names = [d.get("name") or d.get("url", "未命名") for d in favorite_designers]
        logging.info(f"   ⭐ 关注设计师：{sep.join(fav_names)}")

    # 1. 抓取
    from fetch import fetch_all
    raw_items = fetch_all(roles, items_per_day, time_range, favorite_designers)
    if not raw_items:
        logging.error("❌ 未抓取到任何内容，请检查 SERPER_API_KEY 或网络连接")
        sys.exit(1)

    # 2. 生成
    from brief import generate_brief
    brief_text, brief_data = generate_brief(
        raw_items          = raw_items,
        roles              = roles,
        count              = items_per_day,
        title              = brief_title,
        date_str           = date_str,
        favorite_designers = favorite_designers,
    )

    # 3. 输出
    print("\n" + "=" * 50)
    print(brief_text)
    print("=" * 50)

    if PREVIEW_MODE:
        logging.info("👀 预览完成，未保存任何文件")
        return

    # 4. 保存
    out_txt  = LOG_DIR / f"{today}_brief.txt"
    out_json = LOG_DIR / f"{today}_brief.json"

    out_txt.write_text(brief_text, encoding="utf-8")
    out_json.write_text(
        json.dumps(
            {
                "date"      : today,
                "config"    : cfg,
                "raw_count" : len(raw_items),
                "brief"     : brief_data,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    logging.info(f"💾 TXT  => {out_txt}")
    logging.info(f"💾 JSON => {out_json}")


if __name__ == "__main__":
    main()
