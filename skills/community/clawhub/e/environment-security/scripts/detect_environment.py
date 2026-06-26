#!/usr/bin/env python3
"""Detect local environment facts and maintain a reusable baseline JSON."""

from __future__ import annotations

import argparse
import json
import locale
import os
import platform
import re
import socket
import subprocess
import sys
import sysconfig
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

DEFAULT_TOOL_SPECS: dict[str, dict[str, Any]] = {
    "git": {
        "label": "Git",
        "commands": ["git"],
        "version_command": ["{selected_executable}", "--version"],
        "version_regex": r"git version\s+(.+)",
    },
    "java": {
        "label": "Java",
        "commands": ["java"],
        "env_var_hint": "JAVA_HOME",
        "env_var_suffix_windows": ["bin", "java.exe"],
        "env_var_suffix_posix": ["bin", "java"],
        "version_command": ["{selected_executable}", "-version"],
        "version_stream": "stderr",
        "version_regex": r'version "([^"]+)"',
    },
    "javac": {
        "label": "javac",
        "commands": ["javac"],
        "env_var_hint": "JAVA_HOME",
        "env_var_suffix_windows": ["bin", "javac.exe"],
        "env_var_suffix_posix": ["bin", "javac"],
        "version_command": ["{selected_executable}", "-version"],
        "version_regex": r"javac\s+([^\s]+)",
    },
    "maven": {
        "label": "Maven",
        "commands_windows": ["mvn.cmd", "mvn"],
        "commands_posix": ["mvn"],
        "env_var_hint": "MAVEN_HOME",
        "env_var_suffix_windows": ["bin", "mvn.cmd"],
        "env_var_suffix_posix": ["bin", "mvn"],
        "version_command": ["{selected_executable}", "-version"],
        "version_regex": r"Apache Maven\s+([^\s]+)",
    },
    "gradle": {
        "label": "Gradle",
        "commands_windows": ["gradle.bat", "gradle"],
        "commands_posix": ["gradle"],
        "env_var_hint": "GRADLE_HOME",
        "env_var_suffix_windows": ["bin", "gradle.bat"],
        "env_var_suffix_posix": ["bin", "gradle"],
        "version_command": ["{selected_executable}", "--version"],
        "version_regex": r"Gradle\s+([^\s]+)",
    },
    "node": {
        "label": "Node.js",
        "commands": ["node", "nodejs"],
        "version_command": ["{selected_executable}", "--version"],
        "version_regex": r"(v\d+\.\d+\.\d+)",
    },
    "npm": {
        "label": "npm",
        "commands_windows": ["npm.cmd", "npm"],
        "commands_posix": ["npm"],
        "version_command": ["{selected_executable}", "--version"],
        "version_regex": r"(\d+\.\d+\.\d+)",
    },
    "pnpm": {
        "label": "pnpm",
        "commands_windows": ["pnpm.cmd", "pnpm"],
        "commands_posix": ["pnpm"],
        "version_command": ["{selected_executable}", "--version"],
        "version_regex": r"([^\s]+)",
    },
    "yarn": {
        "label": "Yarn",
        "commands_windows": ["yarn.cmd", "yarn"],
        "commands_posix": ["yarn"],
        "version_command": ["{selected_executable}", "--version"],
        "version_regex": r"([^\s]+)",
    },
    "python": {
        "label": "Python",
        "commands_windows": ["python", "py"],
        "commands_posix": ["python3", "python"],
        "selection_strategy": "current_python",
        "version_command": ["{selected_executable}", "--version"],
        "version_regex": r"Python\s+([^\s]+)",
    },
    "go": {
        "label": "Go",
        "commands": ["go"],
        "env_var_hint": "GOROOT",
        "env_var_suffix_windows": ["bin", "go.exe"],
        "env_var_suffix_posix": ["bin", "go"],
        "version_command": ["{selected_executable}", "version"],
        "version_regex": r"go version go([^\s]+)",
    },
    "rustc": {
        "label": "Rust",
        "commands": ["rustc"],
        "version_command": ["{selected_executable}", "--version"],
        "version_regex": r"rustc\s+([^\s]+)",
    },
    "cargo": {
        "label": "Cargo",
        "commands": ["cargo"],
        "env_var_hint": "CARGO_HOME",
        "env_var_suffix_windows": ["bin", "cargo.exe"],
        "env_var_suffix_posix": ["bin", "cargo"],
        "version_command": ["{selected_executable}", "--version"],
        "version_regex": r"cargo\s+([^\s]+)",
    },
    "rustup": {
        "label": "Rustup",
        "commands": ["rustup"],
        "env_var_hint": "CARGO_HOME",
        "env_var_suffix_windows": ["bin", "rustup.exe"],
        "env_var_suffix_posix": ["bin", "rustup"],
        "version_command": ["{selected_executable}", "--version"],
        "version_regex": r"rustup\s+([^\s]+)",
    },
    "clang": {
        "label": "Clang",
        "commands": ["clang"],
        "version_command": ["{selected_executable}", "--version"],
    },
    "clangxx": {
        "label": "Clang++",
        "commands": ["clang++"],
        "version_command": ["{selected_executable}", "--version"],
    },
    "gcc": {
        "label": "GCC",
        "commands": ["gcc"],
        "version_command": ["{selected_executable}", "--version"],
    },
    "gxx": {
        "label": "G++",
        "commands": ["g++"],
        "version_command": ["{selected_executable}", "--version"],
    },
    "cmake": {
        "label": "CMake",
        "commands": ["cmake"],
        "version_command": ["{selected_executable}", "--version"],
        "version_regex": r"cmake version\s+([^\s]+)",
    },
    "make": {
        "label": "Make",
        "commands": ["make"],
        "version_command": ["{selected_executable}", "--version"],
        "version_regex": r"GNU Make\s+([^\s]+)",
    },
    "ninja": {
        "label": "Ninja",
        "commands": ["ninja"],
        "version_command": ["{selected_executable}", "--version"],
        "version_regex": r"([^\s]+)",
    },
    "ruby": {
        "label": "Ruby",
        "commands": ["ruby"],
        "version_command": ["{selected_executable}", "--version"],
        "version_regex": r"ruby\s+([^\s]+)",
    },
    "gem": {
        "label": "RubyGems",
        "commands_windows": ["gem.bat", "gem"],
        "commands_posix": ["gem"],
        "version_command": ["{selected_executable}", "--version"],
        "version_regex": r"([^\s]+)",
    },
    "bundler": {
        "label": "Bundler",
        "commands_windows": ["bundle.bat", "bundle", "bundler.bat", "bundler"],
        "commands_posix": ["bundle", "bundler"],
        "version_command": ["{selected_executable}", "--version"],
        "version_regex": r"Bundler version\s+([^\s]+)",
    },
    "php": {
        "label": "PHP",
        "commands": ["php"],
        "version_command": ["{selected_executable}", "--version"],
        "version_regex": r"PHP\s+([^\s]+)",
    },
    "composer": {
        "label": "Composer",
        "commands_windows": ["composer.bat", "composer"],
        "commands_posix": ["composer"],
        "version_command": ["{selected_executable}", "--version"],
        "version_regex": r"Composer version\s+([^\s]+)",
    },
    "dotnet": {
        "label": ".NET SDK",
        "commands": ["dotnet"],
        "env_var_hint": "DOTNET_ROOT",
        "env_var_suffix_windows": ["dotnet.exe"],
        "env_var_suffix_posix": ["dotnet"],
        "version_command": ["{selected_executable}", "--version"],
        "version_regex": r"([^\s]+)",
    },
    "docker": {
        "label": "Docker",
        "commands": ["docker"],
        "version_command": ["{selected_executable}", "--version"],
        "version_regex": r"Docker version\s+([^,\s]+)",
    },
    "kubectl": {
        "label": "kubectl",
        "commands": ["kubectl"],
        "version_command": ["{selected_executable}", "version", "--client"],
        "version_regex": r"Client Version:\s*v?([^\s]+)",
    },
}

