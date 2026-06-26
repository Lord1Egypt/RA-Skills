# -*- coding: utf-8 -*-
"""
ensure_ffmpeg.py — 自动检测并安装 ffmpeg / ffprobe。

用法:
  # 仅检测，输出安装计划 (JSON)
  python3 ensure_ffmpeg.py

  # 检测 + 自动安装
  python3 ensure_ffmpeg.py --execute

返回 JSON:
  status: "already_available" | "installable" | "installed" | "failed" | "blocked"
  ffmpeg_path / ffprobe_path: 可执行文件路径 (成功时)
  commands: 将要/已经执行的安装命令
  source_policy: 始终为 "package_manager_only"（不从 GitHub/npm 下载）

"""

import json
import os
import platform
import shutil
import subprocess
import sys


def print_json(payload, exit_code=0):
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    if exit_code:
        sys.exit(exit_code)


def has_command(name):
    return shutil.which(name) is not None


def as_command_text(command):
    if isinstance(command, dict):
        return " ".join(command["command"])
    return " ".join(command)


def run_command(command):
    return subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
    )


def linux_privilege_prefix():
    if os.name == "nt":
        return []
    if hasattr(os, "geteuid") and os.geteuid() == 0:
        return []
    if has_command("sudo"):
        return ["sudo"]
    return None


def get_rhel_major_version():
    if not has_command("rpm"):
        return None
    result = run_command(["rpm", "-E", "%rhel"])
    if result.returncode != 0:
        return None
    version = result.stdout.strip()
    return version or None


def dnf_yum_repo_fallback(package_manager, prefix):
    rhel_major = get_rhel_major_version()
    if not rhel_major:
        return None

    commands = [
        {
            "command": prefix + [package_manager, "install", "-y", "epel-release"],
            "optional": True,
        },
    ]

    if has_command(package_manager):
        commands.extend([
            {
                "command": prefix + [package_manager, "config-manager", "--set-enabled", "crb"],
                "optional": True,
            },
            {
                "command": prefix + [package_manager, "config-manager", "--set-enabled", "powertools"],
                "optional": True,
            },
        ])

    rpmfusion_url = (
        "https://mirrors.rpmfusion.org/free/el/"
        f"rpmfusion-free-release-{rhel_major}.noarch.rpm"
    )
    commands.append({
        "command": prefix + [package_manager, "install", "-y", rpmfusion_url],
        "optional": False,
    })
    commands.append({
        "command": prefix + [package_manager, "install", "-y", "ffmpeg"],
        "optional": False,
    })

    return {
        "reason": "ffmpeg_not_in_enabled_repos",
        "rhel_major": rhel_major,
        "commands": commands,
    }


def command_failed_for_missing_ffmpeg(result):
    text = "\n".join([result.stdout or "", result.stderr or ""]).lower()
    patterns = [
        "no match for argument: ffmpeg",
        "unable to find a match: ffmpeg",
        "no package ffmpeg available",
        "nothing provides ffmpeg",
    ]
    return any(pattern in text for pattern in patterns)


def build_install_plan():
    ffmpeg_path = shutil.which("ffmpeg")
    ffprobe_path = shutil.which("ffprobe")
    if ffmpeg_path and ffprobe_path:
        return {
            "status": "already_available",
            "platform": platform.system(),
            "ffmpeg_path": ffmpeg_path,
            "ffprobe_path": ffprobe_path,
            "source_policy": "package_manager_only",
        }

    system = platform.system()

    if system == "Darwin":
        if has_command("brew"):
            return {
                "status": "installable",
                "platform": system,
                "package_manager": "brew",
                "source_policy": "package_manager_only",
                "avoid": ["github-direct", "npm", "manual-zip-download"],
                "commands": [["brew", "install", "ffmpeg"]],
            }
        return {
            "status": "blocked",
            "platform": system,
            "reason": "homebrew_not_found",
            "message": (
                "No supported local package manager was found. "
                "Please install Homebrew first: https://brew.sh"
            ),
            "source_policy": "package_manager_only",
        }

    if system == "Windows":
        if has_command("winget"):
            return {
                "status": "installable",
                "platform": system,
                "package_manager": "winget",
                "source_policy": "package_manager_only",
                "avoid": ["github-direct", "npm", "manual-zip-download"],
                "commands": [[
                    "winget", "install", "--id", "Gyan.FFmpeg", "-e",
                    "--accept-source-agreements", "--accept-package-agreements",
                ]],
            }
        if has_command("choco"):
            return {
                "status": "installable",
                "platform": system,
                "package_manager": "choco",
                "source_policy": "package_manager_only",
                "avoid": ["github-direct", "npm", "manual-zip-download"],
                "commands": [["choco", "install", "ffmpeg", "-y"]],
            }
        return {
            "status": "blocked",
            "platform": system,
            "reason": "package_manager_not_found",
            "message": (
                "No supported Windows package manager was found. "
                "Please install winget or choco first."
            ),
            "source_policy": "package_manager_only",
        }

    # Linux
    prefix = linux_privilege_prefix()
    if has_command("apt-get") and prefix is not None:
        return {
            "status": "installable",
            "platform": system,
            "package_manager": "apt-get",
            "source_policy": "package_manager_only",
            "avoid": ["github-direct", "npm", "manual-zip-download"],
            "commands": [
                prefix + ["apt-get", "update"],
                prefix + ["apt-get", "install", "-y", "ffmpeg"],
            ],
        }
    if has_command("dnf") and prefix is not None:
        return {
            "status": "installable",
            "platform": system,
            "package_manager": "dnf",
            "source_policy": "package_manager_only",
            "avoid": ["github-direct", "npm", "manual-zip-download"],
            "commands": [prefix + ["dnf", "install", "-y", "ffmpeg"]],
            "repo_fallback": dnf_yum_repo_fallback("dnf", prefix),
        }
    if has_command("yum") and prefix is not None:
        return {
            "status": "installable",
            "platform": system,
            "package_manager": "yum",
            "source_policy": "package_manager_only",
            "avoid": ["github-direct", "npm", "manual-zip-download"],
            "commands": [prefix + ["yum", "install", "-y", "ffmpeg"]],
            "repo_fallback": dnf_yum_repo_fallback("yum", prefix),
        }
    if has_command("zypper") and prefix is not None:
        return {
            "status": "installable",
            "platform": system,
            "package_manager": "zypper",
            "source_policy": "package_manager_only",
            "avoid": ["github-direct", "npm", "manual-zip-download"],
            "commands": [prefix + ["zypper", "--non-interactive", "install", "ffmpeg"]],
        }

    return {
        "status": "blocked",
        "platform": system,
        "reason": "package_manager_not_found_or_no_privilege_path",
        "message": (
            "No supported package manager path is available for autonomous installation. "
            "Please install ffmpeg manually."
        ),
        "source_policy": "package_manager_only",
    }


