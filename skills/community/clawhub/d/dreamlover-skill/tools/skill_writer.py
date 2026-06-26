from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from skill_linter import lint_skill_dir
from slugify import slugify

CANON_HEADERS = [
    "## Basic Identity",
    "## Setting Attributes",
    "## Key Plot Events",
    "## Confirmed Relationships",
    "## Official Statements And Notes",
]
PERSONA_HEADERS = [
    "## Behavior Patterns",
    "## Emotional Tendencies",
    "## Interaction Style",
    "## Relationship Progression",
    "## Boundaries And Preferences",
]
STYLE_HEADERS = [
    "## Address Patterns",
    "## Rhythm And Sentence Shape",
    "## Verbal Tics",
    "## Short Example Lines",
]
DEFAULT_INSTALL_ROOT = Path(".agents") / "skills"
DEFAULT_ARCHIVE_ROOT = Path("characters")
DEFAULT_SOURCE_TYPES = ["user"]
DEFAULT_SOURCE_DECISION_POLICY = "user_only"
DEFAULT_INPUT_MODE = "direct_text"
DEFAULT_SEARCH_SCOPE = "none"
SOURCE_DECISION_POLICIES = {
    "1": "user_only",
    "2": "official_wiki_only",
    "3": "official_plus_user",
    "4": "official_quick",
}
SOURCE_DECISION_LABELS = {
    "user_only": "仅使用你提供的信息",
    "official_wiki_only": "官方资料 + wiki 资料",
    "official_plus_user": "官方资料 + 你提供的信息",
    "official_quick": "快速生成",
}
INPUT_MODES = {
    "1": "direct_text",
    "2": "file_path",
}
SEARCH_SCOPES = {
    "1": "small",
    "2": "medium",
    "3": "large",
}
INPUT_MODE_LABELS = {
    "direct_text": "直接贴文本",
    "file_path": "文件路径",
}
SEARCH_SCOPE_LABELS = {
    "none": "不联网补全",
    "small": "小范围补全",
    "medium": "中范围补全",
    "large": "大范围补全",
}
CANONICAL_SLOTS = [
    "source_policy",
    "input_mode",
    "character_name",
    "source_work",
    "material_types",
    "allow_low_confidence_persona",
    "archive_mirror",
]
SOURCE_POLICY_ALIASES = {
    "1": "user_only",
    "只用我给的信息": "user_only",
    "只用用户提供的信息": "user_only",
    "仅用用户信息": "user_only",
    "仅用我提供的信息": "user_only",
    "user_only": "user_only",
    "2": "official_wiki_only",
    "官方资料+wiki资料": "official_wiki_only",
    "官方资料+wiki": "official_wiki_only",
    "官方+wikis资料": "official_wiki_only",
    "官方+wiki": "official_wiki_only",
    "official_wiki_only": "official_wiki_only",
    "3": "official_plus_user",
    "官方资料+用户资料": "official_plus_user",
    "官方+用户": "official_plus_user",
    "官方资料+我提供的信息": "official_plus_user",
    "official_plus_user": "official_plus_user",
    "4": "official_quick",
    "快速生成": "official_quick",
    "快速": "official_quick",
    "快生成": "official_quick",
    "official_quick": "official_quick",
}
INPUT_MODE_ALIASES = {
    "1": "direct_text",
    "直接输送信息": "direct_text",
    "直接输入信息": "direct_text",
    "我直接贴文本": "direct_text",
    "聊天里贴文本": "direct_text",
    "直接贴文本": "direct_text",
    "chat": "direct_text",
    "direct_text": "direct_text",
    "2": "file_path",
    "文件路径": "file_path",
    "路径": "file_path",
    "给你文件路径": "file_path",
    "读取文件路径": "file_path",
    "file_path": "file_path",
}
SEARCH_SCOPE_ALIASES = {
    "1": "small",
    "小": "small",
    "小范围": "small",
    "small": "small",
    "2": "medium",
    "中": "medium",
    "中范围": "medium",
    "medium": "medium",
    "3": "large",
    "大": "large",
    "大范围": "large",
    "large": "large",
}
SOURCE_TYPE_SYNONYMS = {
    "official": "official",
    "official-setting": "official",
    "official_profile": "official",
    "官方": "official",
    "官方资料": "official",
    "plot": "plot",
    "plot-summary": "plot",
    "story": "plot",
    "剧情": "plot",
    "剧情摘要": "plot",
    "quotes": "quotes",
    "quote": "quotes",
    "dialogue": "quotes",
    "台词": "quotes",
    "台词摘录": "quotes",
    "wiki": "wiki",
    "维基": "wiki",
    "wiki资料": "wiki",
    "user": "user",
    "manual": "user",
    "user-description": "user",
    "用户": "user",
    "用户描述": "user",
}
SECTION_PLACEHOLDERS = {
    "## Basic Identity": "- 暂无已确认的基础身份信息。",
    "## Setting Attributes": "- 暂无已确认的设定属性。",
    "## Key Plot Events": "- 暂无已确认的关键剧情事件。",
    "## Confirmed Relationships": "- 暂无已确认的角色关系。",
    "## Official Statements And Notes": "- 暂无已确认的官方口径或补充备注。",
    "## Behavior Patterns": "- 暂无已归纳的行为模式。",
    "## Emotional Tendencies": "- 暂无已归纳的情绪反应倾向。",
    "## Interaction Style": "- 暂无已归纳的互动方式。",
    "## Relationship Progression": "- 暂无已归纳的关系推进逻辑。",
    "## Boundaries And Preferences": "- 暂无已归纳的禁忌或偏好。",
    "## Address Patterns": "- 暂无已整理的称呼方式。",
    "## Rhythm And Sentence Shape": "- 暂无已整理的句式与节奏。",
    "## Verbal Tics": "- 暂无已整理的口头习惯。",
    "## Short Example Lines": "- 暂无已整理的短句样例。",
}
CANON_PREFIXES = {
    "identity": "## Basic Identity",
    "basic": "## Basic Identity",
    "attribute": "## Setting Attributes",
    "setting": "## Setting Attributes",
    "event": "## Key Plot Events",
    "plot": "## Key Plot Events",
    "relation": "## Confirmed Relationships",
    "relationship": "## Confirmed Relationships",
    "official": "## Official Statements And Notes",
    "note": "## Official Statements And Notes",
}
PERSONA_PREFIXES = {
    "behavior": "## Behavior Patterns",
    "emotion": "## Emotional Tendencies",
    "interaction": "## Interaction Style",
    "progression": "## Relationship Progression",
    "relationship": "## Relationship Progression",
    "boundary": "## Boundaries And Preferences",
    "preference": "## Boundaries And Preferences",
}
STYLE_PREFIXES = {
    "address": "## Address Patterns",
    "rhythm": "## Rhythm And Sentence Shape",
    "sentence": "## Rhythm And Sentence Shape",
    "tic": "## Verbal Tics",
    "verbal": "## Verbal Tics",
    "example": "## Short Example Lines",
    "line": "## Short Example Lines",
}
INTERACTIVE_SENTINEL = "END"
RUNTIME_SCRIPT_NAMES = [
    "memory_prepare.py",
    "memory_fetch.py",
    "memory_commit.py",
    "memory_summarize.py",
    "memory_logic.py",
    "memory_store.py",
]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def parse_scope(value: str) -> str:
    allowed = {"codex", "archive", "both"}
    if value not in allowed:
        raise argparse.ArgumentTypeError(f"Unsupported scope: {value}")
    return value