DEFAULT_ENV_VARS = [
    "JAVA_HOME",
    "MAVEN_HOME",
    "GRADLE_HOME",
    "GOROOT",
    "GOPATH",
    "CARGO_HOME",
    "RUSTUP_HOME",
    "NVM_DIR",
    "PYENV_ROOT",
    "RBENV_ROOT",
    "SDKMAN_DIR",
    "HOMEBREW_PREFIX",
    "VIRTUAL_ENV",
    "GEM_HOME",
    "BUNDLE_PATH",
    "COMPOSER_HOME",
    "DOTNET_ROOT",
    "CC",
    "CXX",
]
COMMON_PATH_MARKERS = [
    "java",
    "maven",
    "gradle",
    "node",
    "python",
    "go",
    "cargo",
    "rust",
    "llvm",
    "clang",
    "gcc",
    "cmake",
    "ninja",
    "ruby",
    "php",
    "composer",
    "dotnet",
    "docker",
    "kube",
]
PLATFORM_PATH_MARKERS = {
    "windows": ["windowsapps", "nvm", "nodejs", "cargo", "rustup", "dotnet", "scoop", "chocolatey", "msys", "mingw", "ruby", "php"],
    "macos": [".nvm", ".pyenv", ".rbenv", ".sdkman", ".cargo", ".rustup", "/opt/homebrew", "/usr/local/bin"],
    "linux": [".nvm", ".pyenv", ".rbenv", ".sdkman", ".cargo", ".rustup", "/usr/local/bin", "/usr/lib/jvm", "/snap/bin"],
}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def detect_os_family() -> str:
    system = platform.system().lower()
    if system == "windows":
        return "windows"
    if system == "darwin":
        return "macos"
    if system == "linux":
        return "linux"
    return system or "unknown"


