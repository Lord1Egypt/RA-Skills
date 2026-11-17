"""CLI entry point for agent-skill-manager."""

import sys
import platform

from ..config.products import PRODUCTS, CENTRAL_DIR, get_product_path, get_all_product_dirs
from ..utils.filesystem import is_symlink_or_junction, read_skill_metadata
from ..services.audit import analyze_skill_dir
from ..services.sync import (
    list_skills,
    get_status,
    sync_skill,
    install_skill,
    remove_skill,
    pack_skill,
    adopt_from_platform,
    audit_skill,
    audit_all,
)


def _print_products():
    """Print all supported products and their paths."""
    print(f"\n{'='*60}")
    print(f"Supported Products ({len(PRODUCTS)})")
    print(f"{'='*60}")
    print(f"Platform: {platform.system()}")
    print(f"Central repo: {CENTRAL_DIR}")
    print(f"{'='*60}\n")

    for p in PRODUCTS:
        print(f"  [{p['short']}] {p['name']}")
        if p["sync_method"] == "native":
            path = get_product_path(p)
            print(f"    Path: {path} (native, no sync needed)")
        elif p["sync_method"] == "pack":
            print(f"    Path: App-managed (use 'pack' command)")
        else:
            primary = get_product_path(p)
            if primary:
                exists = "[ok]" if primary.exists() else "[--]"
                print(f"    Path: {primary} {exists}")
        extra_dirs = get_all_product_dirs(p)
        for d in extra_dirs[1:]:
            exists = "[ok]" if d.exists() else "[--]"
            print(f"    Alt:  {d} {exists}")
        if p.get("note"):
            print(f"    Note: {p['note']}")
        print()


def _print_list():
    """List all skills in the central repository."""
    skills = list_skills()
    if not skills:
        if not CENTRAL_DIR.exists():
            print(f"Central repository not found: {CENTRAL_DIR}")
            print("Create it by installing a skill: askill install <path>")
        else:
            print(f"No skills found in {CENTRAL_DIR}")
        return

    print(f"\nSkills in central repository ({CENTRAL_DIR}):")
    print(f"{'-'*50}")
    verdict_icon = {"safe": "OK", "caution": "CAUTION", "risky": "RISKY", "dangerous": "DANGEROUS"}
    for s in skills:
        meta = read_skill_metadata(s)
        report = analyze_skill_dir(s)
        print(f"  {s.name}  [score {report['score']}/100 grade {report['grade']} {verdict_icon[report['verdict']]}]")
        if meta.get("description"):
            desc = meta["description"][:80]
            print(f"    -> {desc}...")
    print()


def _print_status(skill_name=None):
    """Print installation status of skills across all products."""
    results = get_status(skill_name)
    if not results:
        if skill_name:
            print(f"Skill not found: {skill_name}")
        else:
            print("No skills found in central repository.")
        return

    # Build table
    product_shorts = [p["short"] for p in PRODUCTS]
    header = f"{'Skill':<25}"
    for ps in product_shorts:
        header += f" {ps:<12}"
    header += f" {'score':<13}"
    print(f"\n{header}")
    print(f"{'-'*(25 + len(PRODUCTS)*13 + 14)}")

    # Group results by skill (skill -> {product_short: (status, method)})
    verdict_icon = {"safe": "OK", "caution": "CAUTION", "risky": "RISKY", "dangerous": "DANGEROUS"}
    by_skill = {}
    order = []
    for r in results:
        sn = r["skill_name"]
        if sn not in by_skill:
            by_skill[sn] = {}
            order.append(sn)
        by_skill[sn][r["product_short"]] = (r["status"], r["method"])

    for sn in order:
        row = f"{sn:<25}"
        for ps in product_shorts:
            if ps in by_skill[sn]:
                status, method = by_skill[sn][ps]
                if status == "ok":
                    cell = f"ok {method}"
                elif status == "missing":
                    cell = "--"
                elif status == "manual":
                    cell = "manual"
                elif status == "n/a":
                    cell = "n/a"
                else:
                    cell = status
            else:
                cell = "--"
            row += f" {cell:<11}"
        # Security audit score for this skill
        skill_dir = CENTRAL_DIR / sn
        if skill_dir.exists():
            report = analyze_skill_dir(skill_dir)
            row += f" {report['score']}/{report['grade']} {verdict_icon[report['verdict']]:<7}"
        else:
            row += f" {'n/a':<13}"
        print(row)
    print()