def resolve_root(base_root: Path, value: str | None, fallback: Path) -> Path:
    if not value:
        return base_root / fallback
    path = Path(value)
    return path if path.is_absolute() else base_root / path


def read_text(path: str | None) -> str | None:
    if not path:
        return None
    return Path(path).read_text(encoding="utf-8")


def write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def relative_path(base_root: Path, path: Path | None) -> str | None:
    if path is None:
        return None
    return path.relative_to(base_root).as_posix()


def load_existing_meta(paths: list[Path]) -> dict:
    for path in paths:
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8"))
    return {}


def load_existing_text(paths: list[Path]) -> str | None:
    for path in paths:
        if path.exists():
            return path.read_text(encoding="utf-8")
    return None


def default_markdown(headers: list[str]) -> str:
    blocks = [f"{header}\n\n{SECTION_PLACEHOLDERS[header]}" for header in headers]
    return "\n\n".join(blocks) + "\n"


def is_placeholder_line(line: str) -> bool:
    stripped = line.strip()
    if not stripped:
        return False
    return stripped == "- TODO" or stripped in SECTION_PLACEHOLDERS.values()


def normalize_header_line(line: str) -> str:
    return line.strip().lstrip("\ufeff")


def parse_section_segments(text: str, headers: list[str]) -> dict[str, list[list[str]]]:
    segments = {header: [] for header in headers}
    current_header: str | None = None
    current_lines: list[str] = []

    def flush() -> None:
        nonlocal current_header, current_lines
        if current_header is not None:
            segments[current_header].append(current_lines[:])
        current_header = None
        current_lines = []

    for raw_line in text.splitlines():
        stripped = normalize_header_line(raw_line)
        if stripped in headers:
            flush()
            current_header = stripped
            current_lines = []
            continue
        if stripped.startswith("## "):
            flush()
            continue
        if current_header is not None:
            current_lines.append(raw_line)

    flush()
    return segments


def choose_section_body(segments: list[list[str]], placeholder: str) -> str:
    best_lines: list[str] | None = None
    best_score = -1
    for candidate in segments:
        meaningful = [line for line in candidate if line.strip() and not is_placeholder_line(line)]
        score = len(meaningful)
        if score > best_score:
            best_score = score
            best_lines = candidate
    lines = [line.rstrip() for line in (best_lines or [])]
    lines = [line for line in lines if line.strip()]
    if not lines:
        return placeholder
    meaningful = [line for line in lines if not is_placeholder_line(line)]
    if meaningful:
        lines = meaningful
    return "\n".join(lines)


def ensure_sections(text: str | None, headers: list[str]) -> str:
    if not text or not text.strip():
        return default_markdown(headers)
    segments = parse_section_segments(text, headers)
    blocks = []
    for header in headers:
        body = choose_section_body(segments[header], SECTION_PLACEHOLDERS[header])
        blocks.append(f"{header}\n\n{body}")
    return "\n\n".join(blocks) + "\n"


def validate_cross_headers(text: str, forbidden: list[str], label: str) -> None:
    for header in forbidden:
        if header in text:
            raise ValueError(f"{label} contains forbidden section header: {header}")


def normalize_source_types(raw: str | None) -> list[str]:
    if not raw:
        return list(DEFAULT_SOURCE_TYPES)
    normalized: list[str] = []
    for item in raw.replace("，", ",").split(","):
        token = item.strip().lower()
        if not token:
            continue
        normalized_token = SOURCE_TYPE_SYNONYMS.get(token)
        if normalized_token is None:
            raise ValueError(f"Unsupported source type: {item.strip()}")
        if normalized_token not in normalized:
            normalized.append(normalized_token)
    return normalized or list(DEFAULT_SOURCE_TYPES)


def parse_bool_flag(value: str | None, default: bool = False) -> bool:
    if value is None:
        return default
    normalized = value.strip().lower()
    if normalized in {
        "1",
        "true",
        "t",
        "yes",
        "y",
        "允许",
        "允许推断",
        "允许补充",
        "可以",
        "可以补充",
    }:
        return True
    if normalized in {
        "0",
        "false",
        "f",
        "no",
        "n",
        "不允许",
        "不允许推断",
        "不要补充",
        "不可以",
        "否",
    }:
        return False
    raise ValueError(f"Unsupported boolean value: {value}")


def prompt_required(prompt: str, default: str | None = None) -> str:
    shown_default = default if default else None
    suffix = f" [{shown_default}]" if shown_default else ""
    while True:
        value = input(f"{prompt}{suffix}: ").strip()
        if value:
            return value
        if shown_default is not None:
            return shown_default
        print("这一项需要填写。")


