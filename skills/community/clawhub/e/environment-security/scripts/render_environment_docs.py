#!/usr/bin/env python3
"""Render environment policy documents from a baseline JSON."""

from __future__ import annotations

import argparse
import json
import locale
import os
from datetime import datetime
from pathlib import Path
from typing import Any

DEFAULT_TOOL_ORDER = [
    "git",
    "java",
    "javac",
    "maven",
    "gradle",
    "node",
    "npm",
    "pnpm",
    "yarn",
    "python",
    "go",
    "rustc",
    "cargo",
    "rustup",
    "clang",
    "clangxx",
    "gcc",
    "gxx",
    "cmake",
    "make",
    "ninja",
    "ruby",
    "gem",
    "bundler",
    "php",
    "composer",
    "dotnet",
    "docker",
    "kubectl",
]


def load_json(path: str) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def render_date(iso_value: str | None) -> str:
    if not iso_value:
        return datetime.now().strftime("%Y-%m-%d")
    normalized = iso_value.replace("Z", "+00:00")
    return datetime.fromisoformat(normalized).strftime("%Y-%m-%d")


def code(value: str | None) -> str:
    return f"`{value}`" if value else "`<unknown>`"


def first_nonempty(*values: str | None) -> str | None:
    for value in values:
        if value:
            return value
    return None


def approved_version(tool: dict[str, Any]) -> str | None:
    if tool.get("version"):
        return tool["version"]
    if tool.get("version_probe_status") == "ok":
        return tool.get("version_text")
    return None


def normalize_lang(value: str | None) -> str | None:
    if not value:
        return None
    normalized = value.strip().lower().replace("_", "-")
    if normalized.startswith("zh") or "chinese" in normalized:
        return "zh"
    if normalized.startswith("en") or "english" in normalized:
        return "en"
    return None


def detect_locale_candidates() -> list[str]:
    candidates: list[str] = []
    for key in ["CODEX_DOC_LANG", "LC_ALL", "LC_MESSAGES", "LANGUAGE", "LANG"]:
        value = os.environ.get(key)
        if value:
            candidates.append(value)

    try:
        current_locale = locale.getlocale()[0]
        if current_locale:
            candidates.append(current_locale)
    except Exception:
        pass

    return list(dict.fromkeys([item for item in candidates if item]))


def choose_document_language(data: dict[str, Any], explicit_lang: str | None) -> str:
    normalized_explicit = normalize_lang(explicit_lang)
    if explicit_lang and explicit_lang != "auto" and normalized_explicit:
        return normalized_explicit

    context_language = normalize_lang(data.get("context", {}).get("document_language"))
    if context_language:
        return context_language

    context_locale = normalize_lang(data.get("context", {}).get("detected_locale"))
    if context_locale:
        return context_locale

    for candidate in detect_locale_candidates():
        normalized = normalize_lang(candidate)
        if normalized:
            return normalized

    return "en"


def L(lang: str, en: str, zh: str) -> str:
    return zh if lang == "zh" else en


def dash(label: str, value: str | None, lang: str) -> str:
    return f"- {label}：{code(value)}" if lang == "zh" else f"- {label}: {code(value)}"


def detect_os_family(data: dict[str, Any]) -> str:
    context = data.get("context", {})
    family = context.get("os_family")
    if family:
        return family
    platform_system = str(context.get("platform_system", "")).lower()
    if platform_system == "windows":
        return "windows"
    if platform_system == "darwin":
        return "macos"
    if platform_system == "linux":
        return "linux"
    platform_text = str(context.get("platform", "")).lower()
    if "windows" in platform_text:
        return "windows"
    if "darwin" in platform_text or "mac" in platform_text:
        return "macos"
    if "linux" in platform_text:
        return "linux"
    return "unknown"


def os_label(os_family: str) -> str:
    return {
        "windows": "Windows",
        "macos": "macOS",
        "linux": "Linux",
    }.get(os_family, os_family or "Unknown")


