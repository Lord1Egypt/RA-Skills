"""Install/update/uninstall file management for token-stats."""

from __future__ import annotations

import os
import re
import shutil
import sys
from dataclasses import dataclass
from typing import Optional


DEFAULT_INSTALL_DIR = os.path.join(os.path.expanduser("~"), ".token-stats")
PATH_MARKER_START = "# >>> token-stats PATH >>>"
PATH_MARKER_END = "# <<< token-stats PATH <<<"
INSTALL_MANIFEST = (
    "token-stats.py",
    "token_stats",
    "model_prices.toml",
    "README.md",
    "README.zh.md",
    "CHANGELOG.md",
    "LICENSE",
    "SKILL.md",
)


@dataclass
class PathEditResult:
    status: str
    target: str
    error: str = ""

    @property
    def ok(self):
        return self.status in {"added", "exists", "removed", "absent"}


def resolve_install_dir(path: Optional[str] = None):
    return os.path.abspath(os.path.expanduser(path or DEFAULT_INSTALL_DIR))


def default_bin_dir(install_dir: Optional[str] = None):
    return os.path.join(resolve_install_dir(install_dir), "bin")


def legacy_bin_dir():
    return os.path.join(os.path.expanduser("~"), ".local", "bin")


def install_entry_script(install_dir: str):
    return os.path.join(resolve_install_dir(install_dir), "token-stats.py")


def legacy_install_dirs(project_root: str):
    home = os.path.expanduser("~")
    cwd = safe_getcwd()
    legacy_bin_parent = legacy_bin_dir()
    candidates = [
        os.path.join(home, "token-stats"),
        os.path.join(home, "skills", "agent-usage-stats"),
        os.path.join(home, ".clawhub", "skills", "agent-usage-stats"),
        os.path.join(cwd, "skills", "agent-usage-stats"),
        os.path.join(legacy_bin_parent, "skills", "agent-usage-stats"),
        os.path.join(project_root, "skills", "agent-usage-stats"),
    ]
    seen = set()
    out = []
    for item in candidates:
        norm = os.path.normcase(os.path.abspath(os.path.expanduser(item)))
        if norm not in seen:
            seen.add(norm)
            out.append(item)
    return out


def copy_install_files(src_dir: str, install_dir: str):
    """Copy runtime files into the fixed user install directory."""
    src_dir = os.path.abspath(os.path.expanduser(src_dir))
    install_dir = resolve_install_dir(install_dir)
    os.makedirs(install_dir, exist_ok=True)

    if _same_path(src_dir, install_dir):
        return 0

    copied = 0
    for name in INSTALL_MANIFEST:
        src = os.path.join(src_dir, name)
        dst = os.path.join(install_dir, name)
        if not os.path.exists(src):
            continue
        if os.path.isdir(src):
            ignore = shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store")
            if os.path.exists(dst):
                shutil.rmtree(dst)
            shutil.copytree(src, dst, ignore=ignore)
            copied += 1
        elif os.path.isfile(src):
            shutil.copy2(src, dst)
            copied += 1
    return copied


def write_command_wrapper(bin_dir: str, script_path: str):
    is_win = sys.platform == "win32"
    os.makedirs(bin_dir, exist_ok=True)
    if is_win:
        target = os.path.join(bin_dir, "token-stats.cmd")
        wrapper = f'@python "{script_path}" %*\n'
    else:
        target = os.path.join(bin_dir, "token-stats")
        wrapper = "#!/bin/sh\n" f'exec python3 "{script_path}" "$@"\n'
    with open(target, "w", encoding="utf-8") as f:
        f.write(wrapper)
    if not is_win:
        os.chmod(target, 0o755)
    return target


def refresh_command_wrapper(bin_dir: str, install_dir: str):
    return write_command_wrapper(bin_dir, install_entry_script(install_dir))


def remove_command_wrapper(bin_dir: str):
    if sys.platform == "win32":
        targets = [os.path.join(bin_dir, "token-stats.cmd")]
    else:
        targets = [os.path.join(bin_dir, "token-stats")]
    removed = []
    for target in targets:
        if os.path.lexists(target):
            os.remove(target)
            removed.append(target)
    return removed, targets[0]


def detect_rc_file():
    """Detect the current user's shell startup file."""
    shell = os.environ.get("SHELL", "")
    shell_name = os.path.basename(shell)
    if shell_name == "zsh":
        return "~/.zshrc"
    if shell_name == "bash":
        return "~/.bashrc"
    if shell_name == "fish":
        return "~/.config/fish/config.fish"
    for rc in ["~/.zshrc", "~/.bashrc", "~/.bash_profile", "~/.profile"]:
        if os.path.exists(os.path.expanduser(rc)):
            return rc
    return "~/.bashrc"


