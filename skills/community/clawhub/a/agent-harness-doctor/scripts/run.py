#!/usr/bin/env python3
"""
agent-harness-doctor — diagnostic and auto-fix for agent harness
"""

import json
import sys
import os
from pathlib import Path

WORKSPACE = Path.cwd()
AGENTS_FILE = WORKSPACE / "AGENTS.md"
MEMORY_DIR = WORKSPACE / "memory"
SESSION_STATE = MEMORY_DIR / "SESSION-STATE.md"
PROGRESS_FILE = WORKSPACE / "agent-progress.json"

def read_agents():
    if AGENTS_FILE.exists():
        return AGENTS_FILE.read_text()
    return ""

def dimension_session_bridge():
    """Check for agent-progress.json"""
    if PROGRESS_FILE.exists():
        try:
            data = json.loads(PROGRESS_FILE.read_text())
            # Check required fields
            if all(k in data for k in ("lastSession", "taskTracking", "environmentStatus")):
                return {"score": 10, "finding": "Session bridge present and valid", "p0": False}
        except:
            pass
    return {"score": 2, "finding": "Missing or invalid agent-progress.json", "p0": True, "recommendation": "Create agent-progress.json with lastSession, taskTracking, environmentStatus"}

def dimension_startup_sequence():
    """Check AGENTS.md for fixed startup sequence"""
    content = read_agents()
    if "## Session Startup" in content or "startup sequence" in content.lower():
        # Check for ordered steps
        if "Step 1" in content or "1. " in content:
            return {"score": 10, "finding": "Fixed startup sequence documented", "p0": False}
    return {"score": 3, "finding": "No explicit fixed startup sequence in AGENTS.md", "p0": True, "recommendation": "Add a numbered step list that must execute on every session start"}

def dimension_smoke_test():
    """Check for pre-task environment checks"""
    content = read_agents()
    if "smoke test" in content.lower() or "pre-check" in content.lower():
        return {"score": 8, "finding": "Smoke test mentioned", "p0": False}
    return {"score": 4, "finding": "No smoke test procedure found", "p0": False, "recommendation": "Add a step that verifies gateway/API connectivity before tasks"}

def dimension_atomic_checkpoint():
    """Check for commit/save after tasks"""
    content = read_agents()
    if "commit" in content.lower() and "after each task" in content.lower():
        return {"score": 10, "finding": "Atomic checkpoint policy present", "p0": False}
    return {"score": 5, "finding": "Unclear checkpoint cadence", "p0": False, "recommendation": "Define 'after each task, commit state' rule"}

def dimension_output_verification():
    """Check for output self-verification"""
    content = read_agents()
    if "self-check" in content.lower() or "output gate" in content.lower() or "verify before sending" in content.lower():
        return {"score": 9, "finding": "Output verification gate documented", "p0": False}
    return {"score": 3, "finding": "No output verification mechanism", "p0": False, "recommendation": "Add internal check before reporting 'done'"}

def dimension_state_format():
    """Check state files are JSON not Markdown"""
    # Look for state files other than progress (e.g., SESSION-STATE.md)
    if SESSION_STATE.exists():
        # Check extension
        if SESSION_STATE.suffix == ".json":
            return {"score": 10, "finding": "State stored as JSON", "p0": False}
        else:
            return {"score": 4, "finding": "State stored as non-JSON (e.g., .md)", "p0": False, "recommendation": "Use JSON for structured state"}
    return {"score": 7, "finding": "No separate state file found; ok if using memory layers", "p0": False}

def dimension_multi_agent():
    """Check for multi-agent coordination protocol"""
    content = read_agents()
    if "multi-agent" in content.lower() or "agent protocol" in content.lower() or "message passing" in content.lower():
        return {"score": 8, "finding": "Multi-agent protocol mentioned", "p0": False}
    return {"score": 6, "finding": "Multi-agent not applicable or not documented", "p0": False}

def dimension_fallback():
    """Check for fallback/retry logic"""
    content = read_agents()
    if "fallback" in content.lower() or "retry" in content.lower() or "plan b" in content.lower():
        return {"score": 9, "finding": "Fallback plan documented", "p0": False}
    return {"score": 4, "finding": "No fallback strategy", "p0": False, "recommendation": "Define what to do when API/dependency fails"}