def prompt_yes_no(prompt: str, default: bool = False) -> bool:
    default_label = "默认是" if default else "默认否"
    while True:
        value = input(f"{prompt} [{default_label}]: ").strip()
        if not value:
            return default
        try:
            return parse_bool_flag(value)
        except ValueError:
            print("请回答“是”或“否”。")


def prompt_choice(
    prompt: str,
    choices: dict[str, str],
    default_key: str | None = None,
    labels: dict[str, str] | None = None,
    aliases: dict[str, str] | None = None,
) -> str:
    default_suffix = f" [{default_key}]" if default_key else ""
    while True:
        print(prompt)
        for key, value in choices.items():
            label = labels.get(value, value) if labels else value
            print(f"{key}）{label}")
        value = input(f"请选择{default_suffix}: ").strip()
        if not value and default_key:
            value = default_key
        normalized_value = value.strip().lower()
        if aliases and normalized_value in aliases:
            return aliases[normalized_value]
        if value in choices:
            return choices[value]
        print("请选择有效选项。")


def prompt_multiline(prompt: str) -> str:
    print(f"{prompt} 输入完成后，单独输入一行 {INTERACTIVE_SENTINEL} 结束。")
    lines: list[str] = []
    while True:
        line = input()
        if line.strip() == INTERACTIVE_SENTINEL:
            break
        lines.append(line.rstrip())
    return "\n".join(lines).strip()


def read_source_paths(raw_paths: str) -> tuple[list[str], str]:
    paths: list[str] = []
    contents: list[str] = []
    for raw_line in raw_paths.splitlines():
        candidate = raw_line.strip()
        if not candidate:
            continue
        path = Path(candidate)
        if not path.exists():
            raise FileNotFoundError(f"Source path not found: {candidate}")
        paths.append(candidate)
        contents.append(path.read_text(encoding="utf-8"))
    if not paths:
        raise ValueError("At least one source path is required when input mode is file_path.")
    return paths, "\n\n".join(contents).strip()


def build_slot_state(existing: dict) -> dict:
    return {
        "source_policy": existing.get("source_decision_policy"),
        "input_mode": existing.get("input_mode"),
        "character_name": existing.get("character_name") or existing.get("requested_character_name"),
        "source_work": existing.get("source_work"),
        "material_types": existing.get("source_types"),
        "allow_low_confidence_persona": existing.get("allow_low_confidence_persona"),
        "archive_mirror": existing.get("archive_mirror"),
    }


def infer_material_types_from_policy(source_policy: str) -> list[str]:
    if source_policy == "user_only":
        return normalize_source_types("user")
    if source_policy == "official_wiki_only":
        return normalize_source_types("official,wiki")
    if source_policy == "official_plus_user":
        return normalize_source_types("official,user")
    return normalize_source_types("official")


def compute_missing_slots(slot_state: dict, source_policy: str | None) -> list[str]:
    required = ["source_policy", "character_name", "material_types", "allow_low_confidence_persona", "archive_mirror"]
    if source_policy in {"user_only", "official_plus_user"}:
        required.append("input_mode")
    if source_policy != "official_quick" and slot_state.get("source_work") is None:
        required.append("source_work")
    return [slot for slot in CANONICAL_SLOTS if slot in required and slot_state.get(slot) is None]


def normalize_note_line(line: str) -> str:
    stripped = line.strip()
    if stripped.startswith("- "):
        stripped = stripped[2:].strip()
    return stripped


def parse_prefixed_notes(
    raw: str,
    headers: list[str],
    prefix_map: dict[str, str],
    default_header: str,
) -> dict[str, list[str]]:
    bucket = {header: [] for header in headers}
    for raw_line in raw.splitlines():
        line = normalize_note_line(raw_line)
        if not line:
            continue
        if ":" in line:
            prefix, value = line.split(":", 1)
            header = prefix_map.get(prefix.strip().lower())
            if header:
                cleaned = value.strip()
                if cleaned:
                    bucket[header].append(cleaned)
                continue
        bucket[default_header].append(line)
    return bucket


def render_markdown_from_sections(headers: list[str], sections: dict[str, list[str]]) -> str:
    blocks = []
    for header in headers:
        lines = sections.get(header) or []
        body = "\n".join(f"- {line}" for line in lines) if lines else SECTION_PLACEHOLDERS[header]
        blocks.append(f"{header}\n\n{body}")
    return "\n\n".join(blocks) + "\n"


def merge_section_defaults(
    sections: dict[str, list[str]],
    defaults: dict[str, list[str]],
) -> dict[str, list[str]]:
    merged = {header: list(sections.get(header, [])) for header in defaults}
    for header, lines in defaults.items():
        if not merged[header]:
            merged[header] = list(lines)
    return merged


def build_minimal_persona_defaults(target_use: str, allow_low_confidence: bool) -> dict[str, list[str]]:
    if allow_low_confidence:
        return {
            "## Behavior Patterns": [
                f"当前资料较少时，优先让角色表现服务于用户当前目标：{target_use}。"
            ],
            "## Emotional Tendencies": [
                "当证据不足时，情绪表达应当克制，不要擅自补出强烈而无依据的反应。"
            ],
            "## Interaction Style": [
                "优先使用清晰、贴近角色的回应方式；遇到不确定特质时，用收敛表达代替新增设定。"
            ],
            "## Relationship Progression": [
                "关系应随对话逐步推进，不要一开始就默认已经建立很深的信赖。"
            ],
            "## Boundaries And Preferences": [
                "即使允许低置信度人格补充，也不能把推断包装成已确认事实。"
            ],
        }
    return {
        "## Behavior Patterns": [
            "当前缺少足够的人格资料，因此行为表现应当克制，避免使用强烈但无依据的特征。"
        ],
        "## Emotional Tendencies": [
            "在补充更多资料前，默认使用温和、受控的情绪表达。"
        ],
        "## Interaction Style": [
            "先以稳定、自然的角色口吻回应，不要擅自补出未提供的内心动机。"
        ],
        "## Relationship Progression": [
            "没有后续资料或用户明确指引时，不要强行推进亲密或敌对关系。"
        ],
        "## Boundaries And Preferences": [
            "当回答依赖缺失的人格信息时，宁可保守处理，也不要编造细节。"
        ],
    }


