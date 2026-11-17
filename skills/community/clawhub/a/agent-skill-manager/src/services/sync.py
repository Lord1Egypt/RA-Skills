"""Core sync logic: install, sync, remove, pack operations."""
from __future__ import annotations

import json
import shutil
import zipfile
import tempfile
import contextlib
import subprocess
from pathlib import Path

from ..config.products import (
    PRODUCTS,
    CENTRAL_DIR,
    get_product_path,
    get_all_product_dirs,
    ProductSpec,
)
from ..utils.filesystem import (
    is_symlink_or_junction,
    create_link,
    copy_skill,
    remove_path,
    read_skill_metadata,
)
from ..models.report import SkillReport, StatusEntry
from .audit import analyze_skill_dir, analyze_all


def list_skills() -> list[Path]:
    """List all skills in the central repository.

    Returns:
        Sorted list of skill directory paths.
    """
    if not CENTRAL_DIR.exists():
        return []
    return sorted(
        d for d in CENTRAL_DIR.iterdir()
        if d.is_dir() and (d / "SKILL.md").exists()
    )


def get_status(skill_name: str | None = None) -> list[StatusEntry]:
    """Get installation status of skills across all products.

    Args:
        skill_name: If specified, only check this skill.

    Returns:
        List of :class:`StatusEntry` dicts with keys:
        skill_name, product_short, product_name, status, method.
    """
    skills = list_skills()
    if skill_name:
        skills = [s for s in skills if s.name == skill_name]
        if not skills:
            return []

    results = []
    for skill_dir in skills:
        for p in PRODUCTS:
            entry = {
                "skill_name": skill_dir.name,
                "product_short": p["short"],
                "product_name": p["name"],
                "status": "",
                "method": p["sync_method"],
            }
            if p["sync_method"] == "native":
                entry["status"] = "ok" if skill_dir.exists() else "missing"
            elif p["sync_method"] == "pack":
                entry["status"] = "manual"
            else:
                target = get_product_path(p)
                if target is None:
                    entry["status"] = "n/a"
                else:
                    link_path = target / skill_dir.name
                    if link_path.exists() or link_path.is_symlink():
                        if is_symlink_or_junction(link_path):
                            entry["status"] = "ok"
                            entry["method"] = "link"
                        else:
                            entry["status"] = "ok"
                            entry["method"] = "copy"
                    else:
                        # BUGFIX 2026-08-14: previously extra_dirs (e.g. AutoClaw's
                        # ~/.openclaw-autoclaw/skills/) were never checked, so a skill
                        # synced only to an extra dir showed "missing". Check them too:
                        # if ANY extra dir has the skill linked/copied, report ok.
                        from ..config.products import IS_WINDOWS
                        extra_dirs = p.get("extra_dirs_windows", []) if IS_WINDOWS else p.get("extra_dirs_macos", [])
                        extra_ok = False
                        extra_method = ""
                        for extra in extra_dirs:
                            if extra is None:
                                continue
                            extra_link = Path(extra) / skill_dir.name
                            if extra_link.exists() or extra_link.is_symlink():
                                extra_ok = True
                                extra_method = "link" if is_symlink_or_junction(extra_link) else "copy"
                                break
                        if extra_ok:
                            entry["status"] = "ok"
                            entry["method"] = extra_method
                        else:
                            entry["status"] = "missing"
            results.append(entry)
    return results