def run_diagnostic():
    dims = [
        ("session_bridge", dimension_session_bridge()),
        ("startup_sequence", dimension_startup_sequence()),
        ("smoke_test", dimension_smoke_test()),
        ("atomic_checkpoint", dimension_atomic_checkpoint()),
        ("output_verification", dimension_output_verification()),
        ("state_format", dimension_state_format()),
        ("multi_agent", dimension_multi_agent()),
        ("fallback", dimension_fallback()),
    ]
    
    total = sum(d["score"] for _, d in dims)
    avg = total / len(dims)
    grade = "A" if avg >= 9 else "B" if avg >= 7 else "C" if avg >= 5 else "D"
    
    weakest = min(dims, key=lambda x: x[1]["score"])
    
    # Find P0 items
    p0 = [name for name, d in dims if d.get("p0")]
    p1 = []  # could derive from score < 7 but > p0 threshold
    p2 = []
    
    return {
        "summary": {"score": round(avg, 1), "grade": grade, "weakest_dimension": weakest[0]},
        "dimensions": [{"id": name, **d} for name, d in dims],
        "plan": {"P0": p0, "P1": p1, "P2": p2}
    }

def create_session_bridge():
    """Generate agent-progress.json template"""
    template = {
        "_说明": "Agent Session 状态桥。每次 session 启动时读取，结束时更新。JSON 格式防止 agent 误改结构。",
        "schemaVersion": "1.0",
        "lastSession": {
            "timestamp": None,
            "trigger": None,
            "summary": "首次初始化",
            "smokeTest": None,
            "result": "pending"
        },
        "taskTracking": {
            "_说明": "每完成一个任务后在此更新。status: pending|in_progress|done|failed",
            "recentCompleted": []
        },
        "environmentStatus": {
            "lastChecked": None,
            "result": None,
            "notes": None
        },
        "knownIssues": []
    }
    PROGRESS_FILE.write_text(json.dumps(template, indent=2))
    return {"created": str(PROGRESS_FILE)}

def fix_startup_sequence():
    """Insert fixed startup sequence into AGENTS.md if missing"""
    if not AGENTS_FILE.exists():
        return {"error": "AGENTS.md not found"}
    content = AGENTS_FILE.read_text()
    if "## Session Startup" in content and "Step 1" in content:
        return {"skipped": "already present"}
    # Find insertion point after "## Session Startup" or at end of file
    insertion = """\n### Fixed Startup Sequence (must run on every session)

1. Read `agent-progress.json` to understand last session state
2. Perform smoke test (verify gateway/API/network)
3. Load session bridge and continue from last checkpoint
4. Execute tasks with atomic commit after each

"""
    # Append after existing Session Startup section if exists, else at end
    if "## Session Startup" in content:
        parts = content.split("## Session Startup", 1)
        after = parts[1]
        # Find next section or end
        next_section = after.find("\n## ")
        if next_section != -1:
            new_content = parts[0] + "## Session Startup" + after[:next_section] + insertion + after[next_section:]
        else:
            new_content = parts[0] + "## Session Startup" + after + insertion
    else:
        new_content = content + "\n## Session Startup\n" + insertion
    AGENTS_FILE.write_text(new_content)
    return {"updated": str(AGENTS_FILE)}

def apply_fix(fix_id):
    if fix_id == "create_session_bridge":
        return create_session_bridge()
    elif fix_id == "fix_startup_sequence":
        return fix_startup_sequence()
    else:
        return {"error": f"unknown fix_id: {fix_id}"}

def main():
    if len(sys.argv) < 2:
        print("Usage: run.py [harness_check|apply_fix] [json_input]")
        sys.exit(1)
    
    action = sys.argv[1]
    input_data = json.loads(sys.argv[2]) if len(sys.argv) > 2 else {}
    
    if action == "harness_check":
        result = run_diagnostic()
        # If fix_apply provided, apply those fixes automatically
        fix_ids = input_data.get("fix_apply", [])
        if fix_ids:
            applied = []
            for fid in fix_ids:
                res = apply_fix(fid)
                if "error" not in res:
                    applied.append(fid)
                else:
                    res["applied"] = False
            result["applied_fixes"] = applied
        print(json.dumps(result, indent=2, ensure_ascii=False))
    elif action == "apply_fix":
        fix_id = input_data.get("fix_id")
        if not fix_id:
            print(json.dumps({"error": "fix_id required"}))
            sys.exit(1)
        result = apply_fix(fix_id)
        print(json.dumps(result))
    else:
        print(json.dumps({"error": "unknown action"}))
        sys.exit(1)

if __name__ == "__main__":
    main()