def build_minimal_style_defaults(target_use: str) -> dict[str, list[str]]:
    return {
        "## Address Patterns": [
            "先使用适合当前对话的自然称呼，不要过早锁定没有依据的敬语习惯。"
        ],
        "## Rhythm And Sentence Shape": [
            f"句式和节奏以稳定、自然、便于对话为主，服务当前目标：{target_use}。"
        ],
        "## Verbal Tics": [
            "除非资料里明确提供，否则不要擅自添加口头禅。"
        ],
        "## Short Example Lines": [
            "我在这里，你可以直接和我说。",
        ],
    }


def build_minimal_canon_defaults() -> dict[str, list[str]]:
    return {
        "## Basic Identity": [],
        "## Setting Attributes": [
            "当前录入资料中没有更多已确认的设定属性。"
        ],
        "## Key Plot Events": [
            "当前录入资料中没有更多明确剧情事件。"
        ],
        "## Confirmed Relationships": [
            "当前录入资料中没有更多明确关系。"
        ],
        "## Official Statements And Notes": [
            "当前录入资料中没有更多明确官方口径或补充备注。"
        ],
    }


def build_canon_markdown(name: str, source_work: str, note_blocks: dict[str, list[str]]) -> str:
    sections = {header: list(note_blocks.get(header, [])) for header in CANON_HEADERS}
    sections = merge_section_defaults(sections, build_minimal_canon_defaults())
    identity = sections["## Basic Identity"]
    if name:
        identity.insert(0, f"角色名：{name}")
    if source_work:
        identity.append(f"来源作品：{source_work}")
    return render_markdown_from_sections(CANON_HEADERS, sections)


def build_persona_markdown(
    note_blocks: dict[str, list[str]],
    target_use: str,
    allow_low_confidence: bool,
) -> str:
    sections = {header: list(note_blocks.get(header, [])) for header in PERSONA_HEADERS}
    sections = merge_section_defaults(
        sections,
        build_minimal_persona_defaults(target_use, allow_low_confidence),
    )
    return render_markdown_from_sections(PERSONA_HEADERS, sections)


def build_style_markdown(note_blocks: dict[str, list[str]], target_use: str) -> str:
    sections = {header: list(note_blocks.get(header, [])) for header in STYLE_HEADERS}
    sections = merge_section_defaults(sections, build_minimal_style_defaults(target_use))
    return render_markdown_from_sections(STYLE_HEADERS, sections)


def build_normalized_payload(
    intake: dict,
    raw_material_notes: str,
    canon_notes: str,
    persona_notes: str,
    style_notes: str,
    source_paths: list[str],
    updated_at: str,
) -> dict:
    entries: list[dict] = []

    def push_entry(kind: str, text: str, entry_id: str) -> None:
        if text.strip():
            entries.append(
                {
                    "entry_id": entry_id,
                    "text": text.strip(),
                    "kind": kind,
                    "line_start": 1,
                    "line_end": len(text.splitlines()),
                }
            )

    push_entry("source_summary", raw_material_notes, "intake-001")
    push_entry("canon_notes", canon_notes, "intake-002")
    push_entry("persona_notes", persona_notes, "intake-003")
    push_entry("style_notes", style_notes, "intake-004")

    return {
        "schema_version": "0.4",
        "source": {
            "source_type": "interactive-intake",
            "input_path": "",
            "normalized_at": updated_at,
            "source_types": intake["source_types"],
            "source_decision_policy": intake["source_decision_policy"],
            "input_mode": intake["input_mode"],
            "search_scope": intake.get("search_scope", DEFAULT_SEARCH_SCOPE),
            "archive_mirror": intake.get("archive_mirror", True),
            "source_paths": source_paths,
        },
        "intake": {
            "character_name": intake["character_name"],
            "source_work": intake["source_work"],
            "target_use": intake["target_use"],
            "source_types": intake["source_types"],
            "allow_low_confidence_persona": intake["allow_low_confidence_persona"],
            "source_decision_policy": intake["source_decision_policy"],
            "input_mode": intake["input_mode"],
            "search_scope": intake.get("search_scope", DEFAULT_SEARCH_SCOPE),
            "archive_mirror": intake.get("archive_mirror", True),
            "source_paths": source_paths,
            "confirmed": intake["confirmed"],
        },
        "entries": entries,
    }