def env_ref(name: str, suffix: str | None, os_family: str) -> str:
    if os_family == "windows":
        return f"%{name}%\\{suffix}" if suffix else f"%{name}%"
    if suffix:
        return f"${name}/{suffix}"
    return f"${name}"


def compare_paths(left: str | None, right: str | None) -> bool:
    if not left or not right:
        return False
    return os.path.normcase(os.path.normpath(left)) == os.path.normcase(os.path.normpath(right))


def ordered_tools(data: dict[str, Any]) -> list[tuple[str, dict[str, Any]]]:
    tools = data.get("tools", {})
    seen: set[str] = set()
    ordered: list[tuple[str, dict[str, Any]]] = []
    for tool_id in DEFAULT_TOOL_ORDER:
        if tool_id in tools:
            ordered.append((tool_id, tools[tool_id]))
            seen.add(tool_id)
    for tool_id in sorted(tools.keys()):
        if tool_id not in seen:
            ordered.append((tool_id, tools[tool_id]))
    return ordered


def format_path_entry(entry: str, env_vars: dict[str, dict[str, Any]], os_family: str) -> str:
    java_home = env_vars.get("JAVA_HOME", {}).get("value")
    maven_home = env_vars.get("MAVEN_HOME", {}).get("value")
    if java_home and compare_paths(entry, os.path.join(java_home, "bin")):
        return env_ref("JAVA_HOME", "bin", os_family)
    if maven_home and compare_paths(entry, os.path.join(maven_home, "bin")):
        return env_ref("MAVEN_HOME", "bin", os_family)
    return entry


def launcher_label(command_name: str, os_family: str, lang: str) -> str:
    if os_family == "windows" and command_name in {"python", "py"}:
        return L(lang, f"`{command_name}` shim", f"`{command_name}` shim")
    return L(lang, f"`{command_name}` PATH entry", f"`{command_name}` PATH 入口")


