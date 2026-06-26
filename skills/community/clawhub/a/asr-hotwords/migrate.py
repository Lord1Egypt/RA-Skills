#!/usr/bin/env python3
"""
migrate.py — 从旧版 per-agent 安装迁移到全局 ~/.openclaw/skills/asr-hotwords/

扫描所有 agent workspace 下的旧安装，合并 output 数据，迁移标记文件。
"""

import json
import glob
import os
import shutil
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

NEW_SKILL_DIR = Path(__file__).parent.resolve()
OC_CONFIG = Path(os.path.expanduser("~/.openclaw/openclaw.json"))

MIGRATED_CONTENT = """# ⚠️ 已迁移

此目录的 asr-hotwords skill 已迁移到全局位置：

    ~/.openclaw/skills/asr-hotwords/

历史数据（output/vocab_*.json）已合并到新位置。
此目录可安全删除。
"""


def find_old_installations() -> list[Path]:
    """扫描所有 agent workspace 下的旧版 asr-hotwords 安装"""
    old_dirs = []

    if not OC_CONFIG.exists():
        logger.warning(f"未找到 {OC_CONFIG}")
        return old_dirs

    with open(OC_CONFIG, "r", encoding="utf-8") as f:
        oc_config = json.load(f)

    agents_cfg = oc_config.get("agents", {})
    defaults_ws = agents_cfg.get("defaults", {}).get("workspace", "")
    agent_list = agents_cfg.get("list", [])

    # 收集所有 workspace 路径
    workspaces = set()
    if defaults_ws:
        workspaces.add(os.path.expanduser(defaults_ws))
    for agent in agent_list:
        ws = agent.get("workspace", "")
        if ws:
            workspaces.add(os.path.expanduser(ws))

    # 检查每个 workspace 下是否有旧安装
    for ws in workspaces:
        old_path = Path(ws) / "skills" / "asr-hotwords"
        if old_path.exists() and old_path.is_dir():
            # 排除新位置自身
            if old_path.resolve() == NEW_SKILL_DIR.resolve():
                continue
            # 排除已迁移的
            if (old_path / "MIGRATED.md").exists():
                logger.info(f"跳过已迁移: {old_path}")
                continue
            old_dirs.append(old_path)

    # 也检查旧名称 asr-personal-hotwords
    for ws in workspaces:
        old_path = Path(ws) / "skills" / "asr-personal-hotwords"
        if old_path.exists() and old_path.is_dir():
            if (old_path / "MIGRATED.md").exists():
                continue
            old_dirs.append(old_path)

    return old_dirs


def merge_output(src_output: Path, dst_output: Path):
    """合并 vocab 文件，不覆盖已存在的"""
    if not src_output.exists():
        return 0

    dst_output.mkdir(parents=True, exist_ok=True)
    count = 0

    for vocab_file in sorted(src_output.glob("vocab_*.json")):
        dst_file = dst_output / vocab_file.name
        if dst_file.exists():
            logger.info(f"  跳过已存在: {vocab_file.name}")
            continue
        shutil.copy2(vocab_file, dst_file)
        count += 1
        logger.info(f"  迁移: {vocab_file.name}")

    return count


def migrate_markers(src: Path, dst: Path):
    """迁移标记文件"""
    for marker in [".installed", ".cron_configured"]:
        src_marker = src / marker
        dst_marker = dst / marker
        if src_marker.exists() and not dst_marker.exists():
            shutil.copy2(src_marker, dst_marker)
            logger.info(f"  迁移标记: {marker}")


def migrate():
    """执行迁移"""
    old_dirs = find_old_installations()

    if not old_dirs:
        print("未发现旧版安装，无需迁移。")
        return

    print(f"发现 {len(old_dirs)} 个旧版安装:")
    for d in old_dirs:
        print(f"  - {d}")

    NEW_SKILL_DIR.mkdir(parents=True, exist_ok=True)
    new_output = NEW_SKILL_DIR / "output"

    total_migrated = 0

    for old_dir in old_dirs:
        print(f"\n迁移: {old_dir}")

        # 1. 合并 output
        old_output = old_dir / "output"
        count = merge_output(old_output, new_output)
        total_migrated += count
        print(f"  vocab 文件: {count} 个迁移")

        # 2. 迁移标记文件
        migrate_markers(old_dir, NEW_SKILL_DIR)

        # 3. 迁移 hotwords.md（如果新位置没有）
        old_hw = old_dir / "hotwords.md"
        new_hw = NEW_SKILL_DIR / "hotwords.md"
        if old_hw.exists() and not new_hw.exists():
            shutil.copy2(old_hw, new_hw)
            print(f"  迁移: hotwords.md")

        # 4. 写入 MIGRATED.md
        with open(old_dir / "MIGRATED.md", "w", encoding="utf-8") as f:
            f.write(MIGRATED_CONTENT)
        print(f"  已标记为迁移完成")

    print(f"\n✅ 迁移完成，共迁移 {total_migrated} 个 vocab 文件")
    print(f"新位置: {NEW_SKILL_DIR}")
    print("\n旧目录已标记 MIGRATED.md，可手动删除。")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    migrate()