def build_child_skill(platform: str, name: str, slug: str, target_use: str, allow_low_confidence: bool) -> str:
    confidence_line = (
        "Low-confidence persona inference is allowed when material is thin, but it must stay clearly subordinate to canon."
        if allow_low_confidence
        else "When persona evidence is thin, stay conservative and do not improvise strong characterization."
    )
    if platform == "codex":
        description = (
            f"Codex primary role skill for {name}. Answer directly in {name}'s voice using canon, persona, style examples, "
            "and silent conditional memory. This wrapper can also be re-exported to OpenClaw."
        )
        platform_intro = (
            "- Primary runtime: Codex workspace skill installation.\n"
            f"- Expected path: `./.agents/skills/{slug}/`\n"
            f"- Explicit invocation is optional: `${slug}`.\n"
            "- `/skills` should discover this package from the current workspace.\n"
        )
    else:
        description = (
            f"OpenClaw-compatible role skill for {name}. Answer directly in {name}'s voice using canon, persona, style examples, "
            "and silent conditional memory."
        )
        platform_intro = (
            "- Runtime target: OpenClaw workspace skill installation.\n"
            f"- Expected path: `<openclaw_workspace>/.agents/skills/{slug}/`\n"
            "- OpenClaw should discover this package after refresh or a new session.\n"
            "- Use normal conversation after discovery; no special wrapper explanation should be shown to the user.\n"
        )
    return (
        f"---\n"
        f"name: {slug}\n"
        f"description: {description}\n"
        f"metadata: {{openclaw: {{requires: {{bins: [python3]}}}}}}\n"
        f"---\n\n"
        f"# {name}\n\n"
        f"Use this skill to roleplay or answer as {name}.\n\n"
        f"## Platform Wrapper\n\n"
        f"{platform_intro}\n"
        f"## Silent Runtime Order\n\n"
        f"1. Read `canon.md` first for facts, setting, events, and relationships.\n"
        f"2. Read `persona.md` for behavior patterns, emotional tendencies, and interaction strategy.\n"
        f"3. Read `style_examples.md` for wording texture, cadence, and short response flavor.\n"
        f"4. Only when the latest user turn suggests past context, long-term preference, nickname, or relationship state may matter, silently call `python3 runtime/memory_prepare.py --character-slug {slug} --user-message \"<latest user message>\" --data-root ../../../.dreamlover-data`.\n"
        f"5. If `memory_prepare.py` returns `should_read: true`, use the returned `memory_context`.\n"
        f"6. Reply directly in character. Do not mention memory gates, routers, scripts, or checks.\n"
        f"7. If `memory_prepare.py` returns `should_write_after_reply: true`, silently call `python3 runtime/memory_commit.py --character-slug {slug} --user-message \"<latest user message>\" --assistant-message \"<final reply>\" --data-root ../../../.dreamlover-data` after the reply.\n"
        f"8. If `memory_prepare.py` returns `should_summarize_after_reply: true`, silently call `python3 runtime/memory_summarize.py --character-slug {slug} --data-root ../../../.dreamlover-data` after the reply.\n\n"
        f"## Conditional Memory System\n\n"
        f"- Memory is opt-in per turn, not always-on.\n"
        f"- Memory data lives in `<workspace>/.dreamlover-data/memory.sqlite3`, not inside this skill package.\n"
        f"- Default behavior: no memory read and no memory write.\n"
        f"- Ordinary small talk should usually skip memory scripts entirely.\n"
        f"- If `python3` is not available, skip memory scripts and continue in no-memory mode.\n"
        f"- If no relevant memory exists, answer naturally and do not fabricate shared history.\n\n"
        f"## Rules\n\n"
        f"- Enter the character voice immediately. Do not explain internal workflow to the user.\n"
        f"- Never narrate internal checks, tools, or hidden preparation steps.\n"
        f"- If a memory lookup fails and it affects the answer, use one short natural sentence instead of exposing internal tooling.\n"
        f"- Never promote persona inference into canon during live conversation.\n"
        f"- Never say \"we talked about this before\" unless fetched memory actually supports it.\n"
        f"- If facts and style conflict, facts from `canon.md` win.\n"
        f"- If the behavior feels off, improve `persona.md` before changing canon.\n"
        f"- If the voice feels weak, improve `style_examples.md` before changing canon.\n"
        f"- {confidence_line}\n"
    )


def canonical_source_dir(root: Path, slug: str) -> Path:
    return (root / DEFAULT_ARCHIVE_ROOT) / slug


def codex_package_dir(root: Path, slug: str, output_root: str | None) -> Path:
    return resolve_root(root, output_root, DEFAULT_INSTALL_ROOT) / slug


def openclaw_package_dir(workspace: str, slug: str) -> Path:
    return Path(workspace) / ".agents" / "skills" / slug


def ensure_static_source_dir(source_dir: Path) -> None:
    source_dir.mkdir(parents=True, exist_ok=True)
    (source_dir / "sources").mkdir(parents=True, exist_ok=True)
    (source_dir / "versions").mkdir(parents=True, exist_ok=True)


def ensure_package_dir(package_dir: Path) -> None:
    package_dir.mkdir(parents=True, exist_ok=True)
    (package_dir / "sources").mkdir(parents=True, exist_ok=True)
    (package_dir / "versions").mkdir(parents=True, exist_ok=True)
    (package_dir / "runtime").mkdir(parents=True, exist_ok=True)


def copy_runtime_scripts(package_dir: Path) -> None:
    runtime_dir = package_dir / "runtime"
    runtime_dir.mkdir(parents=True, exist_ok=True)
    for filename in RUNTIME_SCRIPT_NAMES:
        source_path = repo_root() / "scripts" / filename
        (runtime_dir / filename).write_text(source_path.read_text(encoding="utf-8"), encoding="utf-8")


def write_static_source(
    source_dir: Path,
    canon_text: str,
    persona_text: str,
    style_text: str,
    meta: dict,
    normalized_payload: dict,
) -> None:
    ensure_static_source_dir(source_dir)
    (source_dir / "canon.md").write_text(canon_text, encoding="utf-8")
    (source_dir / "persona.md").write_text(persona_text, encoding="utf-8")
    (source_dir / "style_examples.md").write_text(style_text, encoding="utf-8")
    write_json(source_dir / "meta.json", meta)
    write_json(source_dir / "sources" / "normalized.json", normalized_payload)


def write_platform_package(
    package_dir: Path,
    canon_text: str,
    persona_text: str,
    style_text: str,
    skill_text: str,
    meta: dict,
    normalized_payload: dict,
) -> None:
    ensure_package_dir(package_dir)
    copy_runtime_scripts(package_dir)
    (package_dir / "canon.md").write_text(canon_text, encoding="utf-8")
    (package_dir / "persona.md").write_text(persona_text, encoding="utf-8")
    (package_dir / "style_examples.md").write_text(style_text, encoding="utf-8")
    (package_dir / "SKILL.md").write_text(skill_text, encoding="utf-8")
    write_json(package_dir / "meta.json", meta)
    write_json(package_dir / "sources" / "normalized.json", normalized_payload)


def lint_package(package_dir: Path) -> dict:
    report = lint_skill_dir(package_dir)
    if report["errors"]:
        raise ValueError(json.dumps(report, ensure_ascii=False, indent=2))
    return report


def list_packages(root: Path, scope: str) -> list[dict]:
    search_roots: list[tuple[str, Path]] = []
    if scope in {"codex", "both"}:
        search_roots.append(("codex", root / DEFAULT_INSTALL_ROOT))
    if scope in {"archive", "both"}:
        search_roots.append(("archive", root / DEFAULT_ARCHIVE_ROOT))
    indexed: dict[str, dict] = {}
    for location, search_root in search_roots:
        if not search_root.exists():
            continue
        for item in sorted(search_root.iterdir()):
            if not item.is_dir():
                continue
            meta_path = item / "meta.json"
            meta = json.loads(meta_path.read_text(encoding="utf-8")) if meta_path.exists() else {"slug": item.name}
            record = indexed.setdefault(meta.get("slug", item.name), dict(meta))
            record.setdefault("locations", [])
            record["locations"].append(location)
    return list(indexed.values())