def canonicalize_path(raw: str | None) -> str | None:
    if not raw:
        return None
    try:
        return str(Path(raw).expanduser().resolve())
    except OSError:
        return os.path.normpath(os.path.expanduser(raw))


def path_exists(raw: str | None) -> bool:
    if not raw:
        return False
    try:
        return Path(raw).expanduser().exists()
    except OSError:
        return False


def is_windows() -> bool:
    return os.name == "nt"


def normalize_tool_id(raw: str) -> str:
    return raw.strip().lower().replace("_", "-")


def unique_strings(values: list[str]) -> list[str]:
    seen: set[str] = set()
    output: list[str] = []
    for item in values:
        key = os.path.normcase(os.path.normpath(item))
        if key in seen:
            continue
        seen.add(key)
        output.append(item)
    return output


def trim_text(text: str, max_chars: int = 1200, max_lines: int = 20) -> str:
    lines = text.splitlines()
    if len(lines) > max_lines:
        lines = lines[:max_lines]
    trimmed = "\n".join(lines)
    if len(trimmed) > max_chars:
        trimmed = trimmed[: max_chars - 3] + "..."
    return trimmed


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

    if is_windows():
        try:
            import ctypes

            lang_id = ctypes.windll.kernel32.GetUserDefaultUILanguage()
            windows_locale = locale.windows_locale.get(lang_id)
            if windows_locale:
                candidates.append(windows_locale)
        except Exception:
            pass

    return unique_strings([item for item in candidates if item])


def choose_document_language(explicit_lang: str | None) -> tuple[str, str | None, list[str], str]:
    normalized_explicit = normalize_lang(explicit_lang)
    if explicit_lang and explicit_lang != "auto" and normalized_explicit:
        return normalized_explicit, explicit_lang, [explicit_lang], "argument"

    candidates = detect_locale_candidates()
    for candidate in candidates:
        normalized = normalize_lang(candidate)
        if normalized:
            return normalized, candidate, candidates, "system"

    return "en", candidates[0] if candidates else None, candidates, "default"


