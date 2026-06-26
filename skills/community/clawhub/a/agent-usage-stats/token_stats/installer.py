"""Setup, update, and uninstall command flows."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys

from . import file_manager


def run_setup(project_root: str, install_dir_arg: str | None, scan_agent_paths, save_agent_paths):
    is_win = sys.platform == "win32"
    install_dir = file_manager.resolve_install_dir(install_dir_arg)
    bin_dir = file_manager.default_bin_dir(install_dir)

    print(f"🚀 正在安装 token-stats ({file_manager.platform_label()})")
    print(f"   安装目录: {install_dir}")
    print(f"   命令目录: {bin_dir}")

    copied = file_manager.copy_install_files(project_root, install_dir)
    script_path = file_manager.install_entry_script(install_dir)
    if not os.path.isfile(script_path):
        print(f"❌ 安装失败，未找到入口文件: {script_path}")
        print("   请确认当前目录是 token-stats/agent-usage-stats 源码目录，或重新通过 ClawHub 安装。")
        return
    if copied:
        print("✅ 运行文件已复制")
    else:
        print("✅ 安装目录已就绪")

    target = file_manager.write_command_wrapper(bin_dir, script_path)
    print(f"✅ 已创建全局命令: {target}")
    _migrate_legacy_wrapper(script_path)

    if is_win:
        legacy_path_result = file_manager.remove_from_path_windows(file_manager.legacy_bin_dir())
        if legacy_path_result.status == "removed":
            print(f"✅ 已清理旧版 PATH: {file_manager.legacy_bin_dir()}")
        path_result = file_manager.add_to_path_windows(bin_dir)
    else:
        _clean_unix_path_blocks_quiet()
        rc = file_manager.detect_rc_file()
        path_result = file_manager.add_to_path_unix(bin_dir, rc)
    _print_path_add_result(path_result, bin_dir)

    if not is_win:
        _warn_legacy_aliases()

    agent_paths = scan_agent_paths()
    if agent_paths:
        save_agent_paths(agent_paths)
        detected = []
        for key in agent_paths:
            label = key.replace("_dir", "").replace("_db", "").replace("_sessions", "")
            detected.append(label.capitalize())
        print(f"✅ 已自动检测并保存 Agent 路径: {', '.join(sorted(set(detected)))}")
    else:
        print("ℹ️  未检测到任何 Agent 数据文件，运行后会自动尝试标准路径")

    print()
    print("下一步:")
    print("  1. 打开一个新终端")
    print("  2. 运行: token-stats --version")


def run_uninstall(project_root: str, install_dir_arg: str | None, config_dir: str):
    is_win = sys.platform == "win32"
    install_dir = file_manager.resolve_install_dir(install_dir_arg)
    bin_dir = file_manager.default_bin_dir(install_dir)
    if _abort_if_current_dir_is_managed(project_root, install_dir, "卸载", include_install_dir=True):
        return

    removed, target = file_manager.remove_command_wrapper(bin_dir)
    legacy_removed, _ = file_manager.remove_command_wrapper(file_manager.legacy_bin_dir())
    removed.extend(legacy_removed)
    if removed:
        for item in removed:
            print(f"✅ 已删除: {item}")
    else:
        print(f"ℹ️  全局命令不存在: {target}")

    if is_win:
        path_results = [
            file_manager.remove_from_path_windows(bin_dir),
            file_manager.remove_from_path_windows(file_manager.legacy_bin_dir()),
        ]
    else:
        path_results = file_manager.remove_from_path_unix_all(bin_dir)
        path_results.extend(file_manager.remove_from_path_unix_all(file_manager.legacy_bin_dir()))
    _print_path_remove_result(path_results)

    if os.path.exists(config_dir):
        try:
            shutil.rmtree(config_dir)
            print(f"✅ 已清理配置文件: {config_dir}")
        except OSError as e:
            print(f"⚠️ 配置文件清理失败: {config_dir}")
            print(f"   原因: {e}")

    removed_dirs, skipped_dirs, failed_dirs = file_manager.remove_install_dirs(install_dir, project_root)
    if removed_dirs:
        for item in removed_dirs:
            print(f"✅ 已删除安装目录: {item}")
    elif not failed_dirs:
        print(f"ℹ️  安装目录不存在: {install_dir}")
    for item, error in failed_dirs:
        print(f"⚠️ 安装目录删除失败: {item}")
        print(f"   原因: {error}")
    for item in skipped_dirs:
        print(f"ℹ️  保留当前正在使用的源码目录: {item}")

    _print_uninstall_shell_hint()
    print()
    print("卸载完成。")


def run_update(project_root: str, version: str, install_dir_arg: str | None):
    print(f"⏳ 正在通过 ClawHub 更新 token-stats ({file_manager.platform_label()})...")
    install_dir = file_manager.resolve_install_dir(install_dir_arg)
    bin_dir = file_manager.default_bin_dir(install_dir)
    if _abort_if_current_dir_is_managed(project_root, install_dir, "更新", include_install_dir=False):
        return
    clawhub_exe = shutil.which("clawhub") or shutil.which("clawhub.cmd") or "clawhub"
    clawhub_cwd = os.path.expanduser("~")

    try:
        old_ver = version
        clawhub_paths = []
        print(f"   ClawHub 工作目录: {clawhub_cwd}")
        result = subprocess.run(
            [clawhub_exe, "update", "agent-usage-stats", "--no-input"],
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            timeout=120,
            cwd=clawhub_cwd,
        )
        output = result.stdout.decode("utf-8", errors="ignore").strip()
        if output:
            print(output)
            clawhub_paths.extend(file_manager.parse_clawhub_install_paths(output))

        if result.returncode != 0:
            print(f"⚠️ ClawHub 更新失败 (exit {result.returncode})，已保留当前版本。")
            _print_clawhub_recovery()
            return

        search_dirs = _update_search_dirs(project_root, install_dir, clawhub_paths)
        updated_src = _find_newer_source(search_dirs, old_ver)

        if updated_src is None:
            print("  ⏳ 常规更新未生效，尝试强制重装...")
            result2 = subprocess.run(
                [clawhub_exe, "install", "agent-usage-stats", "--force"],
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                timeout=120,
                cwd=clawhub_cwd,
            )
            out2 = result2.stdout.decode("utf-8", errors="ignore").strip()
            if out2:
                print(out2)
                clawhub_paths.extend(file_manager.parse_clawhub_install_paths(out2))
            if result2.returncode != 0:
                print(f"⚠️ ClawHub 强制重装失败 (exit {result2.returncode})，已保留当前版本。")
                _print_clawhub_recovery()
                return
            search_dirs = _update_search_dirs(project_root, install_dir, clawhub_paths)
            updated_src = _find_newer_source(search_dirs, old_ver)

        if updated_src:
            file_manager.copy_install_files(updated_src, install_dir)
            new_ver = file_manager.read_version(install_dir)
            if new_ver and new_ver != old_ver:
                _repair_command_and_path(bin_dir, install_dir)
                print(f"✅ 已更新到 v{new_ver}，请运行 token-stats --version 确认")
            else:
                _repair_command_and_path(bin_dir, install_dir)
                print(f"ℹ️ 当前已是 v{old_ver}，命令和 PATH 已检查。")
        else:
            new_ver = file_manager.read_version(install_dir)
            if new_ver and new_ver != old_ver:
                _repair_command_and_path(bin_dir, install_dir)
                print(f"✅ 已更新到 v{new_ver}，请运行 token-stats --version 确认")
            else:
                _repair_command_and_path(bin_dir, install_dir)
                print(f"ℹ️ 当前已是 v{old_ver}，命令和 PATH 已检查。")
    except FileNotFoundError:
        print("❌ 未找到 ClawHub CLI。")
        _print_clawhub_install_hint()
    except subprocess.TimeoutExpired:
        print("⚠️ ClawHub 更新超时，已保留当前版本。")
        print("   请检查网络后重试: token-stats update")
    except Exception as e:
        print(f"⚠️ 更新失败: {e}")
        _print_clawhub_recovery()


def _find_newer_source(search_dirs, old_ver: str):
    for item in search_dirs:
        ver = file_manager.read_version(item)
        if ver and _version_tuple(ver) > _version_tuple(old_ver):
            return item
    return None


def _update_search_dirs(project_root: str, install_dir: str, clawhub_paths: list[str]):
    dirs = []
    dirs.extend(clawhub_paths)
    dirs.extend(file_manager.find_update_sources(project_root, install_dir))
    seen = set()
    out = []
    for item in dirs:
        norm = os.path.normcase(os.path.abspath(os.path.expanduser(item)))
        if norm in seen:
            continue
        seen.add(norm)
        out.append(item)
    return out


def _abort_if_current_dir_is_managed(project_root: str, install_dir: str, action: str, *, include_install_dir: bool):
    managed_dir = file_manager.current_dir_inside(
        file_manager.maintenance_dirs(project_root, install_dir, include_install_dir=include_install_dir)
    )
    if not managed_dir:
        return False
    cwd = file_manager.safe_getcwd()
    print(f"❌ 为避免删除或覆盖当前目录，已停止{action}。")
    print(f"   当前目录: {cwd}")
    print(f"   受维护目录: {managed_dir}")
    print("   请先切换到其他目录后再重试，例如:")
    if sys.platform == "win32":
        print("     cd %USERPROFILE%")
    else:
        print("     cd ~")
    print(f"     token-stats {'--uninstall' if action == '卸载' else 'update'}")
    return True


def _version_tuple(value: str):
    parts = []
    for item in value.split("."):
        try:
            parts.append(int(item))
        except ValueError:
            parts.append(0)
    return tuple(parts)


def _remove_legacy_wrapper():
    removed, _ = file_manager.remove_command_wrapper(file_manager.legacy_bin_dir())
    for item in removed:
        print(f"✅ 已清理旧版全局命令: {item}")


def _migrate_legacy_wrapper(script_path: str):
    """Keep old shell command caches working during the update terminal session."""
    legacy_bin = file_manager.legacy_bin_dir()
    removed, legacy_target = file_manager.remove_command_wrapper(legacy_bin)
    if removed:
        target = file_manager.write_command_wrapper(legacy_bin, script_path)
        print(f"✅ 已迁移旧版全局命令: {legacy_target} -> {target}")
    return legacy_target


def _warn_legacy_aliases():
    rc = file_manager.detect_rc_file()
    rc_files = list(dict.fromkeys([rc, "~/.zshrc", "~/.bashrc", "~/.bash_profile"]))
    for rc_file in rc_files:
        rc_path = os.path.expanduser(rc_file)
        if not os.path.exists(rc_path):
            continue
        with open(rc_path, encoding="utf-8") as f:
            content = f.read()
        alias_lines = []
        for i, line in enumerate(content.splitlines(), 1):
            if "alias token-stats" in line.strip():
                alias_lines.append(f"  {rc_file} 第 {i} 行: {line.strip()}")
        if alias_lines:
            print()
            print("⚠️  检测到旧的 alias，会覆盖全局命令，建议删除：")
            for item in alias_lines:
                print(item)
            print("   删除方法: 手动编辑或用 sed 删除对应行，然后 source ~/.zshrc")


def _repair_command_and_path(bin_dir: str, install_dir: str):
    script_path = file_manager.install_entry_script(install_dir)
    if not os.path.isfile(script_path):
        print(f"⚠️ 未找到安装入口文件，无法修复命令: {script_path}")
        return
    target = file_manager.refresh_command_wrapper(bin_dir, install_dir)
    print(f"✅ 已检查全局命令: {target}")
    _migrate_legacy_wrapper(script_path)
    if sys.platform == "win32":
        legacy_path_result = file_manager.remove_from_path_windows(file_manager.legacy_bin_dir())
        if legacy_path_result.status == "removed":
            print(f"✅ 已清理旧版 PATH: {file_manager.legacy_bin_dir()}")
        path_result = file_manager.add_to_path_windows(bin_dir)
    else:
        _clean_unix_path_blocks_quiet()
        path_result = file_manager.add_to_path_unix(bin_dir, file_manager.detect_rc_file())
    _print_path_add_result(path_result, bin_dir)
    _print_current_shell_hint(bin_dir, target)


def _print_path_add_result(result, bin_dir: str):
    if result.status == "added":
        print(f"✅ 已添加到 PATH: {bin_dir}")
    elif result.status == "exists":
        print(f"✅ PATH 已包含命令目录: {bin_dir}")
    else:
        print(f"⚠️ PATH 自动写入失败: {result.target}")
        if result.error:
            print(f"   原因: {result.error}")
        _print_manual_path_hint(bin_dir)
    _print_wsl_hint()


def _print_path_remove_result(results):
    removed = [r.target for r in results if r.status == "removed"]
    failed = [r for r in results if r.status == "failed"]
    if removed:
        for item in removed:
            print(f"✅ 已清理 PATH 配置: {item}")
    else:
        print("ℹ️  未发现 token-stats PATH 配置")
    for item in failed:
        print(f"⚠️ PATH 配置清理失败: {item.target}")
        if item.error:
            print(f"   原因: {item.error}")


def _clean_unix_path_blocks_quiet():
    results = file_manager.remove_from_path_unix_all(file_manager.default_bin_dir())
    results.extend(file_manager.remove_from_path_unix_all(file_manager.legacy_bin_dir()))
    removed = [r.target for r in results if r.status == "removed"]
    for item in removed:
        print(f"✅ 已清理旧版 PATH 配置: {item}")


def _print_manual_path_hint(bin_dir: str):
    if sys.platform == "win32":
        print("   Windows 可手动添加用户 PATH:")
        print(f"     setx PATH \"%PATH%;{bin_dir}\"")
        print("   然后打开新的 PowerShell/CMD 再运行: token-stats --version")
        return
    shell = os.path.basename(os.environ.get("SHELL", ""))
    if shell == "fish":
        print("   fish 可手动执行:")
        print(f"     fish_add_path -p {bin_dir}")
    else:
        rc = file_manager.detect_rc_file()
        print("   可手动执行:")
        print(f"     echo 'export PATH=\"{bin_dir}:$PATH\"' >> {rc}")
        print(f"     source {rc}")


def _print_wsl_hint():
    if file_manager.is_wsl():
        print("ℹ️  当前运行在 WSL2/Linux 环境。此处只配置 WSL 内的 PATH；")
        print("   如果你也要在 Windows PowerShell/CMD 使用，请在 Windows 侧单独执行 setup。")


def _print_current_shell_hint(bin_dir: str, target: str):
    if not target:
        return
    current_path = os.environ.get("PATH", "")
    entries = [os.path.abspath(os.path.expanduser(p)) for p in current_path.split(os.pathsep) if p]
    bin_abs = os.path.abspath(os.path.expanduser(bin_dir))
    resolved = shutil.which("token-stats")
    if bin_abs in entries and resolved and os.path.abspath(resolved) == os.path.abspath(target):
        print("✅ 当前终端已可直接使用: token-stats --version")
        return
    print("ℹ️  当前终端可能仍在使用旧 PATH。请打开新终端后验证:")
    print("     which token-stats")
    print("     token-stats --version")
    if sys.platform != "win32":
        print("   如需当前终端立即生效，可执行:")
        print(f"     export PATH=\"{bin_dir}:$PATH\"")
        shell = os.path.basename(os.environ.get("SHELL", ""))
        if shell in {"zsh", "bash"}:
            print("     hash -r")


def _print_uninstall_shell_hint():
    if sys.platform == "win32":
        print("ℹ️  如果当前 PowerShell/CMD 仍能找到 token-stats，请打开新终端后再验证。")
        return
    print("ℹ️  如果当前终端仍缓存 token-stats 路径，请打开新终端后验证。")
    shell = os.path.basename(os.environ.get("SHELL", ""))
    if shell in {"zsh", "bash"}:
        print("   当前终端可执行: hash -r")


def _print_clawhub_install_hint():
    if sys.platform == "win32":
        print("   Windows 安装方式:")
        print("     npm install -g clawhub")
        print("     clawhub install agent-usage-stats")
        print("     python %USERPROFILE%\\skills\\agent-usage-stats\\token-stats.py setup")
    else:
        print("   macOS/Linux/WSL2 安装方式:")
        print("     npm install -g clawhub")
        print("     clawhub install agent-usage-stats")
        print("     python3 ~/skills/agent-usage-stats/token-stats.py setup")
    _print_wsl_hint()


def _print_clawhub_recovery():
    print("   可手动重试:")
    print("     clawhub update agent-usage-stats")
    print("     token-stats update")
    print("   如果仍失败，可强制重装 ClawHub 技能后重新 setup。")