def sync_skill(
    skill_name: str | None = None,
    verbose: bool = True,
) -> dict[str, list[tuple[str, bool, str]]]:
    """Sync skills from central repo to all products.

    Args:
        skill_name: If specified, only sync this skill. None = sync all.
        verbose: Print progress messages.

    Returns:
        Dict mapping skill_name -> list of (product_short, success, method).
    """
    if not CENTRAL_DIR.exists():
        if verbose:
            print(f"Central repository not found: {CENTRAL_DIR}")
        return {}

    skills = list_skills()
    if skill_name:
        skills = [s for s in skills if s.name == skill_name]
        if not skills:
            if verbose:
                print(f"Skill not found: {skill_name}")
            return {}

    if not skills:
        if verbose:
            print("No skills to sync.")
        return {}

    if verbose:
        print(f"\nSyncing {len(skills)} skill(s) to {len(PRODUCTS)} product(s)...\n")

    results = {}
    for skill_dir in skills:
        if verbose:
            print(f"[{skill_dir.name}]")
        sync_results = []
        for p in PRODUCTS:
            if p["sync_method"] == "native":
                if verbose:
                    print(f"  {p['short']:>10}: ok native (uses central repo)")
                sync_results.append((p["short"], True, "native"))
                continue

            if p["sync_method"] == "pack":
                if verbose:
                    print(f"  {p['short']:>10}: skip (use 'pack' command)")
                sync_results.append((p["short"], False, "pack"))
                continue

            target = get_product_path(p)
            if target is None:
                if verbose:
                    print(f"  {p['short']:>10}: n/a")
                sync_results.append((p["short"], False, "n/a"))
                continue

            link_path = target / skill_dir.name
            success, method, message = create_link(skill_dir, link_path)
            status_icon = "ok" if success else "FAIL"
            if verbose:
                print(f"  {p['short']:>10}: {status_icon} {method}")
            sync_results.append((p["short"], success, method))

            # BUGFIX 2026-08-14: extra_dirs must be synced too.
            #
            # 背景：部分产品会扫描多个技能目录。例如 AutoClaw 桌面版除了
            # 主路径 ~/.openclaw/skills/ 外，还会扫描 ~/.openclaw-autoclaw/skills/；
            # Kimi 除 ~/.config/agents/skills/ 外还扫描 ~/.kimi-code/skills/。
            # 旧代码只同步主路径，导致通过 askill 安装的技能在这些"额外目录"中
            # 缺失，产品内无法识别。
            #
            # 修复：主路径同步成功后，遍历产品声明的额外目录，对每个额外目录
            # 也创建 junction/symlink（Windows 用 junction，无需管理员权限；
            # macOS 用 symlink；失败时 create_link 内部自动降级为复制）。
            from ..config.products import IS_WINDOWS
            if IS_WINDOWS:
                extra_dirs = p.get("extra_dirs_windows", [])
            else:
                extra_dirs = p.get("extra_dirs_macos", [])
            for extra in extra_dirs:
                if extra is None:
                    continue
                extra_link = Path(extra) / skill_dir.name
                # 确保额外目录存在（mkdir -p 语义）
                try:
                    extra_link.parent.mkdir(parents=True, exist_ok=True)
                except OSError:
                    pass
                ok2, method2, _ = create_link(skill_dir, extra_link)
                if verbose:
                    print(f"  {p['short']:>10}: extra -> {extra_link} ({method2 if ok2 else 'FAIL'})")

            # Handle WorkBuddy settings.json
            if p.get("settings_file") and success:
                _update_workbuddy_settings(p["settings_file"], skill_dir.name, verbose=verbose)

        if verbose:
            print()
        results[skill_dir.name] = sync_results

    return results


def install_skill(source: str, sync: bool = False, audit: bool = False, verbose: bool = True) -> bool:
    """Install a skill to the central repository.

    Args:
        source: Local path or GitHub URL.
        sync: If True, also sync the installed skill to all products.
        audit: If True, run the security audit after install.
        verbose: Print progress messages.

    Returns:
        True if installation succeeded.
    """
    CENTRAL_DIR.mkdir(parents=True, exist_ok=True)

    if source.startswith("http"):
        name, ok = _install_from_url(source, verbose=verbose)
    else:
        name, ok = _install_from_local(source, verbose=verbose)

    if ok and sync and name:
        if verbose:
            print()
        sync_skill(name, verbose=verbose)

    if ok and audit and name:
        if verbose:
            print()
            print(f"Running security audit on {name}...")
        audit_skill(name, verbose=verbose)

    return ok


def _install_from_local(source: str, verbose: bool = True) -> tuple[str | None, bool]:
    """Install skill from a local path.
    Returns (skill_name, success).
    """
    src = Path(source).resolve()
    if not src.exists():
        if verbose:
            print(f"Path not found: {src}")
        return None, False

    if not (src / "SKILL.md").exists():
        if verbose:
            print(f"No SKILL.md found in: {src}")
        return None, False

    dest = CENTRAL_DIR / src.name
    if dest.exists():
        if verbose:
            print(f"Skill already exists: {dest}")
            print(f"Remove it first: askill remove {src.name}")
        return None, False

    shutil.copytree(src, dest)
    if verbose:
        print(f"Installed to central repo: {dest}")
        print(f"  Run 'askill sync' to distribute to all products.")
    return src.name, True