def run_command(command: list[str], timeout: int = 8, cwd: str | None = None) -> dict[str, Any]:
    try:
        completed = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
            check=False,
            cwd=cwd,
        )
    except FileNotFoundError as exc:
        return {
            "status": "error",
            "error": str(exc),
            "exit_code": None,
            "stdout": "",
            "stderr": "",
            "combined": str(exc),
        }
    except OSError as exc:
        return {
            "status": "error",
            "error": str(exc),
            "exit_code": None,
            "stdout": "",
            "stderr": "",
            "combined": str(exc),
        }
    except subprocess.TimeoutExpired as exc:
        stdout = exc.stdout or ""
        stderr = exc.stderr or ""
        return {
            "status": "timeout",
            "error": f"Timed out after {timeout}s",
            "exit_code": None,
            "stdout": stdout,
            "stderr": stderr,
            "combined": (stdout + "\n" + stderr).strip(),
        }

    combined = "\n".join(part for part in [completed.stdout, completed.stderr] if part).strip()
    return {
        "status": "ok" if completed.returncode == 0 else "nonzero_exit",
        "exit_code": completed.returncode,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
        "combined": combined,
    }


def windows_executable_rank(candidate: str) -> int:
    extension = Path(candidate).suffix.lower()
    if extension == ".exe":
        return 0
    if extension == ".cmd":
        return 1
    if extension == ".bat":
        return 2
    if extension == ".com":
        return 3
    if extension:
        return 4
    return 5


def resolve_command_matches(command: str) -> list[str]:
    if is_windows():
        result = run_command(["where.exe", command])
    else:
        result = run_command(["which", "-a", command])
    if result["status"] not in {"ok", "nonzero_exit"}:
        return []
    matches = []
    for line in result["stdout"].splitlines():
        stripped = line.strip()
        if stripped and path_exists(stripped):
            matches.append(canonicalize_path(stripped) or stripped)
    ordered = unique_strings(matches)
    if is_windows():
        ordered.sort(key=windows_executable_rank)
    return ordered


def extract_version(text: str, regex: str | None) -> str | None:
    if not text:
        return None
    if regex:
        match = re.search(regex, text, flags=re.MULTILINE)
        if match:
            return match.group(1).strip()
        return None
    first_line = next((line.strip() for line in text.splitlines() if line.strip()), "")
    return first_line or None


def load_json(path: str | None) -> dict[str, Any] | None:
    if not path:
        return None
    candidate = Path(path)
    if not candidate.exists():
        return None
    return json.loads(candidate.read_text(encoding="utf-8-sig"))


def choose_baseline_path(args: argparse.Namespace) -> str | None:
    if args.baseline:
        return args.baseline
    if args.output and Path(args.output).exists():
        return args.output
    return None


def load_probe_file(path: str | None) -> dict[str, Any]:
    if not path:
        return {}
    probe_path = Path(path)
    return json.loads(probe_path.read_text(encoding="utf-8-sig"))


def merge_tool_specs(extra_probe_data: dict[str, Any]) -> dict[str, dict[str, Any]]:
    merged = deepcopy(DEFAULT_TOOL_SPECS)
    for item in extra_probe_data.get("tools", []):
        tool_id = normalize_tool_id(item["id"])
        base = merged.get(tool_id, {})
        combined = deepcopy(base)
        combined.update(item)
        combined["id"] = tool_id
        merged[tool_id] = combined
    return merged


def get_requested_tool_ids(
    raw_tools: str | None,
    tool_specs: dict[str, dict[str, Any]],
    baseline_data: dict[str, Any] | None,
) -> list[str]:
    if not raw_tools:
        return list(tool_specs.keys())

    requested = [normalize_tool_id(item) for item in raw_tools.split(",") if item.strip()]
    unknown = [
        item
        for item in requested
        if item not in tool_specs and item not in (baseline_data or {}).get("tools", {})
    ]
    if unknown:
        known = ", ".join(sorted(tool_specs.keys()))
        raise SystemExit(f"Unknown tool id(s): {', '.join(unknown)}. Known ids: {known}")
    return requested


def lookup_commands(spec: dict[str, Any]) -> list[str]:
    family = detect_os_family()
    if family == "windows" and spec.get("commands_windows"):
        return spec["commands_windows"]
    if family == "macos" and spec.get("commands_macos"):
        return spec["commands_macos"]
    if family == "linux" and spec.get("commands_linux"):
        return spec["commands_linux"]
    if family in {"macos", "linux"} and spec.get("commands_posix"):
        return spec["commands_posix"]
    return spec.get("commands", [])