def rc_files_for_cleanup():
    """Return shell startup files that may contain token-stats PATH blocks."""
    candidates = [
        detect_rc_file(),
        "~/.zshrc",
        "~/.bashrc",
        "~/.bash_profile",
        "~/.profile",
        "~/.config/fish/config.fish",
    ]
    seen = set()
    out = []
    for item in candidates:
        path = os.path.abspath(os.path.expanduser(item))
        if path not in seen:
            seen.add(path)
            out.append(item)
    return out


def is_wsl():
    if sys.platform != "linux":
        return False
    try:
        with open("/proc/version", encoding="utf-8") as f:
            return "microsoft" in f.read().lower()
    except OSError:
        return False


def platform_label():
    if sys.platform == "win32":
        return "Windows"
    if sys.platform == "darwin":
        return "macOS"
    if is_wsl():
        return "WSL2/Linux"
    if sys.platform.startswith("linux"):
        return "Linux"
    return sys.platform


def add_to_path_windows(bin_dir):
    """Add a directory to the user's Windows PATH."""
    import ctypes
    import winreg

    bin_dir = os.path.normpath(bin_dir)
    key = None
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment", 0, winreg.KEY_READ | winreg.KEY_WRITE)
        try:
            current, _ = winreg.QueryValueEx(key, "PATH")
        except FileNotFoundError:
            current = ""
        entries = [os.path.normpath(e) for e in current.split(";") if e]
        if bin_dir.lower() in (e.lower() for e in entries):
            return PathEditResult("exists", bin_dir)
        entries.insert(0, bin_dir)
        winreg.SetValueEx(key, "PATH", 0, winreg.REG_EXPAND_SZ, ";".join(entries))
        ctypes.windll.user32.SendMessageTimeoutW(0xFFFF, 0x001A, 0, "Environment", 2, 5000, None)
        return PathEditResult("added", bin_dir)
    except Exception as e:
        return PathEditResult("failed", bin_dir, str(e))
    finally:
        if key is not None:
            winreg.CloseKey(key)


def remove_from_path_windows(bin_dir):
    """Remove a directory from the user's Windows PATH."""
    import ctypes
    import winreg

    bin_dir = os.path.normpath(bin_dir)
    key = None
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment", 0, winreg.KEY_READ | winreg.KEY_WRITE)
        try:
            current, _ = winreg.QueryValueEx(key, "PATH")
        except FileNotFoundError:
            return PathEditResult("absent", bin_dir)
        entries = [e for e in current.split(";") if e and os.path.normpath(e).lower() != bin_dir.lower()]
        if len(entries) == len([e for e in current.split(";") if e]):
            return PathEditResult("absent", bin_dir)
        winreg.SetValueEx(key, "PATH", 0, winreg.REG_EXPAND_SZ, ";".join(entries))
        ctypes.windll.user32.SendMessageTimeoutW(0xFFFF, 0x001A, 0, "Environment", 2, 5000, None)
        return PathEditResult("removed", bin_dir)
    except Exception as e:
        return PathEditResult("failed", bin_dir, str(e))
    finally:
        if key is not None:
            winreg.CloseKey(key)


def add_to_path_unix(bin_dir, rc_file):
    """Append a marked PATH block to a shell startup file if missing."""
    rc_path = os.path.expanduser(rc_file)
    is_fish = rc_file.endswith(".fish") or "fish" in rc_file
    export_line = f"fish_add_path -p {bin_dir}" if is_fish else f'export PATH="{bin_dir}:$PATH"'
    block = f"\n{PATH_MARKER_START}\n{export_line}\n{PATH_MARKER_END}\n"
    try:
        content = ""
        if os.path.exists(rc_path):
            with open(rc_path, "r", encoding="utf-8") as f:
                content = f.read()
                if block.strip() in content:
                    return PathEditResult("exists", rc_path)
        content = _remove_token_stats_path_blocks(content)
        rc_dir = os.path.dirname(rc_path)
        if rc_dir:
            os.makedirs(rc_dir, exist_ok=True)
        with open(rc_path, "w", encoding="utf-8") as f:
            f.write(content.rstrip("\n"))
            f.write(block)
        return PathEditResult("added", rc_path)
    except Exception as e:
        return PathEditResult("failed", rc_path, str(e))


