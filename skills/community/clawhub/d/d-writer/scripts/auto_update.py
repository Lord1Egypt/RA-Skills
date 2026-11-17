#!/usr/bin/env python3
"""Skill 自动更新检查器。

功能：
1. 读取本地 _meta.json 中的版本号
2. 从 skillhub API 获取远程最新版本
3. 对比版本（支持语义化版本 x.y.z）
4. 如果本地版本 < 远程版本，执行更新
5. 任何错误均跳过（skip_on_error=true），不中断 skill 运行

使用方式：
- 启动期检查（仅当 _meta.json 中 auto_check=true 时联网）：python scripts/auto_update.py check
- 查看版本状态（不下载）：python scripts/auto_update.py status --verbose
- 强制触发更新检查（覆盖 auto_check=false）：python scripts/auto_update.py check --force

退出码：
- 0 = 无需更新 / 更新成功 / 错误已跳过
- 1 = 发生错误且 skip_on_error=false
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

SKILL_ROOT = Path(__file__).resolve().parent.parent
META_PATH = SKILL_ROOT / "_meta.json"

# 直接下载地址模板：skillhub 官方下载端点（匿名可访问，返回含全部技能文件的 zip）。
# 注意：不是旧版硬编码的 COS 桶地址（已 404）。
DIRECT_DOWNLOAD_URL_TEMPLATE = "https://api.skillhub.cn/api/v1/download?slug={slug}"


def load_meta() -> Dict[str, Any]:
    """加载本地 _meta.json。"""
    if not META_PATH.exists():
        return {}
    try:
        with open(META_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, dict) else {}
    except (json.JSONDecodeError, OSError):
        return {}


def parse_version(v: str) -> Optional[Tuple[int, ...]]:
    """解析语义化版本字符串为元组，如 '2.0.2' -> (2, 0, 2)。"""
    if not v:
        return None
    raw = v.strip().lower()
    if raw.startswith("v"):
        raw = raw[1:]
    if not raw:
        return None
    core = raw.split("-", 1)[0].split("+", 1)[0]
    parts = core.split(".")
    out = []
    for part in parts:
        if not part.isdigit():
            return None
        out.append(int(part))
    return tuple(out) if out else None


def version_is_newer(candidate: str, current: str) -> bool:
    """判断 candidate 是否比 current 新。"""
    candidate = candidate.strip()
    current = current.strip()
    if not candidate:
        return False
    if not current:
        return True  # 无本地版本号 -> 需要更新
    a = parse_version(candidate)
    b = parse_version(current)
    if a is not None and b is not None:
        return a > b
    return candidate != current


def fetch_remote_version(meta: Dict[str, Any]) -> Optional[str]:
    """从 skillhub API 获取远程最新版本号。"""
    check_url = meta.get("update", {}).get("check_url", "")
    if not check_url:
        return None

    slug = meta.get("slug", "d-writer")
    req = urllib.request.Request(
        check_url,
        headers={
            "User-Agent": "dragon-writer-skill-updater/1.0",
            "Accept": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            payload = response.read().decode("utf-8")
            data = json.loads(payload)
    except (urllib.error.URLError, urllib.error.HTTPError, json.JSONDecodeError, OSError):
        return None

    results = data.get("results", [])
    if not isinstance(results, list):
        return None

    for r in results:
        if not isinstance(r, dict):
            continue
        if r.get("slug") == slug:
            version = r.get("version")
            if isinstance(version, str) and version.strip():
                return version.strip()
    return None


def perform_update(meta: Dict[str, Any], remote_version: str) -> bool:
    """执行 skill 更新。优先使用 skillhub CLI，回退到直接下载 zip。"""
    slug = meta.get("slug", "d-writer")
    install_dir = SKILL_ROOT

    # 方案 1：尝试使用 skillhub CLI
    if _try_skillhub_cli_upgrade(slug, install_dir, remote_version):
        return True

    # 方案 2：直接下载 zip
    return _try_direct_download(slug, install_dir, remote_version)


def _try_skillhub_cli_upgrade(slug: str, install_dir: Path, remote_version: str) -> bool:
    """尝试使用 skillhub CLI 执行升级。"""
    skillhub_bin = shutil.which("skillhub")
    if not skillhub_bin:
        # 尝试默认路径
        default_path = Path.home() / ".local" / "bin" / "skillhub"
        if default_path.exists():
            skillhub_bin = str(default_path)
    if not skillhub_bin:
        return False

    try:
        # 先尝试 skillhub upgrade 命令。
        # 注意：CLI 的 upgrade 子命令不接受 --force（只支持 --check-only/--timeout/--dir），
        # 传 --force 会报 "unrecognized arguments" 导致每次都失败。
        result = subprocess.run(
            [skillhub_bin, "upgrade", slug, "--dir", str(install_dir)],
            capture_output=True,
            text=True,
            timeout=60,
        )
        if result.returncode == 0:
            return True
    except (subprocess.TimeoutExpired, OSError):
        pass

    # 回退：使用 skillhub install
    try:
        result = subprocess.run(
            [skillhub_bin, "install", slug, "--dir", str(install_dir), "--force"],
            capture_output=True,
            text=True,
            timeout=60,
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, OSError):
        return False


def _try_direct_download(slug: str, install_dir: Path, remote_version: str) -> bool:
    """直接下载 skill zip 并解压到安装目录。

    下载地址用 skillhub 官方端点（DIRECT_DOWNLOAD_URL_TEMPLATE）：
    旧版硬编码的 COS 桶地址（...myqcloud.com/skills/{slug}.zip）已返回 404，
    导致无 skillhub CLI 的环境下更新必然失败。
    """
    download_url = DIRECT_DOWNLOAD_URL_TEMPLATE.replace(
        "{slug}", urllib.parse.quote(slug)
    )

    try:
        with tempfile.TemporaryDirectory(prefix="d-writer-update-") as tmp:
            zip_path = Path(tmp) / f"{slug}.zip"
            stage_dir = Path(tmp) / "stage"
            stage_dir.mkdir(parents=True, exist_ok=True)

            # 下载
            req = urllib.request.Request(
                download_url,
                headers={"User-Agent": "dragon-writer-skill-updater/1.0"},
            )
            with urllib.request.urlopen(req, timeout=30) as response:
                with open(zip_path, "wb") as f:
                    f.write(response.read())

            # 解压
            with zipfile.ZipFile(zip_path, "r") as zf:
                zf.extractall(stage_dir)

            # 移动到安装目录（保留 _meta.json 中的本地配置）
            _merge_update(stage_dir, install_dir)

        return True
    except Exception:
        return False


def _merge_update(source: Path, target: Path) -> None:
    """将下载的更新合并到安装目录，保留本地配置文件。"""
    # 保留不被覆盖的本地文件（todo / dashboard-todo 已移除，仅保留本地更新配置）
    preserved = {"_meta.json"}
    for item in source.iterdir():
        dest = target / item.name
        if item.name in preserved and dest.exists():
            # 更新 _meta.json 的版本号，其余保留
            if item.name == "_meta.json":
                try:
                    new_meta = json.loads(item.read_text(encoding="utf-8"))
                    old_meta = json.loads(dest.read_text(encoding="utf-8"))
                    # 保留本地 update 配置
                    if "update" in old_meta:
                        new_meta["update"] = old_meta["update"]
                    dest.write_text(json.dumps(new_meta, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
                except Exception:
                    pass
            continue
        # 移动文件/目录
        if dest.exists():
            if dest.is_dir():
                shutil.rmtree(dest)
            else:
                dest.unlink()
        shutil.move(str(item), str(dest))


def _git_uncommitted(install_dir: Path) -> bool:
    """检测 install_dir 是否位于 git 工作树且有未提交改动。

    用于就地覆盖保护：自动更新会覆盖目录内全部文件（仅保留 _meta.json），
    若该目录是 git 工作树且存在未提交改动，应跳过覆盖以免抹掉源码工作。
    非 git 目录 / 命令不可用一律返回 False（不阻断）。
    """
    try:
        r = subprocess.run(
            ["git", "-C", str(install_dir), "status", "--porcelain"],
            capture_output=True,
            text=True,
            timeout=15,
        )
    except (OSError, subprocess.TimeoutExpired):
        return False
    if r.returncode != 0:
        return False  # 不在 git 仓库
    return bool(r.stdout.strip())


def update_local_version(meta: Dict[str, Any], new_version: str) -> None:
    """更新本地 _meta.json 中的版本号。"""
    meta["version"] = new_version
    try:
        with open(META_PATH, "w", encoding="utf-8") as f:
            json.dump(meta, f, indent=2, ensure_ascii=False)
            f.write("\n")
    except OSError:
        pass


def cmd_check(args: argparse.Namespace) -> int:
    """检查更新，如果需要则执行更新。"""
    meta = load_meta()

    if not meta:
        if args.verbose:
            print("[update] 未找到 _meta.json，跳过更新检查")
        return 0

    update_config = meta.get("update", {})
    if not update_config.get("enabled", True):
        if args.verbose:
            print("[update] 自动更新已禁用")
        return 0

    # auto_check=false 时，启动期 check 静默跳过，避免联网覆盖本地未提交工作；
    # 用 --force 显式触发，或 status 子命令只查远程版本不下载。
    if not update_config.get("auto_check", True) and not getattr(args, "force", False):
        if args.verbose:
            print("[update] auto_check=false，跳过启动检查（status 可查版本，check --force 可强制）")
        return 0

    skip_on_error = update_config.get("skip_on_error", True)
    local_version = meta.get("version", "")

    if args.verbose:
        print(f"[update] 本地版本: {local_version or '(无)'}")

    # 获取远程版本
    try:
        remote_version = fetch_remote_version(meta)
    except Exception as exc:
        if args.verbose:
            print(f"[update] 获取远程版本失败（已跳过）: {exc}")
        return 0 if skip_on_error else 1

    if not remote_version:
        if args.verbose:
            print("[update] 未找到远程版本信息，跳过")
        return 0

    if args.verbose:
        print(f"[update] 远程版本: {remote_version}")

    # 对比版本
    if not version_is_newer(remote_version, local_version):
        if args.verbose:
            print("[update] 本地版本已是最新")
        return 0

    print(f"[update] 发现新版本: {local_version or '(无)'} -> {remote_version}")

    # git 工作树保护：就地覆盖会抹掉未提交的源码工作，除非 --force
    if not getattr(args, "force", False) and _git_uncommitted(SKILL_ROOT):
        print(
            "[update] 安装目录是 git 工作树且有未提交改动，已跳过就地覆盖"
            "（防止抹掉源码工作）。"
        )
        print("[update] 如需强制更新，请先提交或使用 --force。")
        return 0

    # 执行更新
    try:
        success = perform_update(meta, remote_version)
    except Exception as exc:
        print(f"[update] 更新失败（已跳过）: {exc}")
        return 0 if skip_on_error else 1

    if success:
        update_local_version(meta, remote_version)
        print(f"[update] 已更新到版本 {remote_version}")
    else:
        print(
            f"[update] 更新失败：CLI 与直接下载均未成功"
            f"（本地仍为 {local_version}，远程 {remote_version}）"
        )
        return 0 if skip_on_error else 1

    return 0


def cmd_status(args: argparse.Namespace) -> int:
    """显示当前版本状态。"""
    meta = load_meta()
    local_version = meta.get("version", "(无)")
    print(f"本地版本: {local_version}")

    try:
        remote_version = fetch_remote_version(meta)
        if remote_version:
            print(f"远程版本: {remote_version}")
            if version_is_newer(remote_version, local_version):
                print("状态: 有新版本可用")
            else:
                print("状态: 已是最新")
        else:
            print("远程版本: 无法获取")
    except Exception as exc:
        print(f"远程版本: 获取失败 ({exc})")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Dragon Writer Skill 自动更新")
    parser.add_argument("command", nargs="?", default="check",
                        choices=["check", "status"],
                        help="check=检查并执行更新, status=显示版本状态")
    parser.add_argument("--verbose", "-v", action="store_true", help="详细输出")
    parser.add_argument("--force", action="store_true",
                        help="强制执行更新检查（覆盖 auto_check=false）")

    args = parser.parse_args()

    if args.command == "check":
        return cmd_check(args)
    elif args.command == "status":
        return cmd_status(args)
    return 0


if __name__ == "__main__":
    sys.exit(main())