def env_var_suffix(spec: dict[str, Any]) -> list[str] | None:
    family = detect_os_family()
    if family == "windows":
        return spec.get("env_var_suffix_windows") or spec.get("env_var_suffix")
    if family == "macos":
        return (
            spec.get("env_var_suffix_macos")
            or spec.get("env_var_suffix_posix")
            or spec.get("env_var_suffix")
        )
    if family == "linux":
        return (
            spec.get("env_var_suffix_linux")
            or spec.get("env_var_suffix_posix")
            or spec.get("env_var_suffix")
        )
    return spec.get("env_var_suffix")


def preferred_executable_from_env(spec: dict[str, Any], env_vars: dict[str, str]) -> str | None:
    env_var_hint = spec.get("env_var_hint")
    if not env_var_hint:
        return None
    env_value = env_vars.get(env_var_hint)
    if not env_value:
        return None
    suffix = env_var_suffix(spec)
    if not suffix:
        return None
    candidate = os.path.join(env_value, *suffix)
    return canonicalize_path(candidate)


def first_existing_path(values: list[str | None]) -> str | None:
    for value in values:
        normalized = canonicalize_path(value)
        if normalized and path_exists(normalized):
            return normalized
    return None


def build_lookup_summary(commands: list[str]) -> dict[str, Any]:
    command_hits: dict[str, list[str]] = {}
    all_matches: list[str] = []
    for command in commands:
        matches = resolve_command_matches(command)
        command_hits[command] = matches
        all_matches.extend(matches)
    ordered = unique_strings(all_matches)
    return {
        "commands": commands,
        "command_hits": command_hits,
        "all_matches": ordered,
        "path_hit": ordered[0] if ordered else None,
    }


def compare_paths(left: str | None, right: str | None) -> bool | None:
    if left is None or right is None:
        return None
    return os.path.normcase(os.path.normpath(left)) == os.path.normcase(os.path.normpath(right))


def build_version_command(spec: dict[str, Any], selected_executable: str | None) -> list[str] | None:
    template = spec.get("version_command")
    if not template or not selected_executable:
        return None
    command: list[str] = []
    for item in template:
        if item == "{selected_executable}":
            command.append(selected_executable)
        else:
            command.append(item)
    return command


def choose_selected_executable(
    spec: dict[str, Any],
    baseline_entry: dict[str, Any] | None,
    env_vars: dict[str, str],
    lookup_summary: dict[str, Any],
) -> tuple[str | None, str]:
    baseline_entry = baseline_entry or {}
    baseline_candidates = [
        baseline_entry.get("selected_executable"),
        baseline_entry.get("preferred_path"),
        baseline_entry.get("resolved_path"),
    ]
    baseline_choice = first_existing_path(baseline_candidates)
    if baseline_choice:
        return baseline_choice, "baseline"

    if spec.get("selection_strategy") == "current_python":
        current_python = canonicalize_path(sys.executable)
        if current_python and path_exists(current_python):
            return current_python, "current_python"

    env_choice = preferred_executable_from_env(spec, env_vars)
    if env_choice and path_exists(env_choice):
        return env_choice, "env_var_hint"

    path_hit = lookup_summary.get("path_hit")
    if path_hit and path_exists(path_hit):
        return path_hit, "path_hit"

    return None, "unresolved"


def summarize_version_probe(
    spec: dict[str, Any],
    selected_executable: str | None,
) -> dict[str, Any]:
    command = build_version_command(spec, selected_executable)
    if not command:
        return {
            "status": "skipped",
            "version": None,
            "version_text": "",
            "version_command": None,
            "exit_code": None,
        }

    result = run_command(command)
    stream = spec.get("version_stream", "combined")
    version_text = result.get(stream, "") if stream in {"stdout", "stderr", "combined"} else result["combined"]
    version_text = trim_text(version_text)
    version = extract_version(version_text or result["combined"], spec.get("version_regex"))
    return {
        "status": result["status"],
        "version": version,
        "version_text": version_text or trim_text(result["combined"]),
        "version_command": command,
        "exit_code": result["exit_code"],
        "stdout": trim_text(result["stdout"]),
        "stderr": trim_text(result["stderr"]),
    }