def interactive_intake(existing: dict) -> dict:
    print("进入角色创建 intake 流程。")
    slot_state = build_slot_state(existing)
    slot_state["archive_mirror"] = existing.get(
        "archive_mirror",
        existing.get("install_scope", "both") in {"both", "archive"},
    )

    if slot_state["source_policy"] is None:
        slot_state["source_policy"] = prompt_choice(
            "请选择资料补全策略。",
            SOURCE_DECISION_POLICIES,
            "1",
            SOURCE_DECISION_LABELS,
            SOURCE_POLICY_ALIASES,
        )
    source_decision_policy = slot_state["source_policy"]

    requested_name = existing.get("requested_character_name") or existing.get("character_name") or ""
    if slot_state["character_name"] is None and requested_name:
        if prompt_yes_no(f'是否将“{requested_name}”作为角色名', True):
            slot_state["character_name"] = requested_name
        else:
            slot_state["character_name"] = prompt_required("请输入角色名")
    elif slot_state["character_name"] is None:
        slot_state["character_name"] = prompt_required("请输入角色名")
    character_name = slot_state["character_name"]

    if source_decision_policy == "official_quick":
        effective_slug = slugify(character_name)
        return {
            "slug": effective_slug,
            "character_name": character_name,
            "source_work": existing.get("source_work", ""),
            "target_use": existing.get("target_use") or "角色扮演对话",
            "source_types": infer_material_types_from_policy(source_decision_policy),
            "allow_low_confidence_persona": existing.get("allow_low_confidence_persona", False),
            "source_decision_policy": source_decision_policy,
            "input_mode": DEFAULT_INPUT_MODE,
            "search_scope": "medium",
            "source_paths": [],
            "archive_mirror": slot_state["archive_mirror"],
            "raw_material_notes": "",
            "canon_notes": "",
            "persona_notes": "",
            "style_notes": "",
            "confirmed": False,
        }

    if source_decision_policy in {"user_only", "official_plus_user"} and slot_state["input_mode"] is None:
        slot_state["input_mode"] = prompt_choice(
            "请选择你提供资料的方式。",
            INPUT_MODES,
            "1",
            INPUT_MODE_LABELS,
            INPUT_MODE_ALIASES,
        )
    input_mode = slot_state["input_mode"] or DEFAULT_INPUT_MODE

    if slot_state["source_work"] is None:
        slot_state["source_work"] = input("来源作品（如果是纯原创角色，可以留空）: ").strip()
    source_work = slot_state["source_work"]

    search_scope = existing.get("search_scope", DEFAULT_SEARCH_SCOPE)
    if source_decision_policy in {"official_wiki_only", "official_plus_user"} and source_work:
        search_scope = prompt_choice(
            "请选择公开资料补全范围。",
            SEARCH_SCOPES,
            "2",
            SEARCH_SCOPE_LABELS,
            SEARCH_SCOPE_ALIASES,
        )

    source_paths: list[str] = []
    raw_material_notes = ""
    if input_mode == "file_path":
        raw_path_block = prompt_multiline("请提供一个或多个资料文件路径。")
        source_paths, raw_material_notes = read_source_paths(raw_path_block)
    elif input_mode == "direct_text":
        raw_material_notes = prompt_multiline("请直接贴出你希望用于生成的资料文本或备注。")

    if slot_state["material_types"] is None:
        slot_state["material_types"] = infer_material_types_from_policy(source_decision_policy)

    if slot_state["allow_low_confidence_persona"] is None:
        slot_state["allow_low_confidence_persona"] = prompt_yes_no(
            "如果资料不够，允不允许我替你做一点性格补充",
            False,
        )
    allow_low_confidence = slot_state["allow_low_confidence_persona"]

    canon_notes = ""
    persona_notes = ""
    style_notes = ""
    effective_slug = slugify(character_name)
    target_use = existing.get("target_use") or "角色扮演对话"

    return {
        "slug": effective_slug,
        "character_name": character_name,
        "source_work": source_work,
        "target_use": target_use,
        "source_types": slot_state["material_types"],
        "allow_low_confidence_persona": allow_low_confidence,
        "source_decision_policy": source_decision_policy,
        "input_mode": input_mode,
        "search_scope": search_scope,
        "source_paths": source_paths,
        "archive_mirror": slot_state["archive_mirror"],
        "raw_material_notes": raw_material_notes,
        "canon_notes": canon_notes,
        "persona_notes": persona_notes,
        "style_notes": style_notes,
        "confirmed": False,
    }


def build_generated_confirmation_summary(
    intake: dict,
    canon_text: str,
    persona_text: str,
    style_text: str,
) -> list[str]:
    persona_behavior = choose_section_body(
        parse_section_segments(persona_text, PERSONA_HEADERS)["## Behavior Patterns"],
        SECTION_PLACEHOLDERS["## Behavior Patterns"],
    ).splitlines()[0].lstrip("- ").strip()
    style_line = choose_section_body(
        parse_section_segments(style_text, STYLE_HEADERS)["## Short Example Lines"],
        SECTION_PLACEHOLDERS["## Short Example Lines"],
    ).splitlines()[0].lstrip("- ").strip()
    summary_lines = [
        f"- 角色名：{intake['character_name']}",
        f"- 标识名（slug）：{intake['slug']}",
        f"- 资料补全策略：{SOURCE_DECISION_LABELS.get(intake['source_decision_policy'], intake['source_decision_policy'])}",
        f"- 输入方式：{INPUT_MODE_LABELS.get(intake['input_mode'], intake['input_mode'])}",
        f"- 来源作品：{intake['source_work'] or '原创角色 / 未提供'}",
        f"- 联网补全范围：{SEARCH_SCOPE_LABELS.get(intake.get('search_scope', DEFAULT_SEARCH_SCOPE), intake.get('search_scope', DEFAULT_SEARCH_SCOPE))}",
        f"- 允许性格补充：{'是' if intake['allow_low_confidence_persona'] else '否'}",
        f"- 人格摘要预览：{persona_behavior}",
        f"- 语言风格预览：{style_line}",
    ]
    return summary_lines


