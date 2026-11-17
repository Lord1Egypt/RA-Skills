#!/usr/bin/env python3
"""Turn a conversation transcript into a snapshot and skill-pack skeleton."""

import argparse
import datetime
import json
import os
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = ROOT / "templates"

ROLE_RE = re.compile(r"^\s*(?:#{1,3}\s+)?(用户|User|助手|Assistant|AI|Human|You)\s*[：:]\s*(.*)$", re.IGNORECASE)
HEADING_ROLE_RE = re.compile(r"^\s*(?:#{1,3}\s+)?(用户|User|助手|Assistant|AI|Human|You)\s*$", re.IGNORECASE)
SCOPE_RE = re.compile(r"^\s*conversation_scope\s*[:：]\s*(whole-dialog|topic)\s*$", re.IGNORECASE)

KEYWORDS = (
    "结论",
    "决策",
    "决定",
    "待办",
    "注意",
    "边界",
    "不要",
    "应该",
    "建议",
    "总结",
    "下一步",
    "方案",
    "原因",
    "问题",
    "重要",
    "Decision",
    "TODO",
    "Summary",
    "Important",
    "Action",
)


def slugify(text):
    slug = re.sub(r"[^\w\u4e00-\u9fff-]+", "-", text).strip("-")
    return slug or "topic"


def transcript_scope(text):
    for line in text.splitlines()[:30]:
        match = SCOPE_RE.match(line)
        if match:
            return match.group(1).lower()
    return ""


def read_template(name):
    path = TEMPLATES / name
    if path.exists():
        return path.read_text(encoding="utf-8")
    return ""


def parse_messages(text):
    messages = []
    current = None
    for line in text.splitlines():
        match = ROLE_RE.match(line) or HEADING_ROLE_RE.match(line)
        if match:
            role = match.group(1).lower()
            body = match.group(2).strip() if match.lastindex and match.lastindex >= 2 else ""
            current = {"role": role, "text": body}
            messages.append(current)
        elif current and line.strip():
            current["text"] += "\n" + line.strip()
    return messages


def extract_candidates(text):
    candidates = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if any(keyword in stripped for keyword in KEYWORDS):
            candidates.append(stripped[:160])
        if len(candidates) >= 80:
            break
    return candidates


def detect_topics(text, config_topics=None):
    if config_topics:
        return [
            item if isinstance(item, dict) else {"name": str(item)}
            for item in config_topics
        ]
    topics = []
    for line in text.splitlines():
        if line.startswith("#"):
            heading = line.lstrip("#").strip()
            if heading and len(heading) <= 24 and heading.lower() not in {
                "用户",
                "user",
                "助手",
                "assistant",
                "ai",
                "对话快照",
                "conversation snapshot",
            }:
                topics.append({"name": heading})
    if not topics:
        topics = [{"name": "通用对话"}]
    return topics[:10]


def render_template(name, replacements):
    content = read_template(name)
    for key, value in replacements.items():
        content = content.replace("{{" + key + "}}", value)
    return content


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--transcript", required=True)
    parser.add_argument("--output-dir", default="conversation-output")
    parser.add_argument("--skill-name", default="")
    parser.add_argument("--config", default="")
    parser.add_argument("--scope", choices=["whole-dialog", "topic"], default="whole-dialog")
    args = parser.parse_args()

    transcript = Path(args.transcript)
    if not transcript.exists():
        raise SystemExit("TRANSCRIPT_NOT_FOUND")

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    config = {}
    if args.config:
        config = json.loads(Path(args.config).read_text(encoding="utf-8"))

    skill_name = args.skill_name or config.get("skill_name") or transcript.stem
    text = transcript.read_text(encoding="utf-8", errors="ignore")
    declared_scope = transcript_scope(text)
    if not declared_scope:
        raise SystemExit("TRANSCRIPT_SCOPE_MISSING: add `conversation_scope: whole-dialog` or `conversation_scope: topic` near the top of the transcript")
    if declared_scope != args.scope:
        raise SystemExit(f"TRANSCRIPT_SCOPE_MISMATCH: transcript declares `{declared_scope}`, command requires `{args.scope}`")

    messages = parse_messages(text)
    last_answer = next(
        (
            message["text"]
            for message in reversed(messages)
            if message["role"].lower() in {"assistant", "ai", "助手"}
        ),
        "",
    )
    candidates = extract_candidates(text)
    topics = detect_topics(text, config.get("topics"))

    snapshot_replacements = {
        "SKILL_NAME": skill_name,
        "SOURCE_NAME": transcript.name,
        "GENERATED_AT": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        "TURNS": str(len(messages)),
        "CHARS": str(len(text)),
        "SCOPE": "整个当前对话框" if args.scope == "whole-dialog" else "指定主题",
        "TOPICS": "、".join(item["name"] if isinstance(item, dict) else str(item) for item in topics),
        "LAST_ANSWER": last_answer or "- 无",
        "CANDIDATES": "\n".join(f"- [自动候选，需复核] {candidate}" for candidate in candidates) or "- 无",
    }
    snapshot = output_dir / "conversation-snapshot.md"
    snapshot.write_text(
        render_template("conversation_snapshot_template.md", snapshot_replacements),
        encoding="utf-8",
    )

    created_skills = []
    for topic_item in topics:
        topic = topic_item["name"] if isinstance(topic_item, dict) else str(topic_item)
        slug = slugify(topic)
        if isinstance(topic_item, dict) and topic_item.get("output"):
            target = Path(topic_item["output"])
            if not target.is_absolute():
                target = output_dir / target
        else:
            target = output_dir / "skills" / slug / "SKILL.md"
        target.parent.mkdir(parents=True, exist_ok=True)
        skill_replacements = {
            "SKILL_NAME": skill_name,
            "SLUG": slug,
            "TOPIC": topic,
        }
        target.write_text(
            render_template("conversation_skill_template.md", skill_replacements),
            encoding="utf-8",
        )
        created_skills.append(str(target))

    index_lines = [
        "# Conversation Routing Index",
        "",
        f"- 对话主题：{snapshot_replacements['TOPICS']}",
        f"- 快照：`conversation-snapshot.md`",
        "",
        "## 技能包",
        "",
    ]
    for path in created_skills:
        index_lines.append(f"- `{os.path.relpath(path, output_dir)}`")
    index = output_dir / "routing-index.md"
    index.write_text("\n".join(index_lines) + "\n", encoding="utf-8")

    print(f"turns={len(messages)}")
    print(f"last_answer_chars={len(last_answer)}")
    print(f"scope={args.scope}")
    print(f"topics={len(topics)}")
    print(f"snapshot={snapshot}")
    print(f"skills={len(created_skills)}")
    print(f"index={index}")
    print("CONVERSATION_ARCHITECT_OK")


if __name__ == "__main__":
    main()