def execute_step(command_spec, outputs):
    optional = False
    command = command_spec
    if isinstance(command_spec, dict):
        optional = command_spec.get("optional", False)
        command = command_spec["command"]

    result = run_command(command)
    outputs.append({
        "command": as_command_text(command_spec),
        "returncode": result.returncode,
        "stdout": result.stdout[-4000:],
        "stderr": result.stderr[-4000:],
        "optional": optional,
    })
    return result, optional


def execute_repo_fallback(plan, outputs):
    fallback = plan.get("repo_fallback")
    if not fallback:
        return None

    for command_spec in fallback.get("commands", []):
        result, optional = execute_step(command_spec, outputs)
        if result.returncode != 0 and not optional:
            return {
                "status": "failed",
                "platform": plan.get("platform"),
                "package_manager": plan.get("package_manager"),
                "source_policy": plan.get("source_policy"),
                "message": (
                    "Tried enabling EPEL / RPM Fusion automatically, "
                    "but ffmpeg is still unavailable."
                ),
                "repo_fallback_attempted": True,
                "repo_fallback_reason": fallback.get("reason"),
                "steps": outputs,
            }
    return None


def execute_plan(plan):
    steps = plan.get("commands", [])
    outputs = []
    for index, command in enumerate(steps):
        result, optional = execute_step(command, outputs)
        if result.returncode != 0:
            if (
                not optional
                and plan.get("package_manager") in {"dnf", "yum"}
                and index == len(steps) - 1
                and command_failed_for_missing_ffmpeg(result)
            ):
                fallback_result = execute_repo_fallback(plan, outputs)
                if fallback_result is not None:
                    return fallback_result
                break
            return {
                "status": "failed",
                "platform": plan.get("platform"),
                "package_manager": plan.get("package_manager"),
                "source_policy": plan.get("source_policy"),
                "repo_fallback_available": bool(plan.get("repo_fallback")),
                "steps": outputs,
            }

    ffmpeg_path = shutil.which("ffmpeg")
    ffprobe_path = shutil.which("ffprobe")
    if ffmpeg_path and ffprobe_path:
        return {
            "status": "installed",
            "platform": plan.get("platform"),
            "package_manager": plan.get("package_manager"),
            "source_policy": plan.get("source_policy"),
            "ffmpeg_path": ffmpeg_path,
            "ffprobe_path": ffprobe_path,
            "steps": outputs,
        }

    return {
        "status": "failed",
        "platform": plan.get("platform"),
        "package_manager": plan.get("package_manager"),
        "source_policy": plan.get("source_policy"),
        "message": "Installation commands finished but ffmpeg/ffprobe are still unavailable.",
        "repo_fallback_available": bool(plan.get("repo_fallback")),
        "steps": outputs,
    }


def main():
    execute = "--execute" in sys.argv[1:]

    plan = build_install_plan()
    if not execute:
        if plan.get("status") == "installable":
            plan["commands_text"] = [as_command_text(cmd) for cmd in plan["commands"]]
        print_json(plan, exit_code=0 if plan.get("status") != "blocked" else 1)
        return

    if plan.get("status") == "already_available":
        print_json(plan)
        return
    if plan.get("status") != "installable":
        print_json(plan, exit_code=1)
        return

    result = execute_plan(plan)
    print_json(result, exit_code=0 if result.get("status") == "installed" else 1)


if __name__ == "__main__":
    main()
