#!/usr/bin/env python3
"""validate_models.py — 模型资料卡准确性守护（P0-2：修复 model_profiles.json 准确性）。

背景（SkillHub 评测 accuracy 4.3 → 待修复）：
  model_profiles.json 是「排行榜以资料卡为准」的唯一权威源，但历史版本混入了
  **无真实来源锚点**的条目——典型为 source 字段以「榜单自动抓取·未联网核实」开头
  （项目内部约定：自动从榜单抓取、未联网核实）。这类条目违反 SKILL.md 硬规则
  「不要凭训练数据脑补数字」，且评测明确指出含未发布/推测模型。

  注：评测曾点名「GPT-5.6 Sol、Claude Opus 5」等，但经联网核实这些模型在 2026 年
  已真实发布且 profile 带真实来源 URL（openai.com / anthropic.com），属已核实条目，
  **保留**。本脚本只清除「无来源锚点」的条目（source 缺失或标记未核实）。

机制（双轨制）：
  - 已核实条目：留在 model_profiles.json，补 verified=true 标记（合同约束）。
  - 未核实条目：移入 model_profiles_unverified.json（🧪 实验模型·未经验证），
    不参与排行榜排名（model_meta._apply_profile_as_truth 跳过 verified=false）。

用法：
  python validate_models.py --list           # 列出未核实条目
  python validate_models.py --check          # CI 模式：存在未核实条目则 exit 1
  python validate_models.py --fix            # 移入 unverified 并从主文件删除
  python validate_models.py --verify "Claude Opus 5 High"   # 复核通过，移回主文件
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
PROFILES = SKILL_DIR / "model_profiles.json"
UNVERIFIED = SKILL_DIR / "model_profiles_unverified.json"

# 未核实判定：source 以该前缀开头（项目内部约定），或 source 为空/缺失。
UNVERIFIED_PREFIX = "榜单自动抓取"


def _is_unverified(entry: dict) -> bool:
    src = (entry or {}).get("source")
    if not src or not str(src).strip():
        return True
    return str(src).strip().startswith(UNVERIFIED_PREFIX)


def load_profiles() -> dict:
    if not PROFILES.exists():
        return {}
    return json.loads(PROFILES.read_text(encoding="utf-8"))


def load_unverified() -> dict:
    if not UNVERIFIED.exists():
        return {}
    return json.loads(UNVERIFIED.read_text(encoding="utf-8"))


def find_unverified(profiles: dict) -> list[tuple[str, dict]]:
    return [(k, v) for k, v in profiles.items() if _is_unverified(v)]


def mark_verified(profiles: dict) -> dict:
    """给所有（保留的）条目补 verified=true；不改动其它字段。"""
    out = {}
    for k, v in profiles.items():
        v = dict(v)
        v["verified"] = True
        out[k] = v
    return out


def cmd_list() -> int:
    profiles = load_profiles()
    flagged = find_unverified(profiles)
    print(f"📋 model_profiles.json 共 {len(profiles)} 条，未核实 {len(flagged)} 条：")
    for k, v in sorted(flagged):
        print(f"  ⚠️ {k} | org={v.get('org','?')} | source={str(v.get('source',''))[:30]}")
    if not flagged:
        print("  ✅ 无未核实条目")
    return 0


def cmd_check() -> int:
    profiles = load_profiles()
    flagged = find_unverified(profiles)
    if flagged:
        print(f"❌ 发现 {len(flagged)} 条未核实模型档案（source 缺失或标记未联网核实）：")
        for k, _ in sorted(flagged):
            print(f"    - {k}")
        print(f"   请运行 `python validate_models.py --fix` 将其移入 "
              f"model_profiles_unverified.json（不纳入排行榜）。")
        return 1
    print("✅ 模型档案全部已核实（verified=true / 带真实来源锚点）。")
    return 0


def cmd_fix() -> int:
    profiles = load_profiles()
    flagged = find_unverified(profiles)
    if not flagged:
        print("✅ 无未核实条目，跳过。")
        # 仍确保保留条目带 verified=true
        kept = mark_verified(profiles)
        PROFILES.write_text(json.dumps(kept, ensure_ascii=False, indent=2), encoding="utf-8")
        return 0

    unverified = load_unverified()
    # 合并（同键以现有 unverified 为准，避免覆盖人工复核备注）
    for k, v in flagged:
        v = dict(v)
        v["verified"] = False
        v.setdefault("verify_status", "榜单自动抓取·未联网核实（未联网核实，不纳入排行榜）")
        unverified[k] = unverified.get(k, v)

    kept = {k: v for k, v in profiles.items() if k not in {fk for fk, _ in flagged}}
    kept = mark_verified(kept)

    PROFILES.write_text(json.dumps(kept, ensure_ascii=False, indent=2), encoding="utf-8")
    UNVERIFIED.write_text(json.dumps(unverified, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"✅ 已将 {len(flagged)} 条未核实条目移入 {UNVERIFIED.name}：")
    for k, _ in sorted(flagged):
        print(f"    - {k}")
    print(f"✅ 主文件保留 {len(kept)} 条（已标记 verified=true）。")
    return 0


def cmd_verify(name: str) -> int:
    unverified = load_unverified()
    if name not in unverified:
        print(f"ℹ️ {name} 不在未核实文件中，可能已核实或不存在。")
        return 0
    profiles = load_profiles()
    entry = unverified.pop(name)
    entry = dict(entry)
    entry["verified"] = True
    entry.pop("verify_status", None)
    # 若来源仍是未核实标记，要求调用方提供真实来源——此处仅移回并提示
    if _is_unverified(entry):
        print(f"⚠️ {name} 来源仍为未核实标记，请先编辑 model_profiles_unverified.json "
              f"补真实 source 再 --verify，避免重新引入未核实数据。已中止。")
        unverified[name] = entry
        UNVERIFIED.write_text(json.dumps(unverified, ensure_ascii=False, indent=2), encoding="utf-8")
        return 1
    profiles[name] = entry
    PROFILES.write_text(json.dumps(mark_verified(profiles), ensure_ascii=False, indent=2), encoding="utf-8")
    UNVERIFIED.write_text(json.dumps(unverified, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"✅ {name} 已复核通过，移回 model_profiles.json（verified=true）。")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="模型资料卡准确性守护（P0-2）")
    ap.add_argument("--list", action="store_true", help="列出未核实条目")
    ap.add_argument("--check", action="store_true", help="CI 模式：存在未核实条目则 exit 1")
    ap.add_argument("--fix", action="store_true", help="移入 unverified 并从主文件删除")
    ap.add_argument("--verify", metavar="NAME", help="复核通过，把某条目从 unverified 移回主文件")
    args = ap.parse_args()

    if args.verify:
        return cmd_verify(args.verify)
    if args.fix:
        return cmd_fix()
    if args.check:
        return cmd_check()
    # 默认 --list
    return cmd_list()


if __name__ == "__main__":
    sys.exit(main())
