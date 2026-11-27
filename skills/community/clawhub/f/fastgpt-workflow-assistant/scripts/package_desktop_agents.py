#!/usr/bin/env python3
"""生成 Trae、WorkBuddy、Hermes 和通用 Agent Skills 客户端包。"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import posixpath
import zipfile
from pathlib import Path

from package_skill import load_version, should_include


MACHINE_NAME = "fastgpt-workflow-assistant"
TRAE_PREFIX = ""
WORKBUDDY_PREFIX = ""
AGENT_SKILLS_PREFIX = f"{MACHINE_NAME}/"
HERMES_PREFIX = f"{MACHINE_NAME}/"
WORKBUDDY_REQUIRED = (
    "name", "version", "display_name", "display_name_en", "description",
    "description_zh", "description_en", "author",
)


def validate_workbuddy_frontmatter(text: str, expected_version: str) -> None:
    """Validate the generated flat metadata, not a substring anywhere in the body."""
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, flags=re.DOTALL)
    if not match:
        raise ValueError("WorkBuddy SKILL.md 缺少 YAML frontmatter")
    fields: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if not line or line.startswith((" ", "#")) or ":" not in line:
            continue
        key, raw = line.split(":", 1)
        if key in fields:
            raise ValueError(f"WorkBuddy frontmatter 重复字段：{key}")
        value = raw.strip()
        if value.startswith('"'):
            value = json.loads(value)
        elif value.startswith("'") and value.endswith("'"):
            value = value[1:-1]
        fields[key] = value
    for key in WORKBUDDY_REQUIRED:
        if not isinstance(fields.get(key), str) or not fields[key].strip():
            raise ValueError(f"WorkBuddy frontmatter 缺少非空字段：{key}")
    if fields["name"] != MACHINE_NAME or fields["version"] != expected_version:
        raise ValueError("WorkBuddy 名称或版本与源清单不一致")
    if not re.fullmatch(r"\d+\.\d+\.\d+", fields["version"]):
        raise ValueError("WorkBuddy version 必须是语义化版本号")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skill_directory", type=Path)
    parser.add_argument("output_directory", type=Path)
    parser.add_argument("--force", action="store_true")
    return parser.parse_args()


def yaml_quote(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def extract_description(skill_text: str) -> str:
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n", skill_text, flags=re.DOTALL)
    if not match:
        raise ValueError("SKILL.md 缺少有效 YAML frontmatter")
    for line in match.group(1).splitlines():
        if line.startswith("description:"):
            return line.split(":", 1)[1].strip().strip('"').strip("'")
    raise ValueError("SKILL.md frontmatter 缺少 description")


def workbuddy_skill_text(skill_text: str, version: str, display_name: str) -> str:
    match = re.match(r"^---\s*\n.*?\n---\s*\n(.*)$", skill_text, flags=re.DOTALL)
    if not match:
        raise ValueError("SKILL.md 缺少有效 YAML frontmatter")
    body = match.group(1)
    description = extract_description(skill_text)
    description_zh = "构建、修改、调试、测试和发布 FastGPT 工作流，支持文件输入、多文件审核和回导验证。"
    description_en = "Build, modify, debug, test, and package FastGPT workflows with file-input and round-trip validation."
    frontmatter = [
        "---",
        f"name: {MACHINE_NAME}",
        f"display_name: {yaml_quote(display_name)}",
        f"display_name_en: {yaml_quote('FastGPT Workflow Assistant')}",
        f"description: {yaml_quote(description)}",
        f"description_zh: {yaml_quote(description_zh)}",
        f"description_en: {yaml_quote(description_en)}",
        f"version: {version}",
        f"author: {yaml_quote('EnderZhou')}",
        "examples_zh:",
        '  - "根据需求生成 FastGPT 工作流并离线校验"',
        '  - "检查这份工作流 JSON 的变量引用和连线"',
        "examples_en:",
        '  - "Generate and validate a FastGPT workflow from requirements"',
        '  - "Check variable references and connections in this workflow JSON"',
        "---",
        "",
    ]
    result = "\n".join(frontmatter) + body
    validate_workbuddy_frontmatter(result, version)
    return result


def archive_files(root: Path) -> list[Path]:
    return sorted(
        path for path in root.rglob("*")
        if path.is_file() and should_include(path, root, "slim-production")
    )


def validate_workbuddy_paths(names: list[str]) -> None:
    """The marketplace accepts only root files and directory/file entries."""
    if len(names) != len(set(names)):
        raise ValueError("WorkBuddy ZIP 存在重名文件")
    for name in names:
        parts = name.split("/")
        if len(parts) > 2 or any(p in {"", ".", ".."} for p in parts) or "\\" in name or ":" in name:
            raise ValueError(f"WorkBuddy ZIP 目录层级或路径不合法：{name}")
    if "SKILL.md" not in names:
        raise ValueError("WorkBuddy ZIP 根目录缺少 SKILL.md")


def validate_workbuddy_resources(archive: zipfile.ZipFile) -> None:
    """Validate local Markdown links against the resources actually shipped."""
    names = set(archive.namelist())
    for name in sorted(names):
        if not name.endswith(".md"):
            continue
        text = archive.read(name).decode("utf-8-sig")
        for link in re.findall(r"\]\(([^)]+)\)", text):
            target = link.split("#", 1)[0].strip("<>")
            if not target or re.match(r"[a-zA-Z]+:", target):
                continue
            resolved = posixpath.normpath(posixpath.join(posixpath.dirname(name), target))
            if resolved not in names:
                raise ValueError(f"WorkBuddy包缺少引用资源：{name} -> {target}")


def build_workbuddy_archive(root: Path, output: Path, skill_text: str, force: bool) -> dict[str, object]:
    if output.exists() and not force:
        raise FileExistsError(output)
    files = archive_files(root)
    mapping = {}
    for file in files:
        old = file.relative_to(root).as_posix()
        parts = old.split("/")
        mapping[old] = old if len(parts) <= 2 else parts[0] + "/" + "__".join(parts[1:])
    validate_workbuddy_paths(list(mapping.values()))
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for file in files:
            old = file.relative_to(root).as_posix()
            new = mapping[old]
            text = skill_text if old == "SKILL.md" else file.read_text(encoding="utf-8-sig")
            # Rewrite root-relative documentation and file-relative catalog references.
            replacements = {}
            for source, target in mapping.items():
                if source == target:
                    continue
                replacements[source] = target
                relative_old = posixpath.relpath(source, posixpath.dirname(old) or ".")
                relative_new = posixpath.relpath(target, posixpath.dirname(new) or ".")
                replacements[relative_old] = relative_new
            if replacements:
                pattern = re.compile("|".join(re.escape(k) for k in sorted(replacements, key=len, reverse=True)))
                text = pattern.sub(lambda m: replacements[m.group(0)], text)
            archive.writestr(new, text.encode("utf-8"))
    with zipfile.ZipFile(output) as archive:
        validate_workbuddy_paths(archive.namelist())
        validate_workbuddy_resources(archive)
        if archive.testzip() is not None:
            raise ValueError("WorkBuddy ZIP CRC校验失败")
    return {"file": output.name, "sha256": hashlib.sha256(output.read_bytes()).hexdigest().upper(),
            "size": output.stat().st_size, "files": len(files), "skill_entry": "SKILL.md", "max_path_parts": 2}


def build_archive(
    root: Path,
    output: Path,
    prefix: str,
    skill_override: str | None,
    force: bool,
) -> dict[str, object]:
    if output.exists() and not force:
        raise FileExistsError(f"拒绝覆盖已存在包：{output}")
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists():
        output.unlink()
    files = archive_files(root)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in files:
            relative = path.relative_to(root).as_posix()
            arcname = f"{prefix}{relative}"
            if relative == "SKILL.md" and skill_override is not None:
                archive.writestr(arcname, skill_override.encode("utf-8"))
            else:
                archive.write(path, arcname)
    with zipfile.ZipFile(output, "r") as archive:
        names = archive.namelist()
        expected_skill = f"{prefix}SKILL.md"
        if expected_skill not in names:
            raise RuntimeError(f"缺少入口：{expected_skill}")
        if archive.testzip() is not None:
            raise RuntimeError(f"ZIP CRC 校验失败：{output}")
        forbidden = {
            f"{prefix}scripts/package_skill.py",
            f"{prefix}scripts/package_desktop_agents.py",
            f"{prefix}scripts/test_skill.py",
            f"{prefix}references/同类技能工程参考.md",
        }
        if forbidden.intersection(names) or any(name.startswith(f"{prefix}scripts/tests/") for name in names):
            raise RuntimeError(f"研发文件泄漏到生产包：{output}")
    digest = hashlib.sha256(output.read_bytes()).hexdigest().upper()
    return {
        "file": output.name,
        "sha256": digest,
        "size": output.stat().st_size,
        "files": len(files),
        "skill_entry": f"{prefix}SKILL.md",
    }


def main() -> int:
    args = parse_args()
    try:
        root = args.skill_directory.resolve()
        if not root.is_dir():
            raise NotADirectoryError(root)
        version = load_version(root)
        version_manifest = json.loads((root / "assets" / "skill-version.json").read_text(encoding="utf-8-sig"))
        display_name = str(version_manifest.get("display_name") or "FastGPT工作流生成助手")
        skill_text = (root / "SKILL.md").read_text(encoding="utf-8-sig")
        workbuddy_text = workbuddy_skill_text(skill_text, version, display_name)
        # Validate before any archives are created and recheck the actual ZIP entry below.
        output_dir = args.output_directory.resolve()
        packages = {
            "trae": build_archive(
                root,
                output_dir / f"fastgpt-workflow-assistant-v{version}_Trae_import-ready.zip",
                TRAE_PREFIX,
                None,
                args.force,
            ),
            "workbuddy": build_workbuddy_archive(
                root,
                output_dir / f"fastgpt-workflow-assistant-v{version}_WorkBuddy_import-ready.zip",
                workbuddy_text,
                args.force,
            ),
            "agent_skills": build_archive(
                root,
                output_dir / f"fastgpt-workflow-assistant-v{version}_AgentSkills_folder.zip",
                AGENT_SKILLS_PREFIX,
                None,
                args.force,
            ),
            "hermes": build_archive(
                root,
                output_dir / f"fastgpt-workflow-assistant-v{version}_Hermes_folder.zip",
                HERMES_PREFIX,
                None,
                args.force,
            ),
        }
        with zipfile.ZipFile(output_dir / str(packages["workbuddy"]["file"])) as archive:
            validate_workbuddy_frontmatter(
                archive.read(f"{WORKBUDDY_PREFIX}SKILL.md").decode("utf-8"), version,
            )
        manifest = {
            "skill_name": MACHINE_NAME,
            "version": version,
            "generated_for": ["Trae", "WorkBuddy", "Hermes Agent", "Agent Skills compatible clients"],
            "validation_status": "candidate packages; target-client import pending",
            "packages": packages,
        }
        manifest_path = output_dir / f"fastgpt-workflow-assistant-v{version}_desktop-packages.json"
        if manifest_path.exists() and not args.force:
            raise FileExistsError(f"拒绝覆盖已存在清单：{manifest_path}")
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
        print(json.dumps({"status": "ok", "manifest": str(manifest_path), **manifest}, ensure_ascii=False, indent=2))
        return 0
    except Exception as exc:
        print(json.dumps({"status": "error", "error": f"{type(exc).__name__}: {exc}"}, ensure_ascii=False))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