def detect_tool(
    tool_id: str,
    spec: dict[str, Any],
    baseline_entry: dict[str, Any] | None,
    env_vars: dict[str, str],
) -> dict[str, Any]:
    commands = lookup_commands(spec)
    lookup_summary = build_lookup_summary(commands)
    selected_executable, selection_reason = choose_selected_executable(
        spec, baseline_entry, env_vars, lookup_summary
    )
    version_probe = summarize_version_probe(spec, selected_executable)
    baseline_selected = canonicalize_path((baseline_entry or {}).get("selected_executable"))
    path_hit = canonicalize_path(lookup_summary.get("path_hit"))
    preferred_path = selected_executable or preferred_executable_from_env(spec, env_vars)

    notes: list[str] = []
    if selection_reason == "baseline" and not compare_paths(baseline_selected, path_hit):
        notes.append("Existing baseline path was preferred over the current PATH hit.")
    if selection_reason == "env_var_hint" and not compare_paths(selected_executable, path_hit):
        env_var_hint = spec.get("env_var_hint")
        if env_var_hint:
            notes.append(
                f"PATH currently resolves a different executable; {env_var_hint} was used as the approved path."
            )
    if spec.get("selection_strategy") == "current_python":
        launcher_hit = next(iter(lookup_summary["all_matches"]), None)
        if launcher_hit and not compare_paths(launcher_hit, selected_executable):
            notes.append(
                "The launcher found on PATH resolves to a different executable than the current interpreter."
            )

    status = "found" if selected_executable else "missing"
    entry: dict[str, Any] = {
        "id": tool_id,
        "label": spec.get("label", tool_id),
        "status": status,
        "commands": commands,
        "lookup": lookup_summary,
        "selected_executable": selected_executable,
        "selection_reason": selection_reason,
        "preferred_path": preferred_path,
        "resolved_path": path_hit,
        "baseline_match": compare_paths(selected_executable, baseline_selected),
        "version": version_probe["version"],
        "version_text": version_probe["version_text"],
        "version_command": version_probe["version_command"],
        "version_probe_status": version_probe["status"],
        "version_probe_exit_code": version_probe["exit_code"],
        "notes": notes,
    }

    if tool_id == "python":
        interpreter_path = Path(sys.executable).resolve()
        interpreter_root = interpreter_path.parent.parent
        entry["details"] = {
            "current_interpreter": canonicalize_path(sys.executable),
            "scripts_dir": canonicalize_path(sysconfig.get_path("scripts")),
            "bin_dir": first_existing_path(
                [
                    canonicalize_path(str(interpreter_root / "bin")),
                    canonicalize_path(sysconfig.get_path("scripts")),
                    canonicalize_path(str(interpreter_path.parent)),
                ]
            ),
            "python_launcher": next(iter(lookup_summary["command_hits"].get("python", [])), None),
            "python3_launcher": next(iter(lookup_summary["command_hits"].get("python3", [])), None),
            "py_launcher": next(iter(lookup_summary["command_hits"].get("py", [])), None),
        }

    return entry


def collect_environment_variables(
    extra_probe_data: dict[str, Any],
    baseline_data: dict[str, Any] | None,
) -> dict[str, dict[str, Any]]:
    requested = set(DEFAULT_ENV_VARS)
    requested.update(extra_probe_data.get("env_vars", []))
    requested.update((baseline_data or {}).get("environment_variables", {}).keys())
    output: dict[str, dict[str, Any]] = {}
    for name in sorted(requested):
        value = os.environ.get(name)
        output[name] = {
            "status": "set" if value else "unset",
            "value": value,
        }
    return output


def important_path_markers(extra_probe_data: dict[str, Any]) -> list[str]:
    family = detect_os_family()
    markers = list(COMMON_PATH_MARKERS)
    markers.extend(PLATFORM_PATH_MARKERS.get(family, []))
    markers.extend(extra_probe_data.get("important_path_contains", []))
    return [item.lower() for item in markers]