def render_tool_section(
    tool_id: str,
    tool: dict[str, Any],
    section_number: int,
    env_vars: dict[str, dict[str, Any]],
    os_family: str,
    lang: str,
) -> list[str]:
    lines = [f"### 3.{section_number} {tool.get('label', tool_id)}", ""]
    selected = first_nonempty(tool.get("selected_executable"), tool.get("preferred_path"), tool.get("resolved_path"))
    version = approved_version(tool)
    path_hit = tool.get("resolved_path")

    if tool_id == "java":
        java_home = env_vars.get("JAVA_HOME", {}).get("value")
        if java_home:
            lines.append(dash(L(lang, "Default JDK", "默认 JDK"), java_home, lang))
            lines.append(dash("JAVA_HOME", java_home, lang))
        else:
            lines.append(dash(L(lang, "Approved Java executable", "批准的 Java 可执行文件"), selected, lang))
        lines.append(dash(L(lang, "Approved Java version", "当前批准使用的 Java 版本"), version, lang))
        lines.append("")
        lines.append(L(lang, "Notes:", "说明："))
        if path_hit and selected and not compare_paths(path_hit, selected):
            lines.append(
                L(
                    lang,
                    f"- `java` currently resolves to {code(path_hit)} on PATH.",
                    f"- `java` 当前 PATH 先命中了 {code(path_hit)}。",
                )
            )
        note = L(
            lang,
            "- Prefer the approved Java path before running Java-related commands",
            "- 执行 Java 相关命令前，如有需要，应优先使用批准路径",
        )
        if java_home:
            note += L(
                lang,
                f" or move {code(env_ref('JAVA_HOME', 'bin', os_family))} to the front of PATH for the current process.",
                f"或在当前进程里把 {code(env_ref('JAVA_HOME', 'bin', os_family))} 放到 PATH 最前面。",
            )
        else:
            note += L(lang, ".", "。")
        lines.append(note)
        if not version and tool.get("version_probe_status") != "ok":
            lines.append(
                L(
                    lang,
                    "- The Java launcher was found, but it did not report a usable runtime version. Treat Java as unavailable until a JDK or JRE is installed and `java -version` succeeds.",
                    "- 已找到 Java 启动入口，但它没有返回可用的运行时版本。在安装好 JDK 或 JRE 且 `java -version` 成功之前，应把 Java 视为不可用。",
                )
            )
        return lines

    if tool_id == "maven":
        maven_home = env_vars.get("MAVEN_HOME", {}).get("value")
        if maven_home:
            lines.append(dash("MAVEN_HOME", maven_home, lang))
        lines.append(dash(L(lang, "Executable", "可执行文件"), selected, lang))
        lines.append(dash(L(lang, "Approved Maven version", "当前批准使用的 Maven 版本"), version, lang))
        if path_hit and selected and not compare_paths(path_hit, selected):
            lines.append("")
            lines.append(L(lang, "Notes:", "说明："))
            lines.append(
                L(
                    lang,
                    f"- `mvn` currently resolves to {code(path_hit)} on PATH.",
                    f"- `mvn` 当前 PATH 先命中了 {code(path_hit)}。",
                )
            )
            note = L(
                lang,
                "- Prefer the approved Maven path before running Maven-related commands",
                "- 执行 Maven 相关命令前，如有需要，应优先使用批准路径",
            )
            if maven_home:
                note += L(
                    lang,
                    f" or move {code(env_ref('MAVEN_HOME', 'bin', os_family))} to the front of PATH for the current process.",
                    f"或在当前进程里把 {code(env_ref('MAVEN_HOME', 'bin', os_family))} 放到 PATH 最前面。",
                )
            else:
                note += L(lang, ".", "。")
            lines.append(note)
        return lines

    if tool_id == "python":
        details = tool.get("details", {})
        lines.append(dash(L(lang, "Approved Python version", "当前版本"), version, lang))
        lines.append(dash(L(lang, "Real interpreter path", "真实解释器路径"), details.get("current_interpreter"), lang))
        lines.append(
            dash(
                L(lang, "Python script directory", "Python 脚本入口目录"),
                details.get("bin_dir") or details.get("scripts_dir"),
                lang,
            )
        )
        for command_name in ["python", "python3", "py"]:
            launcher_value = details.get(f"{command_name}_launcher")
            if launcher_value:
                lines.append(dash(launcher_label(command_name, os_family, lang), launcher_value, lang))
        lines.append("")
        lines.append(L(lang, "Notes:", "说明："))
        lines.append(L(lang, "- Prefer the real interpreter path when an absolute path is required.", "- 需要绝对路径时，优先使用真实解释器路径。"))
        if path_hit and selected and not compare_paths(path_hit, selected):
            lines.append(
                L(
                    lang,
                    "- `python` or `python3` may currently resolve to a shim, wrapper, alias, symlink, or launcher instead of the real install root.",
                    "- `python` 或 `python3` 当前可能命中了 shim、wrapper、alias、symlink 或 launcher，不应将其误认为真实安装根目录。",
                )
            )
        return lines

    if tool_id == "node":
        lines.append(dash("Node", selected, lang))
        lines.append(dash(L(lang, "Approved Node version", "Node 当前版本"), version, lang))
        if path_hit and selected and not compare_paths(path_hit, selected):
            lines.append(dash(L(lang, "Current PATH hit", "当前 PATH 命中"), path_hit, lang))
        return lines

    if tool_id == "npm":
        lines.append(dash("npm", selected, lang))
        lines.append(dash(L(lang, "Approved npm version", "npm 当前版本"), version, lang))
        if path_hit and selected and not compare_paths(path_hit, selected):
            lines.append(dash(L(lang, "Current PATH hit", "当前 PATH 命中"), path_hit, lang))
        return lines

    lines.append(dash(L(lang, "Executable", "可执行文件"), selected, lang))
    if version:
        lines.append(dash(L(lang, "Version", "当前版本"), version, lang))
    if path_hit and selected and not compare_paths(path_hit, selected):
        lines.append(dash(L(lang, "Current PATH hit", "当前 PATH 命中"), path_hit, lang))
    if not version and tool.get("version_command") and tool.get("version_probe_status") != "ok":
        lines.append(
            L(
                lang,
                "- Note: The executable was found, but its version command did not return a usable version. Treat this tool as present but not yet verified for real use.",
                "- 说明：已找到可执行入口，但版本命令没有返回可用版本。在版本命令成功之前，应将该工具视为“已命中入口但尚未真正验证可用”。",
            )
        )
    for note in tool.get("notes", []):
        lines.append(L(lang, f"- Note: {note}", f"- 说明：{note}"))
    return lines


