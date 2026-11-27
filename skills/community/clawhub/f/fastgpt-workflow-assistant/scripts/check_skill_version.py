#!/usr/bin/env python3
"""报告本地 Skill 版本，并与可信发布清单或候选 ZIP 比较。"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import urllib.request
import zipfile
from pathlib import Path
from typing import Any


SKILL_ROOT = Path(__file__).resolve().parent.parent
VERSION_FILE = SKILL_ROOT / "assets" / "skill-version.json"
SEMVER_PATTERN = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")
MAX_MANIFEST_BYTES = 1024 * 1024


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", help="latest.json 本地路径或 HTTPS 地址")
    parser.add_argument("--package", type=Path, help="待验证和比较的 Skill ZIP")
    parser.add_argument("--json", action="store_true", help="输出机器可读 JSON")
    parser.add_argument("--require-latest", action="store_true", help="发现可更新版本时返回退出码2")
    return parser.parse_args()


def load_json_bytes(raw: bytes, source: str) -> dict[str, Any]:
    value = json.loads(raw.decode("utf-8-sig"))
    if not isinstance(value, dict):
        raise ValueError(f"JSON 顶层必须是对象：{source}")
    return value


def load_local_version() -> dict[str, Any]:
    return load_json_bytes(VERSION_FILE.read_bytes(), str(VERSION_FILE))


def validate_semver(value: Any, field: str) -> str:
    version = str(value or "").strip()
    if not SEMVER_PATTERN.fullmatch(version):
        raise ValueError(f"{field} 不是有效的 x.y.z 版本：{version!r}")
    return version


def version_tuple(value: str) -> tuple[int, int, int]:
    return tuple(int(part) for part in value.split("."))  # type: ignore[return-value]


def load_release_manifest(source: str) -> dict[str, Any]:
    if source.lower().startswith("https://"):
        request = urllib.request.Request(source, headers={"User-Agent": "LeapRAG-Skill-Version-Checker/1.0"})
        with urllib.request.urlopen(request, timeout=10) as response:
            raw = response.read(MAX_MANIFEST_BYTES + 1)
        if len(raw) > MAX_MANIFEST_BYTES:
            raise ValueError("发布清单超过1MiB限制")
        return load_json_bytes(raw, source)
    if "://" in source:
        raise ValueError("远程发布清单只允许 HTTPS")
    path = Path(source).expanduser().resolve()
    return load_json_bytes(path.read_bytes(), str(path))


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def inspect_package(path: Path) -> dict[str, Any]:
    package = path.expanduser().resolve()
    if not package.is_file():
        raise FileNotFoundError(package)
    with zipfile.ZipFile(package) as archive:
        bad_entry = archive.testzip()
        if bad_entry:
            raise ValueError(f"ZIP损坏条目：{bad_entry}")
        names = archive.namelist()
        if "SKILL.md" not in names:
            raise ValueError("ZIP根目录缺少SKILL.md")
        if "assets/skill-version.json" not in names:
            raise ValueError("ZIP缺少assets/skill-version.json")
        package_version = load_json_bytes(archive.read("assets/skill-version.json"), str(package))
    return {
        "path": str(package),
        "skill_name": str(package_version.get("skill_name", "")),
        "version": validate_semver(package_version.get("version"), "package.version"),
        "sha256": sha256_file(package),
    }


def verify_local_consistency(local: dict[str, Any]) -> list[str]:
    version = validate_semver(local.get("version"), "version")
    skill_name = str(local.get("skill_name", ""))
    errors: list[str] = []
    skill_text = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8-sig")
    agent_text = (SKILL_ROOT / "agents" / "openai.yaml").read_text(encoding="utf-8-sig")
    release_example = json.loads((SKILL_ROOT / "assets" / "发布清单示例.json").read_text(encoding="utf-8-sig"))
    if f"当前版本 {version}" not in skill_text or f"v{version}" not in skill_text:
        errors.append("SKILL.md版本与skill-version.json不一致")
    if f"v{version}" not in agent_text:
        errors.append("agents/openai.yaml展示版本不一致")
    if str(release_example.get("skill_version")) != version:
        errors.append("发布清单示例版本不一致")
    if not skill_name or f"name: {skill_name}" not in skill_text:
        errors.append("SKILL.md机器名与skill-version.json不一致")
    return errors


def main() -> int:
    args = parse_args()
    try:
        local = load_local_version()
        skill_name = str(local.get("skill_name", ""))
        current_version = validate_semver(local.get("version"), "version")
        consistency_errors = verify_local_consistency(local)
        if consistency_errors:
            raise ValueError("；".join(consistency_errors))

        result: dict[str, Any] = {
            "skill_name": skill_name,
            "display_name": local.get("display_name"),
            "current_version": current_version,
            "release_date": local.get("release_date"),
            "status": "current_only",
            "automatic_update": False,
        }

        latest_version = None
        release_manifest = None
        if args.manifest:
            release_manifest = load_release_manifest(args.manifest)
            manifest_skill = str(release_manifest.get("skill_name", ""))
            if manifest_skill != skill_name:
                raise ValueError(f"发布清单技能名不匹配：{manifest_skill!r}")
            latest_version = validate_semver(
                release_manifest.get("latest_version", release_manifest.get("version")),
                "latest_version",
            )
            result.update({
                "latest_version": latest_version,
                "manifest_source": args.manifest,
                "download_url": release_manifest.get("download_url"),
                "expected_sha256": release_manifest.get("package_sha256"),
            })

        package_info = None
        if args.package:
            package_info = inspect_package(args.package)
            if package_info["skill_name"] != skill_name:
                raise ValueError(f"候选ZIP技能名不匹配：{package_info['skill_name']!r}")
            result["package"] = package_info
            if latest_version and package_info["version"] != latest_version:
                raise ValueError("候选ZIP版本与发布清单latest_version不一致")
            expected_sha = str((release_manifest or {}).get("package_sha256", "")).upper()
            if expected_sha and package_info["sha256"] != expected_sha:
                raise ValueError("候选ZIP的SHA-256与发布清单不一致")
            if latest_version is None:
                latest_version = package_info["version"]
                result["latest_version"] = latest_version

        if latest_version:
            current_key, latest_key = version_tuple(current_version), version_tuple(latest_version)
            if latest_key > current_key:
                result["status"] = "update_available"
            elif latest_key == current_key:
                result["status"] = "up_to_date"
            else:
                result["status"] = "local_newer"

        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"技能：{result['display_name']} ({skill_name})")
            print(f"当前版本：{current_version}，发布日期：{result.get('release_date')}")
            if latest_version:
                print(f"目标版本：{latest_version}，状态：{result['status']}")
            else:
                print("状态：已读取本地版本；未提供可信发布清单，未检查远程更新。")
            if result.get("download_url"):
                print(f"下载地址：{result['download_url']}")
            print("自动更新：关闭；更新需由用户显式执行并验证。")
        if args.require_latest and result["status"] == "update_available":
            return 2
        return 0
    except Exception as exc:
        if args.json:
            print(json.dumps({"status": "error", "error": f"{type(exc).__name__}: {exc}"}, ensure_ascii=False, indent=2))
        else:
            print(f"ERROR: {type(exc).__name__}: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