def _print_sync(skill_name=None):
    """Sync skills and print results."""
    sync_skill(skill_name, verbose=True)


def _print_install(source, sync=False, audit=False):
    """Install a skill and print results."""
    install_skill(source, sync=sync, audit=audit, verbose=True)


def _print_remove(skill_name):
    """Remove a skill and print results."""
    remove_skill(skill_name, verbose=True)


def _print_pack(skill_name):
    """Pack a skill and print results."""
    pack_skill(skill_name, verbose=True)


def _print_adopt(platform_short, skill_name=None):
    """Adopt skills from one platform to all others."""
    adopt_from_platform(platform_short, skill_name, verbose=True)


def _print_audit(skill_name=None):
    """Audit one or all skills and print reports."""
    if skill_name:
        audit_skill(skill_name, verbose=True)
    else:
        audit_all(verbose=True)



USAGE = """\
Agent Skill Manager - Cross-platform skill management for domestic AI agent products.

Supports: AutoClaw, Kimi, MiniMax Code, WorkBuddy, Trae, DuMate.

Usage:
    askill status [skill-name]       Show installation status across products
    askill sync [skill-name]         Sync skill(s) to all products
    askill list                      List skills in central repository
    askill install [--sync] <path-or-url>  Install a skill, optionally sync to all
    askill remove <skill-name>       Remove a skill from all products
    askill pack <skill-name>         Package a skill as .zip for DuMate
    askill adopt <platform> [skill]  Adopt skills from one platform to all others
    askill audit [skill-name]        Security audit of skill(s) in central repo
    askill products                  List all supported products
    askill version                   Show version
"""


def main():
    """CLI entry point."""
    if len(sys.argv) < 2:
        print(USAGE)
        return

    command = sys.argv[1].lower()

    if command == "status":
        skill_name = sys.argv[2] if len(sys.argv) > 2 else None
        _print_status(skill_name)
    elif command == "sync":
        skill_name = sys.argv[2] if len(sys.argv) > 2 else None
        _print_sync(skill_name)
    elif command == "list":
        _print_list()
    elif command == "install":
        if len(sys.argv) < 3 or "--help" in sys.argv or "-h" in sys.argv:
            print("Usage: askill install [--sync] [--audit] <path-or-url>")
            print("  --sync   Also sync to all products after install")
            print("  --audit  Run security audit after install")
            return
        do_sync = False
        do_audit = False
        args = sys.argv[2:]
        if "--sync" in args:
            do_sync = True
            args.remove("--sync")
        if "--audit" in args:
            do_audit = True
            args.remove("--audit")
        if not args:
            print("Usage: askill install [--sync] [--audit] <path-or-url>")
            return
        _print_install(args[0], sync=do_sync, audit=do_audit)
    elif command == "remove":
        if len(sys.argv) < 3:
            print("Usage: askill remove <skill-name>")
            return
        _print_remove(sys.argv[2])
    elif command == "pack":
        if len(sys.argv) < 3:
            print("Usage: askill pack <skill-name>")
            return
        _print_pack(skill_name=sys.argv[2])
    elif command == "adopt":
        if len(sys.argv) < 3:
            print("Usage: askill adopt <platform> [skill-name]")
            return
        platform = sys.argv[2].lower()
        skill = sys.argv[3] if len(sys.argv) > 3 else None
        _print_adopt(platform, skill)
    elif command == "audit":
        skill_name = sys.argv[2] if len(sys.argv) > 2 else None
        _print_audit(skill_name)
    elif command == "products":
        _print_products()
    elif command == "version":
        from .. import __version__
        print(f"agent-skill-manager v{__version__}")
    elif command in ("-h", "--help", "help"):
        print(USAGE)
    else:
        print(f"Unknown command: {command}")
        print(USAGE)


if __name__ == "__main__":
    main()