def render_missing_tools(data: dict[str, Any], start_section: int, lang: str) -> list[str]:
    missing = [
        (tool_id, tool)
        for tool_id, tool in ordered_tools(data)
        if tool.get("status") != "found"
    ]
    if not missing:
        return []

    lines = [f"### 3.{start_section} {L(lang, 'Verified but currently missing tools', '未找到但曾被校验的工具')}", ""]
    for tool_id, tool in missing:
        lines.append(L(lang, f"- {tool.get('label', tool_id)}: executable not found.", f"- {tool.get('label', tool_id)}：未找到可执行文件。"))
    return lines


def render_checks(data: dict[str, Any], section_number: int, lang: str) -> list[str]:
    checks = data.get("checks", {})
    if not checks:
        return []

    lines = [f"### 3.{section_number} {L(lang, 'Additional environment elements', '补充环境要素')}", ""]
    for check_id in sorted(checks.keys()):
        check = checks[check_id]
        lines.append(dash(check.get("label", check_id), check.get("status"), lang))
        lines.append(L(lang, f"  - Command: {code(' '.join(check.get('command', [])))}", f"  - 命令：{code(' '.join(check.get('command', [])))}"))
        if check.get("matched_patterns"):
            lines.append(L(lang, f"  - Matched patterns: {code(', '.join(check['matched_patterns']))}", f"  - 命中模式：{code(', '.join(check['matched_patterns']))}"))
    return lines