def remove_from_path_unix(bin_dir, rc_file):
    """Remove token-stats marked PATH blocks from a shell startup file."""
    rc_path = os.path.expanduser(rc_file)
    if not os.path.exists(rc_path):
        return PathEditResult("absent", rc_path)
    try:
        with open(rc_path, "r", encoding="utf-8") as f:
            content = f.read()
        new_content = _remove_token_stats_path_blocks(content)
        if new_content == content:
            return PathEditResult("absent", rc_path)
        with open(rc_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        return PathEditResult("removed", rc_path)
    except Exception as e:
        return PathEditResult("failed", rc_path, str(e))


def remove_from_path_unix_all(bin_dir):
    results = []
    for rc_file in rc_files_for_cleanup():
        results.append(remove_from_path_unix(bin_dir, rc_file))
    return results


def read_version(path):
    """Read VERSION from both the new package layout and old single-file layout."""
    try:
        candidates = [
            os.path.join(path, "token_stats", "app.py"),
            os.path.join(path, "token-stats.py"),
        ]
        for fpath in candidates:
            if not os.path.isfile(fpath):
                continue
            with open(fpath, encoding="utf-8") as f:
                for line in f:
                    if line.startswith('VERSION = "'):
                        return line.split('"')[1]
    except Exception:
        pass
    return None


def find_update_sources(project_root: str, install_dir: str):
    candidates = [project_root, resolve_install_dir(install_dir)]
    candidates.extend(legacy_install_dirs(project_root))
    seen = set()
    out = []
    for item in candidates:
        norm = os.path.normcase(os.path.abspath(os.path.expanduser(item)))
        if norm in seen:
            continue
        seen.add(norm)
        out.append(item)
    return out


def parse_clawhub_install_paths(output: str):
    """Extract skill install directories printed by ClawHub."""
    paths = []
    if not output:
        return paths
    patterns = [
        r"Installed\s+agent-usage-stats\s+->\s+(.+)",
        r"agent-usage-stats:\s+updated\s+->\s+(.+)",
    ]
    for line in output.splitlines():
        for pattern in patterns:
            match = re.search(pattern, line)
            if not match:
                continue
            value = match.group(1).strip().strip("\"'")
            if not value or re.fullmatch(r"\d+(?:\.\d+)*", value):
                continue
            paths.append(os.path.abspath(os.path.expanduser(value)))
    return paths


def maintenance_dirs(project_root: str, install_dir: str, *, include_install_dir: bool = True):
    candidates = []
    if include_install_dir:
        candidates.append(resolve_install_dir(install_dir))
    candidates.extend(legacy_install_dirs(project_root))
    seen = set()
    out = []
    for item in candidates:
        path = os.path.abspath(os.path.expanduser(item))
        norm = os.path.normcase(path)
        if norm in seen:
            continue
        seen.add(norm)
        out.append(path)
    return out


def current_dir_inside(paths):
    cwd = os.path.abspath(safe_getcwd())
    for item in paths:
        path = os.path.abspath(os.path.expanduser(item))
        if _same_or_child(cwd, path):
            return path
    skill_dir = _skill_dir_from_path(cwd)
    if skill_dir:
        return skill_dir
    return None


def remove_install_dirs(install_dir: str, project_root: str):
    """Remove the active install dir and legacy ClawHub/source install dirs."""
    cwd = safe_getcwd()
    removed = []
    skipped = []
    failed = []
    install_path = os.path.abspath(os.path.expanduser(resolve_install_dir(install_dir)))
    project_path = os.path.abspath(os.path.expanduser(project_root))
    protected_paths = {os.path.normcase(os.path.abspath(cwd)), os.path.normcase(project_path)}
    if os.path.exists(install_path):
        if _same_path(install_path, cwd):
            skipped.append(install_path)
        else:
            try:
                shutil.rmtree(install_path)
                removed.append(install_path)
            except OSError as e:
                failed.append((install_path, str(e)))
    for item in legacy_install_dirs(project_root):
        path = os.path.abspath(os.path.expanduser(item))
        norm = os.path.normcase(path)
        if not os.path.exists(path) or _same_path(path, install_path):
            continue
        if norm in protected_paths:
            skipped.append(path)
            continue
        try:
            shutil.rmtree(path)
            removed.append(path)
        except OSError as e:
            failed.append((path, str(e)))
    return removed, skipped, failed


def _same_path(a: str, b: str):
    return os.path.normcase(os.path.normpath(os.path.realpath(a))) == os.path.normcase(os.path.normpath(os.path.realpath(b)))


def safe_getcwd():
    try:
        return os.getcwd()
    except FileNotFoundError:
        return os.environ.get("PWD") or os.path.expanduser("~")


def _same_or_child(path: str, parent: str):
    path = os.path.normcase(os.path.normpath(os.path.realpath(path)))
    parent = os.path.normcase(os.path.normpath(os.path.realpath(parent)))
    return path == parent or path.startswith(parent + os.sep)


def _skill_dir_from_path(path: str):
    path = os.path.abspath(path)
    parts = path.split(os.sep)
    for i in range(len(parts) - 1):
        if parts[i] == "skills" and parts[i + 1] == "agent-usage-stats":
            return os.sep.join(parts[: i + 2]) or os.sep
    return None


def _remove_token_stats_path_blocks(content: str):
    pattern = re.compile(
        rf"\n?{re.escape(PATH_MARKER_START)}\n.*?\n{re.escape(PATH_MARKER_END)}\n?",
        re.DOTALL,
    )
    return pattern.sub("\n", content).lstrip("\n")