def _install_from_url(source: str, verbose: bool = True) -> tuple[str | None, bool]:
    """Install skill from a GitHub URL.

    Supports these GitHub URL formats:
      - https://github.com/user/repo                      (repo root SKILL.md)
      - https://github.com/user/repo/tree/branch          (branch root)
      - https://github.com/user/repo/tree/branch/path/to/skill
      - https://github.com/user/repo/blob/branch/path/to/skill/SKILL.md

    Returns (skill_name, success).
    """
    if verbose:
        print(f"Installing from URL: {source}")

    if "github.com" not in source:
        if verbose:
            print("Unsupported URL format. Use a GitHub URL.")
        return None, False

    # Parse GitHub URL into (repo_url, branch, sub_path, skill_name)
    branch = None  # None = use git default branch
    if "/tree/" in source:
        parts = source.split("/tree/")
        repo_url = parts[0]
        rest = parts[1].lstrip("/")
        segs = rest.split("/")
        branch = segs[0] if segs else None
        sub_path = "/".join(segs[1:]) if len(segs) > 1 else ""
        skill_name = segs[-1] if len(segs) > 1 else repo_url.split("/")[-1]
    elif "/blob/" in source:
        parts = source.split("/blob/")
        repo_url = parts[0]
        rest = parts[1].lstrip("/")
        segs = rest.split("/")
        branch = segs[0] if segs else None
        if segs and (segs[-1] == "SKILL.md" or segs[-1] == "SKILL.md/"):
            segs = segs[:-1]  # strip SKILL.md from path
        sub_path = "/".join(segs[1:]) if len(segs) > 1 else ""
        skill_name = segs[-1] if len(segs) > 1 else repo_url.split("/")[-1]
    else:
        parts = source.rstrip("/").split("/")
        if len(parts) < 5:
            if verbose:
                print(f"Invalid GitHub URL: {source}")
            return None, False
        repo_url = "/".join(parts[:5])
        sub_path = ""
        skill_name = parts[-1]

    dest = CENTRAL_DIR / skill_name
    if dest.exists():
        if verbose:
            print(f"Skill already exists: {dest}")
            print(f"Remove it first: askill remove {skill_name}")
        return None, False

    if verbose:
        print(f"  Repo: {repo_url}")
        print(f"  Branch: {branch or '(default)'}")
        print(f"  Path: {sub_path or '(root)'}")

    with tempfile.TemporaryDirectory() as tmp:
        try:
            cmd = ["git", "clone", "--depth", "1"]
            if branch:
                cmd += ["--branch", branch]
            cmd += [repo_url, tmp]
            subprocess.run(
                cmd,
                check=True, capture_output=True, text=True, encoding="utf-8", errors="replace",
            )
            if sub_path:
                src = Path(tmp) / sub_path
            else:
                src = Path(tmp)

            if not src.exists() or not (src / "SKILL.md").exists():
                if verbose:
                    print(f"No SKILL.md found in {src}")
                return None, False

            shutil.copytree(src, dest)
            if verbose:
                print(f"Installed: {dest}")
            return skill_name, True
        except subprocess.CalledProcessError as e:
            if verbose:
                print(f"Git clone failed: {e.stderr}")
            return None, False
        except Exception as e:
            if verbose:
                print(f"Error: {e}")
            return None, False

def remove_skill(skill_name: str, verbose: bool = True) -> list[str]:
    """Remove a skill from central repo and all products.

    Args:
        skill_name: Name of the skill to remove.
        verbose: Print progress messages.

    Returns:
        List of locations where the skill was removed.
    """
    skill_dir = CENTRAL_DIR / skill_name
    if not skill_dir.exists():
        if verbose:
            print(f"Skill not found in central repo: {skill_name}")
        return []

    removed = []

    for p in PRODUCTS:
        if p["sync_method"] in ("native", "pack"):
            continue

        target = get_product_path(p)
        if target is None:
            continue

        link_path = target / skill_name
        if link_path.exists() or link_path.is_symlink():
            remove_path(link_path)
            removed.append(p["short"])

        for d in get_all_product_dirs(p)[1:]:
            link_path = d / skill_name
            if link_path.exists() or link_path.is_symlink():
                remove_path(link_path)
                removed.append(f"{p['short']}-alt")

        if p.get("settings_file"):
            _remove_from_workbuddy_settings(p["settings_file"], skill_name, removed, verbose=verbose)

    shutil.rmtree(skill_dir)
    removed.append("central")

    if verbose:
        print(f"Removed '{skill_name}' from: {', '.join(removed)}")
    return removed


