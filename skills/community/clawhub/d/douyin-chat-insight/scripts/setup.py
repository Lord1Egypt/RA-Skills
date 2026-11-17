#!/usr/bin/env python3
"""First-run setup: no secrets, no Bailian required."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# allow running as script
sys.path.insert(0, str(Path(__file__).resolve().parent))

from core import default_output_dir, load_config, save_config
from setup_config import detect_existing_setup


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Douyin Chat Insight 首次配置（无需 API Key / 登录）")
    p.add_argument("--output-dir", type=Path, help="报告输出目录")
    p.add_argument("--owner-alias", action="append", default=[], help="群主/主理人昵称，可重复")
    p.add_argument("--config", type=Path, help="配置写入路径")
    p.add_argument("--json", action="store_true")
    p.add_argument("--check", action="store_true", help="只检查，不写")
    args = p.parse_args(argv)

    det = detect_existing_setup(args.config)
    cfg = load_config(args.config)

    if not args.check:
        if args.output_dir:
            cfg["output_dir"] = str(args.output_dir.expanduser())
        elif not cfg.get("output_dir"):
            cfg["output_dir"] = str(default_output_dir())
        aliases = list(cfg.get("owner_aliases") or [])
        for a in args.owner_alias:
            if a and a not in aliases:
                aliases.append(a)
        cfg["owner_aliases"] = aliases
        path = save_config(cfg, args.config)
        det = detect_existing_setup(path)
        det["wrote"] = str(path)
    else:
        det["wrote"] = None

    # human guidance
    guide = {
        "needs_bailian_appkey": False,
        "needs_douyin_login": False,
        "needs_docker": False,
        "independent_of_creator_insight": True,
        "install_steps": [
            "1. 安装本 skill 到 Agent skills 目录（ClawHub 或 git clone）",
            "2. python3 scripts/setup.py   # 可选，只设输出目录/群主别名",
            "3. 准备自备导出文件（见 references/how-to-get-exports.md）",
            "4. python3 scripts/run.py --input /path/to/export",
            "5. 查看 inventory 后: python3 scripts/run.py --input ... --conv 1",
        ],
        "if_other_skills_installed": (
            "检测到兄弟 skill 时仅展示状态，不读取其收藏账本/浏览器 profile，"
            "不要求复用配置。可选视频转写若未来启用，才会探测 DASHSCOPE_API_KEY。"
        ),
        "siblings": det.get("siblings"),
    }

    out = {"setup": det, "guide": guide}
    if args.json:
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        print("=== Douyin Chat Insight Setup ===")
        print(f"配置文件: {det.get('config_path') or '（将写入默认路径）'}")
        print(f"输出目录: {det.get('output_dir')}")
        print(f"群主别名: {det.get('owner_aliases') or '[]'}")
        print(f"需要阿里百炼 AppKey: 否（核心路径）")
        print(f"需要抖音登录: 否")
        print(f"已装兄弟 skill: " + ", ".join(k for k,v in (det.get('siblings') or {}).items() if v and k != 'dashscope_key_present') or "无")
        print(f"本机存在 DASHSCOPE_API_KEY: {det.get('cloud_asr_optional')}")
        print("可选端口: 聊天内抖音链接 ASR → references/optional-douyin-link-asr.md（不强制）")
        if det.get("wrote"):
            print(f"已写入: {det['wrote']}")
        print("\n首次使用步骤:")
        for s in guide["install_steps"]:
            print(" ", s)
        print("\n详细: README.md / docs/INSTALL.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