def build_path_summary(
    tools: dict[str, dict[str, Any]],
    env_variables: dict[str, dict[str, Any]],
    extra_probe_data: dict[str, Any],
) -> dict[str, Any]:
    raw_path = os.environ.get("PATH", "")
    entries = [canonicalize_path(item) or item for item in raw_path.split(os.pathsep) if item]
    important_entries: list[str] = []

    def maybe_add(value: str | None) -> None:
        normalized = canonicalize_path(value)
        if normalized and normalized in entries and normalized not in important_entries:
            important_entries.append(normalized)

    java_home = env_variables.get("JAVA_HOME", {}).get("value")
    maven_home = env_variables.get("MAVEN_HOME", {}).get("value")
    if java_home:
        maybe_add(os.path.join(java_home, "bin"))
    if maven_home:
        maybe_add(os.path.join(maven_home, "bin"))

    for name in [
        "NVM_DIR",
        "PYENV_ROOT",
        "RBENV_ROOT",
        "SDKMAN_DIR",
        "HOMEBREW_PREFIX",
        "VIRTUAL_ENV",
        "GRADLE_HOME",
        "GOROOT",
        "GOPATH",
        "CARGO_HOME",
        "RUSTUP_HOME",
        "GEM_HOME",
        "BUNDLE_PATH",
        "COMPOSER_HOME",
        "DOTNET_ROOT",
    ]:
        value = env_variables.get(name, {}).get("value")
        if value:
            maybe_add(value)
            maybe_add(os.path.join(value, "bin"))

    for tool in tools.values():
        selected = tool.get("selected_executable")
        if selected:
            maybe_add(str(Path(selected).parent))
        if tool["id"] == "python":
            maybe_add(tool.get("details", {}).get("bin_dir"))
            maybe_add(tool.get("details", {}).get("scripts_dir"))

    markers = important_path_markers(extra_probe_data)
    for entry in entries:
        if entry in important_entries:
            continue
        if any(marker in entry.lower() for marker in markers):
            important_entries.append(entry)

    return {
        "entries": entries,
        "important_entries": important_entries,
        "separator": os.pathsep,
    }


def run_checks(extra_probe_data: dict[str, Any], baseline_data: dict[str, Any] | None) -> dict[str, Any]:
    existing_checks = deepcopy((baseline_data or {}).get("checks", {}))
    if not extra_probe_data.get("checks"):
        return existing_checks

    for check in extra_probe_data["checks"]:
        command = check["command"]
        result = run_command(command, timeout=check.get("timeout", 8), cwd=check.get("cwd"))
        capture = check.get("capture", "combined")
        output_text = result.get(capture, "") if capture in {"stdout", "stderr", "combined"} else result["combined"]
        success_patterns = check.get("success_patterns", [])
        matched_patterns = [pattern for pattern in success_patterns if re.search(pattern, output_text)]
        status = "passed"
        if result["status"] == "timeout":
            status = "timeout"
        elif result["status"] == "error":
            status = "error"
        elif success_patterns and len(matched_patterns) != len(success_patterns):
            status = "failed"
        elif result["exit_code"] not in (0, None) and not success_patterns:
            status = "failed"

        existing_checks[normalize_tool_id(check["id"])] = {
            "label": check.get("label", check["id"]),
            "command": command,
            "status": status,
            "exit_code": result["exit_code"],
            "matched_patterns": matched_patterns,
            "output_excerpt": trim_text(output_text),
        }

    return existing_checks