def pack_skill(skill_name: str, verbose: bool = True) -> Path | None:
    """Package a skill as .zip for DuMate upload.

    Args:
        skill_name: Name of the skill to pack.
        verbose: Print progress messages.

    Returns:
        Path to the generated .zip file, or None on failure.
    """
    skill_dir = CENTRAL_DIR / skill_name
    if not skill_dir.exists():
        if verbose:
            print(f"Skill not found: {skill_name}")
        return None

    if not (skill_dir / "SKILL.md").exists():
        if verbose:
            print(f"No SKILL.md found in: {skill_dir}")
        return None

    output_path = CENTRAL_DIR / f"{skill_name}.zip"

    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for file_path in skill_dir.rglob("*"):
            if file_path.is_file():
                arcname = file_path.relative_to(skill_dir.parent)
                zf.write(file_path, arcname)

    if verbose:
        print(f"Packed: {output_path}")
        print(f"  Upload this file in DuMate App -> Skills -> Install")
    return output_path


def _update_workbuddy_settings(settings_path: Path, skill_name: str, verbose: bool = True) -> None:
    """Enable a skill in WorkBuddy's settings.json."""
    try:
        if settings_path.exists():
            settings = json.loads(settings_path.read_text(encoding="utf-8"))
        else:
            settings = {}

        skills_config = settings.setdefault("skills", {})
        skills_config[skill_name] = True

        settings_path.parent.mkdir(parents=True, exist_ok=True)
        settings_path.write_text(
            json.dumps(settings, indent=2, ensure_ascii=False),
            encoding="utf-8"
        )
        if verbose:
            print(f"  {'':>10}   Updated settings.json")
    except Exception as e:
        if verbose:
            print(f"  {'':>10}   Warning: could not update settings.json: {e}")


def _remove_from_workbuddy_settings(
    settings_path: Path, skill_name: str, removed: list, verbose: bool = True
) -> None:
    """Remove a skill from WorkBuddy's settings.json."""
    try:
        if settings_path.exists():
            settings = json.loads(settings_path.read_text(encoding="utf-8"))
            if "skills" in settings and skill_name in settings["skills"]:
                del settings["skills"][skill_name]
                settings_path.write_text(
                    json.dumps(settings, indent=2, ensure_ascii=False),
                    encoding="utf-8"
                )
                removed.append("workbuddy-settings")
    except Exception:
        pass



def audit_skill(skill_name: str, verbose: bool = True) -> SkillReport | None:
    """Run the static security audit on a skill in the central repository.

    Args:
        skill_name: Name of the skill directory.
        verbose: Print the report.

    Returns:
        :class:`SkillReport`, or None if the skill does not exist.
    """
    skill_dir = CENTRAL_DIR / skill_name
    if not skill_dir.exists():
        if verbose:
            print(f"Skill not found: {skill_name}")
        return None
    report = analyze_skill_dir(skill_dir)
    if verbose:
        _print_audit_report(report)
    return report


def audit_all(verbose: bool = True) -> list[SkillReport]:
    """Audit all skills in the central repository. Returns list of reports."""
    reports = analyze_all(CENTRAL_DIR)
    if verbose:
        if not reports:
            print("No skills found in central repository.")
        else:
            for r in reports:
                _print_audit_report(r, brief=True)
                print()
    return reports


def _print_audit_report(report: SkillReport, brief: bool = False) -> None:
    """Pretty-print an audit report."""
    verdict_icon = {
        "safe": "OK",
        "caution": "CAUTION",
        "risky": "RISKY",
        "dangerous": "DANGEROUS",
    }
    print(f"[{report['skill']}] score={report['score']}/100 grade={report['grade']} "
          f"verdict={verdict_icon[report['verdict']]} files={report['files']}")
    s = report["summary"]
    print(f"  findings: critical={s['critical']} high={s['high']} "
          f"medium={s['medium']} low={s['low']} info={s['info']}")
    if brief and not report["findings"]:
        return
    if brief:
        for f in report["findings"]:
            if f["severity"] in ("critical", "high"):
                loc = f":{f['line']}" if f.get("line") else ""
                print(f"  - [{f['severity']}] {f['message']} ({f['file']}{loc})")
        return
    if not report["findings"]:
        print("  No issues found.")
        return
    for f in report["findings"]:
        loc = f":{f['line']}" if f.get("line") else ""
        print(f"  - [{f['severity']}] {f['message']} ({f['file']}{loc})")


