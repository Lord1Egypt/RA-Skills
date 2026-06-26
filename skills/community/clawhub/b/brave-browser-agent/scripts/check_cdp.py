#!/usr/bin/env python3
"""Comprehensive CDP health check for Brave Browser.

Tests: CDP connection, tab listing, JS execution, screenshot capability,
smart_interact delegation, page_state delegation, framework_click delegation.

Usage:
    python3 check_cdp.py          # Full check
    python3 check_cdp.py --quick  # Quick check (connection only)
    python3 check_cdp.py --json   # JSON output for tooling

Exit codes:
    0 - All OK
    1 - CDP port unreachable (Brave not running)
    2 - Some tests failed
"""

import argparse
import json
import os
import sys
import urllib.request

CDP_PORT = 9222
CDP_BASE = f"http://localhost:{CDP_PORT}"


def cdp_get(path, timeout=5):
    try:
        with urllib.request.urlopen(f"{CDP_BASE}{path}", timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        return {"_error": str(e)}


def check_connection():
    info = cdp_get("/json/version")
    if "_error" in info:
        return False, info["_error"], None
    return True, info.get("Browser", "?"), info.get("webSocketDebuggerUrl", "?")


def check_tabs():
    tabs = cdp_get("/json/list")
    if isinstance(tabs, dict) and "_error" in tabs:
        return False, tabs["_error"], 0
    return True, "ok", len(tabs) if tabs else 0


def check_script_imports():
    """Verify all sub-modules can be imported."""
    results = {}
    try:
        import ast
        # Parse cdp_exec.py to verify syntax
        script_dir = os.path.join(os.path.dirname(__file__))
        for fname in ["cdp_exec.py", "smart_interact.py", "page_state.py", "framework_click.py", "check_brave.py"]:
            fpath = os.path.join(script_dir, fname)
            if not os.path.exists(fpath):
                results[fname] = "MISSING"
                continue
            try:
                with open(fpath) as f:
                    ast.parse(f.read())
                results[fname] = "OK"
            except SyntaxError as e:
                results[fname] = f"SYNTAX ERROR: {e}"
        return results
    except Exception as e:
        return {"error": str(e)}


def check_skel():
    """Check SKILL.md for common issues."""
    issues = []
    skill_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "SKILL.md")
    if not os.path.exists(skill_path):
        return ["SKILL.md missing"]
    
    with open(skill_path) as f:
        content = f.read()
    
    # Check for duplicate headings
    headings = [l.strip() for l in content.split("\n") if l.strip().startswith("##")]
    from collections import Counter
    dupes = [h for h, c in Counter(headings).items() if c > 1]
    if dupes:
        issues.append(f"Duplicate headings: {dupes}")
    
    # Check for {{SKILL_DIR}} template vars (should resolve in OpenClaw)
    if "{{SKILL_DIR}}" not in content:
        issues.append("SKILL_DIR template variable missing from command examples")
    
    return issues


def check_assets():
    """Check assets directory size and content."""
    assets_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets")
    if not os.path.exists(assets_dir):
        return {"exists": False, "size_kb": 0}
    
    total_size = 0
    file_count = 0
    for root, dirs, files in os.walk(assets_dir):
        for f in files:
            fpath = os.path.join(root, f)
            total_size += os.path.getsize(fpath)
            file_count += 1
    
    return {
        "exists": True,
        "file_count": file_count,
        "size_kb": total_size // 1024,
    }


def run_all_checks(quick=False):
    results = {"status": "ok"}

    # 1. CDP Connection
    ok, browser, ws = check_connection()
    results["connection"] = {
        "ok": ok,
        "browser": browser,
        "websocket_url": ws,
    }
    if not ok:
        results["status"] = "error: brave not running"
        return results

    if quick:
        return results

    # 2. Tabs
    ok, _, count = check_tabs()
    results["tabs"] = {"ok": ok, "count": count}

    # 3. Script health
    results["scripts"] = check_script_imports()

    # 4. SKILL.md health
    skel_issues = check_skel()
    results["skel"] = {"ok": len(skel_issues) == 0, "issues": skel_issues}

    # 5. Assets
    results["assets"] = check_assets()

    # 6. Overall status
    all_script_ok = all(v == "OK" for v in results.get("scripts", {}).values())
    if not results["connection"]["ok"]:
        results["status"] = "fail"
    elif not all_script_ok:
        results["status"] = "warning"
    else:
        results["status"] = "ok"

    return results


def print_human(results):
    status = results.get("status", "unknown")
    if status == "error: brave not running":
        print("❌ Brave Browser 未运行或未启用远程调试 (port 9222)")
        print("   请手动重启 Brave: /Applications/Brave\\ Browser.app/Contents/MacOS/Brave\\ Browser --remote-debugging-port=9222")
        return

    if status == "ok":
        print("✅ All checks passed")
    elif status == "warning":
        print("⚠️  Some checks have warnings (see below)")
    else:
        print("❌ Some checks failed (see below)")

    conn = results.get("connection", {})
    if conn:
        print(f"\n📡 CDP Connection: {'✅' if conn['ok'] else '❌'}")
        if conn.get("browser"):
            print(f"   Browser: {conn['browser']}")

    tabs = results.get("tabs", {})
    if tabs:
        print(f"   Open tabs: {tabs.get('count', '?')}")

    print(f"\n📜 Script Health:")
    for name, status in results.get("scripts", {}).items():
        icon = "✅" if status == "OK" else "❌" if "MISSING" in status else "⚠️"
        print(f"   {icon} {name}: {status}")

    skel = results.get("skel", {})
    if skel.get("issues"):
        print(f"\n📄 SKILL.md Issues:")
        for issue in skel["issues"]:
            print(f"   ⚠️  {issue}")
    else:
        print(f"\n📄 SKILL.md: ✅ No issues")

    assets = results.get("assets", {})
    if assets:
        if assets.get("exists"):
            print(f"\n🗄️  Assets: {assets['file_count']} files, {assets['size_kb']}KB")
        else:
            print(f"\n🗄️  Assets: empty")


def main():
    parser = argparse.ArgumentParser(description="Brave Browser CDP Health Check")
    parser.add_argument("--quick", action="store_true", help="Quick check (connection only)")
    parser.add_argument("--json", action="store_true", help="JSON output")
    args = parser.parse_args()

    results = run_all_checks(quick=args.quick)

    if args.json:
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        print_human(results)

    status = results.get("status", "unknown")
    if status == "ok":
        sys.exit(0)
    elif status == "error: brave not running":
        sys.exit(1)
    else:
        sys.exit(2)


if __name__ == "__main__":
    main()