def render_policy(data: dict[str, Any], baseline_name: str, lang: str) -> str:
    env_vars = data.get("environment_variables", {})
    os_family = detect_os_family(data)
    platform_text = first_nonempty(data.get("context", {}).get("platform"), data.get("context", {}).get("platform_system"))
    date_text = render_date(data.get("generated_at"))
    lines: list[str] = [
        L(lang, "# Global Environment Policy", "# 全局环境政策"),
        "",
        L(lang, f"Last updated: {date_text}", f"最后更新：{date_text}"),
        "",
        L(lang, "## 1. Overview", "## 1. 说明"),
        "",
        L(lang, "This document is the master environment policy for the current machine.", "这份文档是当前机器环境的主文档。"),
        "",
        L(
            lang,
            f"Current baseline platform: {code(os_label(os_family))}; platform fingerprint: {code(platform_text)}.",
            f"当前基线平台：{code(os_label(os_family))}，平台指纹：{code(platform_text)}。",
        ),
        "",
        L(
            lang,
            "All models, AI agents, CLIs, OpenClaw sessions, or other automations must read this document before performing environment-related work.",
            "所有模型、AI、CLI、OpenClaw 或其他自动化代理在任何工作目录下，只要涉及环境相关任务，都应先读取本文件。",
        ),
        "",
        L(
            lang,
            f"Keep the reusable machine-readable baseline in {code(baseline_name)} when possible. This document records the approved environment and the hard rules derived from verified facts.",
            f"机器可复用基线建议保存在 {code(baseline_name)}；本文件负责记录经验证后批准使用的环境与硬性规则。",
        ),
        "",
        L(lang, "## 2. Basic Rules", "## 2. 基本规则"),
        "",
        L(lang, "### 2.1 Prohibited Actions", "### 2.1 禁止事项"),
        "",
        L(lang, "- Do not download, install, upgrade, uninstall, or auto-configure software, CLIs, SDKs, runtimes, databases, browsers, drivers, plugins, or global dependencies without explicit user approval.", "- 未经用户明确要求，不得下载、安装、升级、卸载或自动配置任何软件、CLI、SDK、运行时、数据库、浏览器、驱动、插件或全局依赖。"),
        L(lang, "- Do not modify `PATH`, `JAVA_HOME`, `MAVEN_HOME`, or other environment variables without explicit user approval.", "- 未经用户明确要求，不得修改 `PATH`、`JAVA_HOME`、`MAVEN_HOME` 等环境变量。"),
        L(lang, "- Do not assume that tools not listed in this document or the baseline are already installed.", "- 对于本文件或基线中未列出的工具，不得默认假定本机已经安装。"),
        "",
        L(lang, "### 2.2 What To Do When Tools Are Missing", "### 2.2 缺工具时的处理方式"),
        "",
        L(lang, "If the current task depends on a missing tool, CLI, SDK, service, or other environment component, you must:", "如果任务需要本机当前没有的工具、CLI、SDK、服务或其他环境组件，必须："),
        "",
        L(lang, "1. Tell the user which tool is missing.", "1. 告诉用户缺少什么工具。"),
        L(lang, "2. Explain why it is needed.", "2. 说明为什么需要。"),
        L(lang, "3. Ask the user to return the executable path or install directory after installation.", "3. 说明希望用户提供哪个可执行文件路径或安装目录。"),
        L(lang, "4. Default to user-managed installation. Only continue with self-installation when the user explicitly authorizes it.", "4. 默认等待用户自行安装；只有用户明确授权并要求代理代装时，才可继续安装。"),
        L(lang, f"5. Update both this document and {code(baseline_name)} after installation or verification.", f"5. 安装或校验完成后，同时更新本文件和 {code(baseline_name)}。"),
        "",
        L(lang, "## 3. Approved Environment", "## 3. 当前批准使用的环境"),
        "",
    ]

    section_number = 1
    for tool_id, tool in ordered_tools(data):
        if tool.get("status") == "found":
            lines.extend(render_tool_section(tool_id, tool, section_number, env_vars, os_family, lang))
            lines.append("")
            section_number += 1

    missing_lines = render_missing_tools(data, section_number, lang)
    if missing_lines:
        lines.extend(missing_lines)
        lines.append("")
        section_number += 1

    check_lines = render_checks(data, section_number, lang)
    if check_lines:
        lines.extend(check_lines)
        lines.append("")

    lines.extend(
        [
            L(lang, "## 4. Environment Variables", "## 4. 当前环境变量"),
            "",
        ]
    )
    for name in sorted(env_vars.keys()):
        value = env_vars[name].get("value")
        if value:
            lines.append(f"- `{name}={value}`")
    lines.append("")
    lines.append(L(lang, "Important PATH entries include:", "当前用户 `PATH` 中的重要项包括："))
    lines.append("")
    for entry in data.get("path", {}).get("important_entries", []):
        lines.append(f"- {code(format_path_entry(entry, env_vars, os_family))}")

    lines.extend(
        [
            "",
            L(lang, "## 5. Execution Requirements", "## 5. 环境相关任务的执行要求"),
            "",
            L(lang, "Before running build, run, test, debug, script, database, service, migration, or startup tasks, check:", "遇到构建、运行、测试、调试、脚本执行、数据库连接、服务启动、迁移、开机启动等任务时，先检查："),
            "",
            L(lang, "1. The current environment facts in this document.", "1. 本文件中的当前环境说明。"),
            L(lang, f"2. Whether {code(baseline_name)} already contains a matching baseline.", f"2. {code(baseline_name)} 中是否已有对应基线。"),
            L(lang, "3. Whether the target tool really exists.", "3. 目标工具是否真的存在。"),
            L(lang, "4. Whether the version fits the current task.", "4. 版本是否符合当前任务要求。"),
            L(lang, "5. Whether the planned operation will trigger installation, upgrade, global writes, or environment changes.", "5. 本次操作是否会触发安装、升级、全局写入或环境改动。"),
            "",
            L(lang, "If item 5 is true, obtain explicit user approval first.", "如果第 5 项答案是“会”，必须先得到用户明确同意。"),
            "",
            L(lang, "## 6. Maintenance Rules", "## 6. 后续维护要求"),
            "",
            L(lang, f"- Update both this document and {code(baseline_name)} whenever verified environment facts change.", f"- 只要环境事实变化，就同步更新本文件和 {code(baseline_name)}。"),
            L(lang, "- If the task only introduces one new tool, verify it surgically instead of doing a blind full rescan.", "- 如果任务只涉及一个新工具，先做针对性校验，不要盲目全量重扫。"),
            L(lang, "- Keep shims, wrappers, symlinks, startup scripts, and real install directories separate in the docs.", "- 对 shim、wrapper、symlink、启动脚本和真实安装目录要分开记录，避免混淆。"),
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def render_agents_snippet(policy_name: str, baseline_name: str, lang: str) -> str:
    lines = [
        L(lang, "# Environment Rules", "# 环境规则"),
        "",
        L(lang, "## Read This First", "## 先读这里"),
        "",
        L(lang, f"- Read {code(policy_name)} before any task involving local tools, CLIs, SDKs, runtimes, compilers, environment variables, databases, services, startup scripts, builds, tests, or debugging.", f"- 只要任务涉及本机工具、CLI、SDK、运行时、编译器、环境变量、数据库、服务、脚本启动、构建、测试或调试，先读取 {code(policy_name)}。"),
        L(lang, f"- If {code(baseline_name)} already exists, reuse it as the machine-readable baseline. If it does not exist, detect the machine first and write it.", f"- 如果 {code(baseline_name)} 已存在，优先将其作为机器可复用基线；不存在时先探测并写入。"),
        "",
        L(lang, "## Hard Rules", "## 硬性规则"),
        "",
        L(lang, "- Do not download, install, upgrade, uninstall, or auto-configure software, CLIs, SDKs, runtimes, databases, browsers, drivers, plugins, or global dependencies without explicit user approval.", "- 未经用户明确要求，不得下载、安装、升级、卸载或自动配置任何软件、CLI、SDK、运行时、数据库、浏览器、驱动、插件或全局依赖。"),
        L(lang, "- Do not modify `PATH`, `JAVA_HOME`, `MAVEN_HOME`, or other environment variables without explicit user approval.", "- 未经用户明确要求，不得修改 `PATH`、`JAVA_HOME`、`MAVEN_HOME` 等环境变量。"),
        L(lang, "- Full filesystem access does not mean you may change the machine environment without permission.", "- 完全访问权限不等于可以擅自改动本机环境。"),
        "",
        L(lang, "## What To Do When Tools Are Missing", "## 缺工具时必须怎么做"),
        "",
        L(lang, "- Tell the user exactly which tool is missing.", "- 明确告诉用户缺少哪个工具。"),
        L(lang, "- Explain why that tool is needed.", "- 说明这个工具为什么需要。"),
        L(lang, "- Ask for the executable path or install directory that should be returned after installation.", "- 告诉用户安装完成后需要返回哪个可执行文件路径或安装目录。"),
        L(lang, "- Default to user-managed installation. Only install the tool yourself when the user explicitly authorizes it.", "- 默认等待用户自行安装；只有用户明确授权并要求代理代装时，才可安装。"),
        L(lang, f"- Update both {code(policy_name)} and {code(baseline_name)} after verification.", f"- 校验完成后，更新 {code(policy_name)} 和 {code(baseline_name)}。"),
        "",
        L(lang, "## Execution Style", "## 执行方式"),
        "",
        L(lang, "- Prefer tools that already exist on the machine and are already recorded in the baseline.", "- 优先使用机器上已经存在并已登记的工具。"),
        L(lang, "- Use absolute paths, version commands, and targeted probes to verify that a tool is really available.", "- 用绝对路径、版本命令和针对性探针检查工具是否真的可用。"),
        L(lang, "- If the existing baseline and the live machine disagree, re-check the mismatch before updating docs.", "- 如果已有基线与现场不一致，先局部复核，再更新文档。"),
        L(lang, "- Do not confuse shims, wrappers, symlinks, or startup scripts with the real install root.", "- 不要把 shim、wrapper、symlink 或启动脚本误认为真实安装根目录。"),
    ]
    return "\n".join(lines).rstrip() + "\n"


def render_skill_snippet(policy_name: str, baseline_name: str, lang: str) -> str:
    lines = [
        L(lang, "## Environment Baseline", "## 环境基线"),
        "",
        L(lang, f"- Read {code(policy_name)} before any build, run, test, debug, install, service, database, compiler, runtime, or startup-script task.", f"- 在任何构建、运行、测试、调试、安装、服务、数据库、编译器、运行时或启动脚本任务之前，先读取 {code(policy_name)}。"),
        L(lang, f"- Reuse {code(baseline_name)} as the machine-readable baseline when it already exists.", f"- 如果 {code(baseline_name)} 已存在，优先复用它作为机器可读基线。"),
        L(lang, "- If the baseline does not exist, detect the current machine first and write the baseline before describing the environment.", "- 如果基线不存在，先探测当前机器并写入基线，再描述环境。"),
        L(lang, "- If a task mentions a tool that is missing from the baseline, verify that tool first and then update both the baseline and human-readable docs.", "- 如果任务提到一个未出现在基线中的工具，先定向校验该工具，再更新基线和人类可读文档。"),
        L(lang, "- If a required tool is missing, ask the user to install it or obtain explicit approval before installing it yourself.", "- 如果缺少必需工具，先让用户安装，或在自行安装前取得明确授权。"),
        L(lang, "- Keep shims, wrappers, symlinks, launchers, startup scripts, and real install directories clearly separated in the docs.", "- 在文档中清晰区分 shim、wrapper、symlink、launcher、启动脚本和真实安装目录。"),
    ]
    return "\n".join(lines).rstrip() + "\n"


def write_output(path: str | None, content: str) -> None:
    if not path:
        return
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Render ENVIRONMENT_POLICY, AGENTS, and skill snippets from a baseline JSON."
    )
    parser.add_argument("baseline", help="Path to environment-baseline.json")
    parser.add_argument("--policy-out", help="Write ENVIRONMENT_POLICY markdown here.")
    parser.add_argument("--agents-out", help="Write AGENTS environment snippet here.")
    parser.add_argument("--skill-snippet-out", help="Write a reusable skill snippet here.")
    parser.add_argument(
        "--policy-name",
        default="ENVIRONMENT_POLICY.md",
        help="Display name used inside the rendered documents.",
    )
    parser.add_argument(
        "--baseline-name",
        default="environment-baseline.json",
        help="Display name used inside the rendered documents.",
    )
    parser.add_argument(
        "--lang",
        default="auto",
        help="Document language preference: auto, en, or zh.",
    )
    parser.add_argument(
        "--stdout",
        choices=["policy", "agents", "skill"],
        help="Print one rendered document to stdout.",
    )
    args = parser.parse_args()

    data = load_json(args.baseline)
    lang = choose_document_language(data, args.lang)
    policy = render_policy(data, args.baseline_name, lang)
    agents = render_agents_snippet(args.policy_name, args.baseline_name, lang)
    skill = render_skill_snippet(args.policy_name, args.baseline_name, lang)

    write_output(args.policy_out, policy)
    write_output(args.agents_out, agents)
    write_output(args.skill_snippet_out, skill)

    if args.stdout == "policy":
        print(policy, end="")
    elif args.stdout == "agents":
        print(agents, end="")
    elif args.stdout == "skill":
        print(skill, end="")


if __name__ == "__main__":
    main()