def adopt_from_platform(
    platform_short: str,
    skill_name: str | None = None,
    verbose: bool = True,
) -> dict:
    """Adopt skills from one product platform into central repo, sync to all others.

    Scans a product skill directory for skills not yet in the central
    repository, copies them in, then syncs to all OTHER products.
    Reverse of sync: pull from one product to everywhere else.

    Args:
        platform_short: Short name of source product (e.g. autoclaw, trae).
        skill_name: If specified, only adopt this single skill.
        verbose: Print progress messages.

    Returns:
        Dict with keys: adopted (list of tuples), synced (dict from sync_skill).
    """
    from ..config.products import get_all_product_dirs, IS_WINDOWS

    product: ProductSpec | None = None
    for p in PRODUCTS:
        if p["short"] == platform_short:
            product = p
            break
    if product is None:
        if verbose:
            print(f"Unknown platform: {platform_short}")
            shorts = [p["short"] for p in PRODUCTS]
            print(f"Available: {', '.join(shorts)}")
        return {"adopted": [], "synced": {}}

    if product["sync_method"] in ("native", "pack"):
        if verbose:
            print(
                f"Platform {platform_short!r} uses {product['sync_method']} mode, "
                "no skill directory to adopt from."
            )
        return {"adopted": [], "synced": {}}

    all_dirs = get_all_product_dirs(product)
    source_skills: dict[str, Path] = {}

    for d in all_dirs:
        if not d.exists():
            continue
        for item in sorted(d.iterdir()):
            if item.is_dir() and (item / "SKILL.md").exists():
                real = item.resolve()
                if item.name not in source_skills:
                    source_skills[item.name] = real

    if not source_skills:
        if verbose:
            print(f"No skills found in {product['name']} directories.")
        return {"adopted": [], "synced": {}}

    if skill_name:
        if skill_name not in source_skills:
            if verbose:
                print(f"Skill {skill_name!r} not found in {product['name']}.")
                print("Available: " + ", ".join(sorted(source_skills.keys())))
            return {"adopted": [], "synced": {}}
        source_skills = {skill_name: source_skills[skill_name]}

    if verbose:
        print(f"\nAdopting from {product['name']} ({platform_short}):")
        print(f"  Found {len(source_skills)} skill(s)")
        print(f"  Central repo: {CENTRAL_DIR}\n")

    CENTRAL_DIR.mkdir(parents=True, exist_ok=True)

    adopted = []
    skills_to_sync = []

    for name, src_path in source_skills.items():
        dest = CENTRAL_DIR / name

        if dest.exists():
            if dest.resolve() == src_path:
                if verbose:
                    print(f"  [{name}] already in central repo, skipping")
                adopted.append((name, True, "already-present"))
                skills_to_sync.append(name)
                continue
            else:
                if verbose:
                    print(f"  [{name}] already exists (different source)")
                    print(f"    Remove first: askill remove {name}")
                adopted.append((name, False, "conflict"))
                continue

        try:
            real_src = src_path
            if IS_WINDOWS and _is_junction(src_path):
                real_src = src_path.resolve()
            elif src_path.is_symlink():
                real_src = src_path.resolve()

            shutil.copytree(real_src, dest)
            if verbose:
                print(f"  [{name}] adopted -> {dest}")
            adopted.append((name, True, "copied"))
            skills_to_sync.append(name)
        except Exception as e:
            if verbose:
                print(f"  [{name}] FAILED: {e}")
            adopted.append((name, False, f"error: {e}"))

    synced = {}
    if skills_to_sync:
        if verbose:
            print(
                f"\nSyncing {len(skills_to_sync)} skill(s) to "
                "other products...\n"
            )

        other_products = [p for p in PRODUCTS if p["short"] != platform_short]
        with _patch_products(other_products):
            for skill in skills_to_sync:
                result = sync_skill(skill, verbose=verbose)
                synced.update(result)

    return {"adopted": adopted, "synced": synced}


def _is_junction(path: Path) -> bool:
    """Check if a Windows path is a junction point."""
    import platform
    if platform.system() != "Windows":
        return False
    try:
        result = subprocess.run(
            ["fsutil", "reparsepoint", "query", str(path)],
            capture_output=True, text=True, encoding="utf-8", errors="replace",
        )
        return result.returncode == 0
    except Exception:
        return False


@contextlib.contextmanager
def _patch_products(new_products):
    """Temporarily replace PRODUCTS list (exclude source platform)."""
    old = PRODUCTS[:]
    PRODUCTS.clear()
    PRODUCTS.extend(new_products)
    try:
        yield
    finally:
        PRODUCTS.clear()
        PRODUCTS.extend(old)
