#!/usr/bin/env python3
# /// script
# dependencies = []
# ///
"""
Cross-Platform Environment Check Script
Checks Python version and dependencies, supports Windows/Linux/macOS
Outputs JSON results for AI parsing
"""

import json
import os
import platform
import subprocess
import sys
from pathlib import Path
from typing import Any

# aaPanel minimum version requirement
MIN_PANEL_VERSION = "9.0.0"

# global config path
GLOBAL_CONFIG_PATH = Path.home() / ".openclaw" / "bt-skills.yaml"


def get_platform_info() -> dict:
    """Get platform info"""
    system = platform.system()
    return {
        "system": system,
        "system_lower": system.lower(),
        "machine": platform.machine(),
        "python_version": platform.python_version(),
        "python_implementation": platform.python_implementation(),
        "is_windows": system == "Windows",
        "is_linux": system == "Linux",
        "is_macos": system == "Darwin",
    }


def check_python_version() -> dict:
    """Check Python version"""
    version = sys.version_info
    required_major = 3
    required_minor = 10

    is_valid = version.major > required_major or (
        version.major == required_major and version.minor >= required_minor
    )

    return {
        "version": f"{version.major}.{version.minor}.{version.micro}",
        "required": f"{required_major}.{required_minor}+",
        "is_valid": is_valid,
        "message": (
            f"Python version {'meets requirements' if is_valid else 'does not meet requirements'}: "
            f"current {version.major}.{version.minor}.{version.micro}, requires {required_major}.{required_minor}+"
        ),
    }


def check_module(module_name: str, import_name: str = None) -> dict:
    """Check individual module"""
    import_name = import_name or module_name
    try:
        module = __import__(import_name)
        version = getattr(module, "__version__", "unknown")
        return {
            "name": module_name,
            "installed": True,
            "version": version,
            "message": f"✓ {module_name} ({version})",
        }
    except ImportError:
        return {
            "name": module_name,
            "installed": False,
            "version": None,
            "message": f"✗ {module_name} not installed",
        }


def check_dependencies() -> dict:
    """Check dependencies"""
    required_modules = [
        ("requests", "requests"),
        ("pyyaml", "yaml"),
        ("rich", "rich"),
    ]

    optional_modules = [
        ("pytest", "pytest"),
    ]

    required_results = []
    required_passed = True

    for module_name, import_name in required_modules:
        result = check_module(module_name, import_name)
        required_results.append(result)
        if not result["installed"]:
            required_passed = False

    optional_results = []
    for module_name, import_name in optional_modules:
        optional_results.append(check_module(module_name, import_name))

    return {
        "required": required_results,
        "required_passed": required_passed,
        "optional": optional_results,
    }