def build_interactive_outputs(
    existing: dict,
    forced_slug: str | None,
    preset_openclaw_workspace: str | None = None,
) -> tuple[str, str, str, dict, dict]:
    intake = interactive_intake(existing)
    if forced_slug:
        intake["slug"] = forced_slug

    updated_at = utc_now()
    canon_blocks = parse_prefixed_notes(intake["canon_notes"], CANON_HEADERS, CANON_PREFIXES, "## Basic Identity")
    persona_blocks = parse_prefixed_notes(
        intake["persona_notes"],
        PERSONA_HEADERS,
        PERSONA_PREFIXES,
        "## Behavior Patterns",
    )
    style_blocks = parse_prefixed_notes(
        intake["style_notes"],
        STYLE_HEADERS,
        STYLE_PREFIXES,
        "## Address Patterns",
    )
    canon_text = build_canon_markdown(intake["character_name"], intake["source_work"], canon_blocks)
    persona_text = build_persona_markdown(
        persona_blocks,
        intake["target_use"],
        intake["allow_low_confidence_persona"],
    )
    style_text = build_style_markdown(style_blocks, intake["target_use"])
    normalized_payload = build_normalized_payload(
        intake,
        intake["raw_material_notes"],
        intake["canon_notes"],
        intake["persona_notes"],
        intake["style_notes"],
        intake["source_paths"],
        updated_at,
    )
    print("写入任何文件之前，请先确认这份生成草稿摘要：")
    print("\n".join(build_generated_confirmation_summary(intake, canon_text, persona_text, style_text)))
    intake["confirmed"] = prompt_yes_no("确认这份草稿并允许开始写入角色文件吗", False)
    if not intake["confirmed"]:
        raise SystemExit(
            json.dumps(
                {
                    "status": "aborted",
                    "reason": "intake_not_confirmed",
                    "message": "硬性 intake gate 已阻止写入，当前没有创建任何角色文件。",
                },
                ensure_ascii=False,
                indent=2,
            )
        )
    if preset_openclaw_workspace:
        intake["export_openclaw"] = True
        intake["openclaw_workspace"] = preset_openclaw_workspace
    else:
        intake["export_openclaw"] = prompt_yes_no("是否额外导出一份 OpenClaw 版本", False)
        intake["openclaw_workspace"] = (
            prompt_required("请输入 OpenClaw workspace 路径") if intake["export_openclaw"] else ""
        )
    return canon_text, persona_text, style_text, normalized_payload, intake


