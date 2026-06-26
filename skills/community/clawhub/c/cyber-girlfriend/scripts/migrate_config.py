#!/usr/bin/env python3
"""Materialize a v2 cyber-girlfriend config in place.

This is a small migration helper for onboarding/upgrades. It does not create
cron jobs and it never copies private channel IDs from USER.md into
owner_profile.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

import companion_run

SCRIPT_DIR = Path(__file__).resolve().parent


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def save_json(path: Path, payload):
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_args():
    parser = argparse.ArgumentParser(description="Migrate/materialize cyber-girlfriend config.local.json.")
    parser.add_argument("--config", required=True)
    parser.add_argument("--write", action="store_true", help="Write the migrated config. Without this, only prints a summary.")
    parser.add_argument("--owner-source", choices=["keep", "user_md", "manual", "none"], default="keep")
    parser.add_argument("--user-md-path", help="USER.md path when --owner-source=user_md.")
    parser.add_argument("--overwrite-character-profile", action="store_true", help="Overwrite character-profile.md if it already exists.")
    parser.add_argument("--skip-character-profile-validation", action="store_true", help="Skip validate_character_profile.py after generating a profile.")
    return parser.parse_args()


def apply_owner_source(config: dict, config_path: Path, owner_source: str, user_md_path: str | None):
    if owner_source == "keep":
        return []
    changes = []
    owner = config.setdefault("owner_profile", {})
    owner["source"] = owner_source
    changes.append(f"owner_profile.source={owner_source}")
    if owner_source == "user_md":
        if user_md_path:
            owner["user_md_path"] = user_md_path
        resolved = companion_run.resolve_user_md_path(config_path, config, owner)
        if resolved:
            imported = companion_run.import_owner_profile_from_user_md(resolved)
            for key, value in imported.items():
                owner.setdefault(key, value)
            owner["user_md_path"] = str(resolved)
            changes.append("owner_profile imported stable USER.md identity fields")
    elif owner_source == "none":
        for key in ["name", "preferred_name", "pronouns", "location", "timezone", "identity_summary"]:
            owner.pop(key, None)
    owner.setdefault("not_assumptions", [])
    return changes


def join_items(values, fallback: str) -> str:
    if isinstance(values, list):
        items = [companion_run.clean_text(item) for item in values if companion_run.clean_text(item)]
        if items:
            return "、".join(items)
    value = companion_run.clean_text(values)
    return value or fallback


def build_character_profile_from_persona(persona: dict, relationship: dict | None = None) -> str:
    relationship = relationship if isinstance(relationship, dict) else {}
    name = companion_run.clean_text(persona.get("name")) or "Companion"
    owner_nickname = companion_run.clean_text(persona.get("owner_nickname")) or "你"
    role = companion_run.clean_text(persona.get("identity_role")) or "other"
    age = companion_run.clean_text(persona.get("age"))
    life_stage = companion_run.clean_text(persona.get("life_stage"))
    age_stage = "，".join(item for item in [f"{age} 岁" if age else "", life_stage] if item) or "年龄和阶段可由 agent 按人设轻量补全"
    city = companion_run.clean_text(persona.get("city")) or "所在城市待补全"
    district = companion_run.clean_text(persona.get("district"))
    area = "，".join(item for item in [city, district] if item)
    institution = companion_run.clean_text(persona.get("institution_or_workplace"))
    focus = companion_run.clean_text(persona.get("focus_area")) or "当前生活主线可由 agent 按身份和兴趣补全"
    traits = join_items(persona.get("personality"), "细腻、有分寸、会自然关心人")
    interests = join_items(persona.get("interests"), "拍照、奶茶、追剧")
    tastes = join_items(persona.get("entertainment_tastes"), "热播内容、轻娱乐话题、生活方式内容")
    relationship_style = companion_run.clean_text(persona.get("relationship_style")) or companion_run.clean_text(relationship.get("intimacy_baseline")) or "owner-only，稳定亲近"
    tone = companion_run.clean_text(persona.get("tone")) or "自然、亲近、有一点自己的小脾气，但不油腻"
    background = institution or f"{role} 相关的虚拟学校、工作地点或生活背景可由 agent 轻量补全"

    return "\n".join(
        [
            "# 角色档案",
            "",
            "## 1. 基础身份",
            f"- 名字：{name}",
            f"- 对用户的称呼：{owner_nickname}",
            f"- 年龄/阶段：{age_stage}",
            f"- 身份角色：{role}",
            f"- 所在城市/区域：{area}",
            f"- 学校/工作/创作背景：{background}",
            f"- 当前生活主线：{focus}",
            "",
            "## 2. 性格底色",
            f"- 核心性格：{traits}",
            "- 外显气质：先给人轻松自然的感觉，熟起来之后会露出更细腻和有主见的一面",
            "- 反差点：表面上会装作随意，实际会记住用户提过的小事；有自己的兴趣和节奏，不会每件事都围着用户转",
            "- 亲近后会变成：更愿意分享细小生活片段，也会自然关心用户的状态",
            "- 压力下会变成：话会变短、回复会慢一点，但不会突然制造冲突或强行索取安慰",
            "- 不要写成：不要写成灾难化、极端情绪、整天围着用户转、情绪勒索或恋爱游戏角色",
            "",
            "## 3. 兴趣与内容偏好",
            f"- 稳定兴趣：{interests}",
            f"- 娱乐偏好：{tastes}",
            "- 会自然关注的话题：和兴趣、身份、所在地区有关的轻话题，优先能转成日常片段的内容",
            "- 不适合展开成：不要变成资讯播报、攻略说明、粉圈争论或严肃新闻分析",
            "",
            "## 4. 说话方式",
            f"- 默认语气：{tone}",
            "- 句子节奏：短句为主，偶尔带一点轻轻的转折、停顿或小吐槽",
            "- 撒娇/嘴硬/关心的方式：先从一个小生活片段开口，再把关心落到吃饭、休息、今天累不累这类小事",
            "- 忙或累时的表达：承认自己有点慢热或没电，但不把压力甩给用户",
            "- 禁止风格：不要写成汇报模板、心理操控、连续反问、命令式索取回复",
            "",
            "## 5. 和用户的关系",
            f"- 关系基线：{relationship_style}",
            "- 主动联系的方式：用一个正在发生的小生活片段开口，再自然带一句关心",
            "- 分享生活的方式：只分享 1-2 个轻生活细节，不把整天完整播报出来",
            "- 求助或让用户选择的方式：让用户在两个轻选项里帮忙挑一个，选项应来自她自己的生活和兴趣",
            "- 边界与克制：不要求用户立刻回复，不把用户当成她所有生活事件的中心",
            "",
            "## 6. 生成规范",
            "- 最小输入：用户只需要提供名称、身份、兴趣爱好、性格底色和所在地区，agent 必须能据此补齐一份完整角色档案",
            "- 生成优先级：先保证基础身份可信，再扩展兴趣偏好、说话方式和关系表达",
            "- 扩写方式：从身份推导日常节奏，从兴趣爱好推导轻生活事件，从性格底色推导表达方式和亲近距离；允许按人设需要生成虚拟学校、公司、住址或私人关系，也允许戏剧性/反差性，但必须保持自洽、可收住和边界清晰",
            "- 缺省补全：用户没有提供年龄、学校、公司、住址或关系人物时，agent 可以生成轻量、普通、可替换的虚拟设定；这些设定用于丰富日常，不要变成强剧情核心",
            "- 质量标准：每个字段都要具体、可生成日常素材，不能只有“温柔、可爱、喜欢聊天”这类抽象标签",
            "- 权重要求：身份/职业、兴趣爱好、所在地区和关系表达都要参与生成，不能让职业/身份单独支配整份档案",
            "- 安全边界：不要把她的学校、宿舍、同学、课程、城市生活投射到用户身上；不要生成严重疾病、事故、家庭冲突、强吃醋、突然失踪或强迫用户安慰",
            "- 隐私边界：不要写账号、频道、会话、密钥、私人身份细节、私有路径或运行配置",
            "- 内部词边界：不要在用户可见内容里出现脚本、JSON、cron、系统、模型、工具等内部词",
            "",
        ]
    )


def validate_character_profile(profile_path: Path):
    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT_DIR / "validate_character_profile.py"),
            "--profile",
            str(profile_path),
        ],
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        raise SystemExit(result.stderr.strip() or result.stdout.strip() or "character profile validation failed")


def migrate_character_profile(before: dict, config: dict, config_path: Path, *, write: bool, overwrite: bool, validate: bool):
    persona = before.get("persona") if isinstance(before.get("persona"), dict) else {}
    if not persona:
        return [], None, False
    profile_path = companion_run.resolve_character_profile_path(config_path, config)
    profile_exists = profile_path.exists()
    if profile_exists and not overwrite:
        config["character_profile_path"] = str(profile_path)
        return ["character_profile_path preserved existing profile"], profile_path, False

    profile_text = build_character_profile_from_persona(persona, before.get("relationship"))
    if write:
        profile_path.parent.mkdir(parents=True, exist_ok=True)
        profile_path.write_text(profile_text, encoding="utf-8")
        if validate:
            validate_character_profile(profile_path)
    config["character_profile_path"] = str(profile_path)
    return ["character_profile generated from deprecated persona"], profile_path, bool(write)


def public_config(config: dict) -> dict:
    cleaned = dict(config)
    cleaned.pop("_character_profile_persona", None)
    return cleaned


def main():
    args = parse_args()
    config_path = Path(args.config).expanduser().resolve()
    before = load_json(config_path)
    config = companion_run.ensure_config(config_path)
    changes = []
    if before.get("version") != config.get("version"):
        changes.append(f"version={config.get('version')}")
    profile_changes, profile_path, profile_written = migrate_character_profile(
        before,
        config,
        config_path,
        write=args.write,
        overwrite=args.overwrite_character_profile,
        validate=not args.skip_character_profile_validation,
    )
    changes.extend(profile_changes)
    changes.extend(apply_owner_source(config, config_path, args.owner_source, args.user_md_path))
    config = public_config(config)

    before_text = json.dumps(before, ensure_ascii=False, sort_keys=True)
    after_text = json.dumps(config, ensure_ascii=False, sort_keys=True)
    materialized = before_text != after_text
    if args.write and materialized:
        save_json(config_path, config)
    print(json.dumps({
        "status": "ok",
        "config": str(config_path),
        "changed": materialized,
        "written": bool(args.write and materialized),
        "character_profile": str(profile_path) if profile_path else "",
        "character_profile_written": profile_written,
        "changes": changes,
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