def find_python_executable() -> dict:
    """Find available Python executable"""
    candidates = ["python3", "python", "py"]
    found = []
    preferred = None

    for cmd in candidates:
        try:
            result = subprocess.run(
                [cmd, "--version"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            if result.returncode == 0:
                version_str = result.stdout.strip() or result.stderr.strip()
                found.append(
                    {
                        "command": cmd,
                        "version": version_str,
                        "path": find_executable_path(cmd),
                    }
                )
                if preferred is None and "3." in version_str:
                    preferred = cmd
        except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
            continue

    # Current Python takes priority
    current = sys.executable

    return {
        "current": current,
        "preferred": preferred or sys.executable,
        "all_found": found,
    }


def find_executable_path(cmd: str) -> str:
    """Find executable file path"""
    try:
        result = subprocess.run(
            ["which" if platform.system() != "Windows" else "where", cmd],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode == 0:
            return result.stdout.strip().split("\n")[0]
    except Exception:
        pass
    return "unknown"


def check_config_file() -> dict:
    """Check config file"""
    project_root = Path(__file__).parent.parent
    config_path = project_root / "config"

    results = {
        "global_config_path": str(GLOBAL_CONFIG_PATH),
        "global_config_exists": GLOBAL_CONFIG_PATH.exists(),
        "local_config_dir_exists": config_path.exists(),
        "local_config_exists": (config_path / "servers.local.yaml").exists(),
        "example_config_exists": (config_path / "servers.yaml").exists() or (config_path / "servers.yaml.example").exists(),
        "env_var_set": "BT_CONFIG_PATH" in os.environ,
        "env_var_value": os.environ.get("BT_CONFIG_PATH"),
    }

    # Config ready: global config exists or local config exists or env var set
    results["config_ready"] = (
        results["global_config_exists"]
        or results["local_config_exists"]
        or results["env_var_set"]
    )

    if results["config_ready"]:
        results["message"] = "Config file ready"
        # Point to active config path
        if results["env_var_set"]:
            results["active_config"] = results["env_var_value"]
        elif results["global_config_exists"]:
            results["active_config"] = str(GLOBAL_CONFIG_PATH)
        else:
            results["active_config"] = str(config_path / "servers.local.yaml")
    else:
        results["message"] = f"Need to create config file: {GLOBAL_CONFIG_PATH} or config/servers.local.yaml"
        results["active_config"] = None

    return results


def check_skills_directory() -> dict:
    """Check skills directory structure"""
    project_root = Path(__file__).parent.parent
    skills_dir = project_root / "skills"

    required_skills = [
        "bt_common",
        "bt-system-monitor",
        "bt-security-check",
        "bt-health-check",
    ]

    results = {
        "skills_dir_exists": skills_dir.exists(),
        "skills": {},
    }

    for skill in required_skills:
        skill_path = skills_dir / skill
        results["skills"][skill] = {
            "exists": skill_path.exists(),
            "has_skill_md": (skill_path / "SKILL.md").exists() if skill != "bt_common" else None,
            "has_scripts": (skill_path / "scripts").exists() if skill != "bt_common" else None,
        }

    results["all_skills_present"] = all(
        results["skills"][s]["exists"] for s in required_skills
    )

    return results


def get_install_commands() -> dict:
    """Get install commands"""
    system = platform.system()

    commands = {
        "pip_install": "pip install -r requirements.txt",
        "pip_install_user": "pip install --user -r requirements.txt",
    }

    if system == "Windows":
        commands.update({
            "winget_python": "winget install Python.Python.3.12",
            "choco_python": "choco install python",
        })
    elif system == "Linux":
        commands.update({
            "apt": "sudo apt install python3 python3-pip python3-yaml python3-requests",
            "dnf": "sudo dnf install python3 python3-pip python3-pyyaml python3-requests",
            "pacman": "sudo pacman -S python python-pip python-yaml python-requests",
        })
    elif system == "Darwin":
        commands.update({
            "brew": "brew install python3 pyyaml",
        })

    return commands


def run_full_check() -> dict:
    """Run full check"""
    platform_info = get_platform_info()
    python_check = check_python_version()
    deps_check = check_dependencies()
    python_exe = find_python_executable()
    config_check = check_config_file()
    skills_check = check_skills_directory()
    install_cmds = get_install_commands()

    # Calculate overall status
    all_passed = (
        python_check["is_valid"]
        and deps_check["required_passed"]
        and config_check["config_ready"]
        and skills_check["all_skills_present"]
    )

    return {
        "status": "passed" if all_passed else "failed",
        "passed": all_passed,
        "min_panel_version": MIN_PANEL_VERSION,
        "platform": platform_info,
        "python": python_check,
        "python_executable": python_exe,
        "dependencies": deps_check,
        "config": config_check,
        "skills": skills_check,
        "install_commands": install_cmds,
        "summary": generate_summary(
            python_check, deps_check, config_check, skills_check, all_passed
        ),
    }


def generate_summary(python, deps, config, skills, all_passed) -> dict:
    """Generate summary"""
    issues = []
    suggestions = []

    if not python["is_valid"]:
        issues.append(f"Python version too low: {python['version']}, requires {python['required']}")
        suggestions.append("Please upgrade Python to 3.10 or higher")

    for dep in deps["required"]:
        if not dep["installed"]:
            issues.append(f"Missing dependency: {dep['name']}")
            suggestions.append(f"Run: pip install {dep['name']}")

    if not config["config_ready"]:
        issues.append("Config file not ready")
        suggestions.append(f"Create global config: {GLOBAL_CONFIG_PATH}")
        suggestions.append("Or create local config: config/servers.local.yaml")

    for skill_name, skill_info in skills["skills"].items():
        if not skill_info["exists"]:
            issues.append(f"Missing skills directory: {skill_name}")

    return {
        "is_ready": all_passed,
        "issues": issues,
        "suggestions": suggestions,
        "min_panel_version": MIN_PANEL_VERSION,
        "message": "Environment check passed, ready to use" if all_passed else "Environment has issues, please fix according to hints",
    }


def print_human_readable(result: dict):
    """Print human-readable output"""
    print("=" * 60)
    print("aaPanel Log Inspection Skills Package - Environment Check")
    print("=" * 60)
    print()

    # Platform info
    print(f"🖥️  OS: {result['platform']['system']} ({result['platform']['machine']})")
    print(f"🐍 Python: {result['python']['version']}")
    print(f"   Status: {'✅ ' + result['python']['message'] if result['python']['is_valid'] else '❌ ' + result['python']['message']}")
    print(f"📋 aaPanel version requirement: >= {result.get('min_panel_version', MIN_PANEL_VERSION)}")
    print()

    # Dependencies check
    print("📦 Dependencies check:")
    for dep in result["dependencies"]["required"]:
        status = "✅" if dep["installed"] else "❌"
        print(f"   {status} {dep['name']}: {dep['version'] or 'Not installed'}")
    print()

    # Config check
    print("⚙️  Config check:")
    print(f"   Global config path: {result['config']['global_config_path']}")
    if result["config"]["global_config_exists"]:
        print("   ✅ Global config exists")
    elif result["config"]["config_ready"]:
        print(f"   ✅ Config file ready: {result['config'].get('active_config', 'Unknown')}")
    else:
        print("   ❌ Config file not ready")
        print(f"   Hint: {result['config']['message']}")
    print()

    # Skills check
    print("📁 Skills directory:")
    for skill_name, skill_info in result["skills"]["skills"].items():
        status = "✅" if skill_info["exists"] else "❌"
        print(f"   {status} {skill_name}")
    print()

    # Summary
    print("=" * 60)
    if result["passed"]:
        print("✅ Environment check passed, ready to use!")
    else:
        print("❌ Environment check failed, please fix the following issues:")
        for issue in result["summary"]["issues"]:
            print(f"   - {issue}")
        print()
        print("💡 Suggestions:")
        for suggestion in result["summary"]["suggestions"]:
            print(f"   - {suggestion}")
    print("=" * 60)


def main():
    """Main function"""
    import argparse

    parser = argparse.ArgumentParser(
        description="aaPanel Log Inspection Skills Package - Environment Check",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--format", "-f",
        choices=["json", "text"],
        default="text",
        help="Output format (json/text)",
    )
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Quiet mode, only output result status",
    )

    args = parser.parse_args()

    result = run_full_check()

    if args.quiet:
        print("passed" if result["passed"] else "failed")
        sys.exit(0 if result["passed"] else 1)

    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print_human_readable(result)

    sys.exit(0 if result["passed"] else 1)


if __name__ == "__main__":
    main()