def main() -> None:
    parser = argparse.ArgumentParser(description="Create, update, or list character skill packages.")
    parser.add_argument("--action", required=True, choices=["create", "update", "list"], help="Operation to run.")
    parser.add_argument("--slug", help="Character slug.")
    parser.add_argument("--root", default=str(repo_root()), help="Repository root.")
    parser.add_argument("--output-root", help="Override the Codex installation root. Defaults to ./.agents/skills.")
    parser.add_argument(
        "--install-scope",
        default="codex",
        type=parse_scope,
        help="Legacy compatibility flag. `codex` writes canonical source plus Codex install. `archive` writes only canonical source. `both` behaves like `codex`.",
    )
    parser.add_argument(
        "--list-scope",
        default="codex",
        type=parse_scope,
        help="Which package roots to inspect when using --action list.",
    )
    parser.add_argument("--interactive", action="store_true", help="Run an intake-first interactive session for create or update.")
    parser.add_argument("--name", help="Character display name.")
    parser.add_argument("--source-work", default="", help="Source work name.")
    parser.add_argument("--target-use", default="", help="Target roleplay use or scenario.")
    parser.add_argument("--source-types", help="Comma-separated source types: official, plot, quotes, wiki, user.")
    parser.add_argument("--allow-low-confidence-persona", help="Whether low-confidence persona inference is allowed: yes/no.")
    parser.add_argument("--canon-file", help="Optional canon markdown path.")
    parser.add_argument("--persona-file", help="Optional persona markdown path.")
    parser.add_argument("--style-file", help="Optional style markdown path.")
    parser.add_argument("--openclaw-workspace", help="Optional OpenClaw workspace to export to after generation.")
    parser.add_argument("--skip-lint", action="store_true", help="Skip post-write package linting.")
    args = parser.parse_args()

    root = Path(args.root)
    (root / DEFAULT_INSTALL_ROOT).mkdir(parents=True, exist_ok=True)
    (root / DEFAULT_ARCHIVE_ROOT).mkdir(parents=True, exist_ok=True)

    if args.action == "list":
        print(json.dumps(list_packages(root, args.list_scope), ensure_ascii=False, indent=2))
        return

    effective_slug = args.slug or (slugify(args.name) if args.name else None)
    if not effective_slug and not args.interactive:
        raise SystemExit("--slug is required for create and update unless --interactive is used")

    placeholder_slug = effective_slug or "interactive-intake"
    canonical_dir = canonical_source_dir(root, placeholder_slug)
    codex_dir = codex_package_dir(root, placeholder_slug, args.output_root)
    meta_candidates = [canonical_dir / "meta.json", codex_dir / "meta.json"]
    existing = load_existing_meta(meta_candidates)
    if args.name:
        existing.setdefault("requested_character_name", args.name)
    elif args.slug:
        existing.setdefault("requested_character_name", args.slug)

    if args.interactive:
        canon_text, persona_text, style_text, normalized_payload, intake = build_interactive_outputs(
            existing,
            args.slug,
            args.openclaw_workspace,
        )
        name = intake["character_name"]
        effective_slug = intake["slug"]
        source_work = intake["source_work"]
        target_use = intake["target_use"]
        source_types = intake["source_types"]
        allow_low_confidence = intake["allow_low_confidence_persona"]
        openclaw_workspace = intake.get("openclaw_workspace", "")
    else:
        canon_existing = load_existing_text([canonical_dir / "canon.md", codex_dir / "canon.md"])
        persona_existing = load_existing_text([canonical_dir / "persona.md", codex_dir / "persona.md"])
        style_existing = load_existing_text([canonical_dir / "style_examples.md", codex_dir / "style_examples.md"])
        canon_text = ensure_sections(read_text(args.canon_file) or canon_existing, CANON_HEADERS)
        persona_text = ensure_sections(read_text(args.persona_file) or persona_existing, PERSONA_HEADERS)
        style_text = ensure_sections(read_text(args.style_file) or style_existing, STYLE_HEADERS)
        name = args.name or existing.get("character_name") or effective_slug or "character"
        source_work = args.source_work or existing.get("source_work", "")
        target_use = args.target_use or existing.get("target_use", "角色扮演对话")
        source_types = normalize_source_types(args.source_types or ",".join(existing.get("source_types", DEFAULT_SOURCE_TYPES)))
        allow_low_confidence = parse_bool_flag(
            args.allow_low_confidence_persona,
            existing.get("allow_low_confidence_persona", False),
        )
        source_decision_policy = existing.get("source_decision_policy", DEFAULT_SOURCE_DECISION_POLICY)
        input_mode = existing.get("input_mode", DEFAULT_INPUT_MODE)
        normalized_payload = {
            "schema_version": "0.4",
            "source": {
                "source_type": "manual",
                "input_path": "",
                "normalized_at": utc_now(),
                "source_types": source_types,
                "source_decision_policy": source_decision_policy,
                "input_mode": input_mode,
                "search_scope": existing.get("search_scope", DEFAULT_SEARCH_SCOPE),
                "archive_mirror": existing.get("archive_mirror", True),
                "source_paths": existing.get("source_paths", []),
            },
            "intake": {
                "slug": effective_slug,
                "character_name": name,
                "source_work": source_work,
                "target_use": target_use,
                "source_types": source_types,
                "allow_low_confidence_persona": allow_low_confidence,
                "source_decision_policy": source_decision_policy,
                "input_mode": input_mode,
                "search_scope": existing.get("search_scope", DEFAULT_SEARCH_SCOPE),
                "archive_mirror": existing.get("archive_mirror", True),
                "source_paths": existing.get("source_paths", []),
                "confirmed": True,
            },
            "entries": [],
        }
        openclaw_workspace = args.openclaw_workspace or ""

    validate_cross_headers(canon_text, PERSONA_HEADERS + STYLE_HEADERS, "canon")
    validate_cross_headers(persona_text, CANON_HEADERS + STYLE_HEADERS, "persona")
    validate_cross_headers(style_text, CANON_HEADERS + PERSONA_HEADERS, "style_examples")

    created_at = existing.get("created_at", utc_now())
    updated_at = utc_now()
    canonical_dir = canonical_source_dir(root, effective_slug or placeholder_slug)
    codex_dir = codex_package_dir(root, effective_slug or placeholder_slug, args.output_root)
    openclaw_dir = openclaw_package_dir(openclaw_workspace, effective_slug) if openclaw_workspace else None
    write_codex_install = args.install_scope != "archive"
    generated_for = ["codex"] if write_codex_install else []
    if openclaw_dir is not None:
        generated_for.append("openclaw")
    canonical_source = relative_path(root, canonical_dir) or str(canonical_dir)
    export_targets: dict[str, str] = {}
    if write_codex_install:
        export_targets["codex"] = relative_path(root, codex_dir) or str(codex_dir)
    if openclaw_dir is not None:
        export_targets["openclaw"] = str(openclaw_dir)
    meta = {
        "slug": effective_slug,
        "character_name": name,
        "source_work": source_work,
        "target_use": target_use,
        "source_types": source_types,
        "allow_low_confidence_persona": allow_low_confidence,
        "source_decision_policy": normalized_payload["intake"]["source_decision_policy"],
        "input_mode": normalized_payload["intake"]["input_mode"],
        "search_scope": normalized_payload["intake"].get("search_scope", DEFAULT_SEARCH_SCOPE),
        "archive_mirror": normalized_payload["intake"].get("archive_mirror", True),
        "source_paths": normalized_payload["intake"].get("source_paths", []),
        "layout_version": "0.7",
        "created_at": created_at,
        "updated_at": updated_at,
        "primary_path": relative_path(root, codex_dir) if write_codex_install else None,
        "archive_path": canonical_source,
        "install_scope": args.install_scope,
        "canonical_source": canonical_source,
        "export_targets": export_targets,
        "generated_for": generated_for,
        "openclaw_exported_at": updated_at if openclaw_dir is not None else None,
    }
    normalized_payload["source"]["normalized_at"] = updated_at
    normalized_payload["intake"]["slug"] = effective_slug
    normalized_payload["intake"]["character_name"] = name
    normalized_payload["exports"] = export_targets
    normalized_payload["canonical_source"] = canonical_source

    write_static_source(canonical_dir, canon_text, persona_text, style_text, meta, normalized_payload)
    if write_codex_install:
        write_platform_package(
            codex_dir,
            canon_text,
            persona_text,
            style_text,
            build_child_skill("codex", name, effective_slug or "character", target_use, allow_low_confidence),
            meta,
            normalized_payload,
        )
    if openclaw_dir is not None:
        write_platform_package(
            openclaw_dir,
            canon_text,
            persona_text,
            style_text,
            build_child_skill("openclaw", name, effective_slug or "character", target_use, allow_low_confidence),
            meta,
            normalized_payload,
        )

    lint_results: dict[str, dict] = {}
    if not args.skip_lint:
        if write_codex_install:
            lint_results["codex"] = lint_package(codex_dir)
        if openclaw_dir is not None:
            lint_results["openclaw"] = lint_package(openclaw_dir)

    print(
        json.dumps(
            {
                "canonical_source": canonical_source,
                "codex_install": export_targets.get("codex"),
                "openclaw_export": export_targets.get("openclaw"),
                "package": meta,
                "lint": lint_results,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()