def compute_differences(
    baseline_data: dict[str, Any] | None,
    current_snapshot: dict[str, Any],
    scanned_tools: list[str],
) -> list[dict[str, Any]]:
    if not baseline_data:
        return []

    differences: list[dict[str, Any]] = []
    baseline_tools = baseline_data.get("tools", {})
    current_tools = current_snapshot.get("tools", {})
    for tool_id in scanned_tools:
        old = baseline_tools.get(tool_id)
        new = current_tools.get(tool_id)
        if not old and new:
            differences.append({"scope": "tool", "name": tool_id, "change": "added"})
            continue
        if not old or not new:
            continue
        for field in ["status", "selected_executable", "version"]:
            if old.get(field) != new.get(field):
                differences.append(
                    {
                        "scope": "tool",
                        "name": tool_id,
                        "field": field,
                        "before": old.get(field),
                        "after": new.get(field),
                    }
                )

    baseline_env = baseline_data.get("environment_variables", {})
    current_env = current_snapshot.get("environment_variables", {})
    for name, current_value in current_env.items():
        old_value = baseline_env.get(name, {})
        if old_value.get("value") != current_value.get("value"):
            differences.append(
                {
                    "scope": "env_var",
                    "name": name,
                    "before": old_value.get("value"),
                    "after": current_value.get("value"),
                }
            )

    return differences


def build_snapshot(args: argparse.Namespace) -> dict[str, Any]:
    baseline_path = choose_baseline_path(args)
    baseline_data = load_json(baseline_path)
    extra_probe_data = load_probe_file(args.probe_file)
    tool_specs = merge_tool_specs(extra_probe_data)
    requested_tool_ids = get_requested_tool_ids(args.tools, tool_specs, baseline_data)
    env_variables = collect_environment_variables(extra_probe_data, baseline_data)
    raw_env_values = {
        name: details["value"]
        for name, details in env_variables.items()
        if details["value"]
    }

    merged_tools = deepcopy((baseline_data or {}).get("tools", {}))
    for tool_id in requested_tool_ids:
        spec = deepcopy(tool_specs.get(tool_id, {"id": tool_id, "label": tool_id, "commands": [tool_id]}))
        spec["id"] = tool_id
        merged_tools[tool_id] = detect_tool(
            tool_id,
            spec,
            (baseline_data or {}).get("tools", {}).get(tool_id),
            raw_env_values,
        )

    document_language, detected_locale, locale_candidates, language_source = choose_document_language(args.lang)
    family = detect_os_family()
    snapshot = deepcopy(baseline_data or {})
    snapshot.update(
        {
            "schema_version": 1,
            "generated_at": utc_now(),
            "context": {
                "hostname": socket.gethostname(),
                "platform": platform.platform(),
                "platform_system": platform.system(),
                "os_family": family,
                "python_version": platform.python_version(),
                "cwd": canonicalize_path(os.getcwd()),
                "scan_mode": "targeted" if args.tools or args.probe_file else "full",
                "requested_tools": requested_tool_ids,
                "baseline_path": canonicalize_path(baseline_path),
                "probe_file": canonicalize_path(args.probe_file),
                "document_language": document_language,
                "detected_locale": detected_locale,
                "locale_candidates": locale_candidates,
                "document_language_source": language_source,
            },
            "tools": merged_tools,
            "environment_variables": env_variables,
        }
    )
    snapshot["path"] = build_path_summary(snapshot["tools"], env_variables, extra_probe_data)
    snapshot["checks"] = run_checks(extra_probe_data, baseline_data)
    snapshot["differences_from_baseline"] = compute_differences(
        baseline_data, snapshot, requested_tool_ids
    )
    return snapshot


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Detect local environment facts and optionally merge them into a baseline JSON."
    )
    parser.add_argument("--baseline", help="Existing baseline JSON to reuse as the source of truth.")
    parser.add_argument("--output", help="Write the merged snapshot to this JSON file.")
    parser.add_argument(
        "--tools",
        help="Comma-separated tool ids to verify. Defaults to the built-in full scan.",
    )
    parser.add_argument(
        "--probe-file",
        help="Optional JSON file that adds extra tools, env vars, path markers, or checks.",
    )
    parser.add_argument(
        "--lang",
        default="auto",
        help="Document language preference: auto, en, or zh.",
    )
    parser.add_argument(
        "--compact",
        action="store_true",
        help="Print compact JSON instead of indented JSON when writing to stdout.",
    )
    args = parser.parse_args()

    snapshot = build_snapshot(args)
    json_text = json.dumps(snapshot, ensure_ascii=False, indent=None if args.compact else 2)

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json_text + "\n", encoding="utf-8")
    else:
        sys.stdout.write(json_text + "\n")


if __name__ == "__main__":
    main()
