#!/usr/bin/env python3
"""Forge 🔨 — 维修-监理自动循环编排器

通用的repair-inspect loop，任何项目都能用。
脚本做编排（依赖分析、状态管理、安全检查），LLM做执行（repair/inspect）。

用法:
    python3 forge.py init --workdir /path/to/project
    python3 forge.py add "任务描述" --criteria "验收标准" [--depends task-1]
    python3 forge.py plan                # 依赖分析，输出执行计划
    python3 forge.py run                 # 推进下一批任务
    python3 forge.py status              # 查看进度
    python3 forge.py advance TASK_ID     # 手动推进指定任务
    python3 forge.py reset               # 清除状态

状态持久化到 forge-state.json，支持断点恢复。

Author: Forge Contributors
"""

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

# ── 路径 ──────────────────────────────────────────────────────
FORGE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = FORGE_DIR / "assets" / "templates"

# ── 常量 ──────────────────────────────────────────────────────
MAX_ROUNDS = 5
REPAIR_TIMEOUT = 600
INSPECT_TIMEOUT = 300
DEFAULT_MODEL = "anthropic/claude-opus-4-6"


# ══════════════════════════════════════════════════════════════
# Experience Accumulation
# ══════════════════════════════════════════════════════════════

def extract_universal_pattern(project_pattern: dict) -> Optional[dict]:
    """Extract a universal (project-agnostic) pattern from a project-specific repair pattern.

    Strips file paths, project-specific names, and keeps only the abstract lesson.
    Returns None if the pattern is too project-specific to generalize.
    """
    name = project_pattern.get("pattern_name", "")
    if not name:
        return None

    # Extract generalizable fields
    universal = {
        "pattern_name": name,
        "error_type": project_pattern.get("error_type", ""),
        "solution_template": project_pattern.get("solution_template", ""),
        "prevention": project_pattern.get("prevention", ""),
    }

    # Strip empty fields
    universal = {k: v for k, v in universal.items() if v}
    if "pattern_name" not in universal:
        return None

    # Skip patterns that are purely project-specific (heuristic: if solution_template
    # contains too many specific file paths, it's not universal)
    template = universal.get("solution_template", "")
    path_indicators = [".py", ".sh", ".json", ".yaml", "scripts/", "cache/", "prompts/"]
    path_count = sum(1 for ind in path_indicators if ind in template)
    if path_count >= 3 and len(template) < 200:
        # Too many paths in a short template = project-specific
        return None

    return universal


# ══════════════════════════════════════════════════════════════
# State Management
# ══════════════════════════════════════════════════════════════

def state_path(workdir: Path) -> Path:
    return workdir / "forge-state.json"


def load_state(workdir: Path) -> Optional[dict]:
    sf = state_path(workdir)
    if sf.exists():
        try:
            with open(sf) as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"🚨 状态文件损坏: {sf}")
            print(f"   用 'forge.py reset' 清除后重新开始")
            sys.exit(1)
    return None


def save_state(workdir: Path, state: dict):
    state["updated_at"] = datetime.now().isoformat()
    with open(state_path(workdir), 'w') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def init_state(workdir: Path, project_name: str = "") -> dict:
    state = {
        "project": project_name or workdir.name,
        "workdir": str(workdir),
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "tasks": {},
        "task_counter": 0,
        "protected_files": load_protected_files(workdir),
        "config": {
            "max_rounds": MAX_ROUNDS,
            "repair_timeout": REPAIR_TIMEOUT,
            "inspect_timeout": INSPECT_TIMEOUT,
            "model": DEFAULT_MODEL,
            "auto_commit": True,
        },
    }
    save_state(workdir, state)
    return state


# ══════════════════════════════════════════════════════════════
# Protected Files
# ══════════════════════════════════════════════════════════════

def load_protected_files(workdir: Path) -> list:
    """Load protected files list if exists in project."""
    pf = workdir / "protected-files.txt"
    if not pf.exists():
        return []
    lines = pf.read_text().strip().split("\n")
    return [l.strip() for l in lines
            if l.strip() and not l.strip().startswith("#")]


def check_protected_files(workdir: Path, changed_files: list, protected: list) -> list:
    """Check if any changed files are protected. Returns list of violations."""
    violations = []
    for cf in changed_files:
        for pf in protected:
            cf_norm = os.path.normpath(cf.strip())
            pf_norm = os.path.normpath(pf.strip())
            if cf_norm == pf_norm or cf_norm.endswith(os.sep + pf_norm):
                violations.append(cf_norm)
    return violations


# ══════════════════════════════════════════════════════════════
# Task Management
# ══════════════════════════════════════════════════════════════

def add_task(state: dict, description: str, criteria: str = "",
             depends: list = None, priority: str = "P1",
             source: str = "", files_hint: list = None) -> str:
    """Add a repair task. Returns task_id."""
    state["task_counter"] += 1
    task_id = f"task-{state['task_counter']:03d}"

    state["tasks"][task_id] = {
        "id": task_id,
        "description": description,
        "criteria": criteria or "修复后代码能正确运行，无回归问题",
        "priority": priority,
        "source": source,
        "files_hint": files_hint or [],
        "depends_on": depends or [],
        "status": "pending",
        "current_round": 0,
        "rounds": [],
        "created_at": datetime.now().isoformat(),
        "completed_at": None,
        "result": None,
    }
    return task_id


def get_parallel_groups(state: dict) -> list:
    """Topological sort tasks into parallel execution groups."""
    tasks = state["tasks"]
    remaining = {tid for tid, t in tasks.items()
                 if t["status"] in ("pending", "repair_needed")}
    done = {tid for tid, t in tasks.items()
            if t["status"] in ("done", "skipped")}
    groups = []

    while remaining:
        # Find tasks whose deps are all in 'done'
        group = []
        for tid in list(remaining):
            task = tasks[tid]
            deps = set(task.get("depends_on", []))
            if deps.issubset(done):
                group.append(tid)

        if not group:
            # Circular dependency or blocked
            groups.append({"type": "blocked", "tasks": list(remaining)})
            break

        groups.append({"type": "parallel", "tasks": group})
        for tid in group:
            remaining.discard(tid)
            done.add(tid)

    return groups


# ══════════════════════════════════════════════════════════════
# Prompt Generation
# ══════════════════════════════════════════════════════════════

def load_template(name: str) -> str:
    """Load a prompt template."""
    template_file = TEMPLATES_DIR / f"{name}.md"
    if template_file.exists():
        return template_file.read_text()
    # Fallback to inline template
    return ""


def generate_repair_task(task: dict, state: dict, inspector_issues: str = "") -> str:
    """Generate a repair engineer spawn task."""
    workdir = state["workdir"]
    protected = state.get("protected_files", [])
    round_num = task["current_round"]

    protected_text = ""
    if protected:
        protected_text = "\n".join(f"  - {f}" for f in protected)
        protected_text = f"""
## 🔒 受保护文件（禁止修改）
以下文件在自动循环中禁止修改。如需改动，输出 BLOCKED 并说明原因。
{protected_text}
"""

    files_hint = ""
    if task.get("files_hint"):
        files_hint = "\n## 相关文件提示\n" + "\n".join(f"- {f}" for f in task["files_hint"])

    prev_issues = ""
    if inspector_issues:
        prev_issues = f"""
## 上轮监理反馈（第{round_num}轮）
{inspector_issues}

请针对上述问题逐一修复。
"""

    # Load reflections: universal patterns (cross-project) + project-specific
    reflections_text = ""
    universal_reflections_file = FORGE_DIR / "reflections" / "patterns.jsonl"
    project_reflections_file = Path(workdir) / "forge-reflections.jsonl"

    patterns = []
    # Universal layer first (cross-project lessons)
    if universal_reflections_file.exists():
        try:
            for line in universal_reflections_file.read_text().strip().split("\n")[-5:]:
                if line.strip():
                    patterns.append(("通用", json.loads(line)))
        except Exception:
            pass
    # Project layer (project-specific patterns)
    if project_reflections_file.exists():
        try:
            for line in project_reflections_file.read_text().strip().split("\n")[-5:]:
                if line.strip():
                    patterns.append(("项目", json.loads(line)))
        except Exception:
            pass

    if patterns:
        reflections_text = "\n## 历史修复经验\n"
        for layer, r in patterns:
            name = r.get('pattern_name', '?')
            template = r.get('solution_template', r.get('description', ''))
            reflections_text += f"- **{name}**: {template}\n"

    return f"""你是维修工程师（Repair Engineer）。

## 修复任务
{task['description']}

## 验收标准
{task['criteria']}
{prev_issues}{protected_text}{files_hint}{reflections_text}
## 安全规则（不可违反）
- 🚫 禁止删除任何文件（用 # DEPRECATED 标记）
- 🚫 禁止修改受保护文件（见上方列表）
- 🚫 禁止修改 cron 配置
- ✅ 只能修改任务描述中明确涉及的文件
- ✅ 用 edit 工具精确修改，不要重写整个文件

## 输出格式
将修复报告写入文件: `{workdir}/forge-output/{task['id']}-repair-r{round_num}.json`

```json
{{
  "role": "repair_engineer",
  "task_id": "{task['id']}",
  "round": {round_num},
  "repairs": [
    {{
      "title": "修复标题",
      "status": "FIXED / PARTIAL / BLOCKED / SKIPPED",
      "diagnosis": {{ "root_cause": "根因", "affected_files": ["file.py"] }},
      "changes": [{{ "file": "path", "description": "改了什么" }}],
      "self_test": {{ "method": "自测方式", "result": "通过/失败", "evidence": "数据" }},
      "regression_risk": "low / medium / high"
    }}
  ],
  "repair_pattern": {{
    "error_type": "错误分类",
    "pattern_name": "简短模式名",
    "solution_template": "通用解决方案",
    "prevention": "预防措施"
  }},
  "summary": {{
    "fixed_count": 0,
    "blocked_count": 0,
    "total_files_changed": 0
  }}
}}
```

## 执行步骤
1. 读取相关文件，诊断根因
2. 用 edit 精确修改
3. 自测验证
4. 将修复报告JSON写入上述文件路径
5. 回复 "done"

工作目录: {workdir}
"""


def generate_inspect_task(task: dict, state: dict, repair_report: dict) -> str:
    """Generate an inspector spawn task."""
    workdir = state["workdir"]
    round_num = task["current_round"]

    # Summarize repair report
    repair_summary = json.dumps(repair_report, ensure_ascii=False, indent=2)
    if len(repair_summary) > 3000:
        # Truncate but keep structure
        repairs = repair_report.get("repairs", [])
        repair_summary = "修复摘要:\n"
        for r in repairs:
            repair_summary += f"- {r.get('title', '?')}: {r.get('status', '?')}\n"
            for c in r.get("changes", []):
                repair_summary += f"  改动: {c.get('file', '?')} — {c.get('description', '?')}\n"

    return f"""你是监理（Inspector），独立验收修复是否真正解决了问题。

## 原始问题
{task['description']}

## 验收标准
{task['criteria']}

## 维修工程师报告（第{round_num}轮）
{repair_summary}

## 验收要求
1. **必须跑代码验证** — 不接受"看起来对了"
2. 用 grep/python 做全量扫描，不抽样
3. 检查边缘情况和回归风险
4. 验证修复后代码实际能运行

## 输出格式
将验收报告写入文件: `{workdir}/forge-output/{task['id']}-inspect-r{round_num}.json`

```json
{{
  "role": "inspector",
  "task_id": "{task['id']}",
  "round": {round_num},
  "verdict": "PASS / FAIL / CONDITIONAL / NEEDS_HUMAN",
  "inspections": [
    {{
      "check": "检查内容",
      "method": "验证方法",
      "result": "通过/失败",
      "evidence": "实际输出"
    }}
  ],
  "issues_found": [
    {{
      "severity": "critical / warning / info",
      "description": "问题描述",
      "suggestion": "建议修复方式"
    }}
  ],
  "summary": "一句话结论"
}}
```

## 执行步骤
1. 读取维修工程师修改的文件
2. 运行代码验证输出
3. 检查边缘情况
4. 将验收报告JSON写入上述文件路径
5. 回复 "done"

工作目录: {workdir}
"""


# ══════════════════════════════════════════════════════════════
# Execution Flow
# ══════════════════════════════════════════════════════════════

def prepare_repair(state: dict, task_id: str) -> dict:
    """Prepare repair spawn instruction for a task."""
    task = state["tasks"][task_id]
    workdir = Path(state["workdir"])

    # Increment round
    task["current_round"] += 1
    task["status"] = "repairing"
    round_num = task["current_round"]

    # Get previous inspector issues if any
    inspector_issues = ""
    if task["rounds"]:
        last_round = task["rounds"][-1]
        if last_round.get("inspect_issues"):
            inspector_issues = last_round["inspect_issues"]

    # Generate task content
    task_content = generate_repair_task(task, state, inspector_issues)

    # Ensure output dir exists
    output_dir = workdir / "forge-output"
    output_dir.mkdir(parents=True, exist_ok=True)

    # Write task file
    task_file = output_dir / f"{task_id}-repair-r{round_num}.task.md"
    task_file.write_text(task_content)

    # Record round
    task["rounds"].append({
        "round": round_num,
        "repair_started": datetime.now().isoformat(),
        "repair_file": str(output_dir / f"{task_id}-repair-r{round_num}.json"),
        "inspect_file": str(output_dir / f"{task_id}-inspect-r{round_num}.json"),
        "repair_done": False,
        "inspect_done": False,
        "inspect_issues": "",
    })

    return {
        "type": "repair",
        "task_id": task_id,
        "round": round_num,
        "task_file": str(task_file),
        "result_file": str(output_dir / f"{task_id}-repair-r{round_num}.json"),
        "label": f"forge-repair-{task_id}-r{round_num}",
        "model": state["config"]["model"],
        "timeout": state["config"]["repair_timeout"],
    }


def prepare_inspect(state: dict, task_id: str) -> dict:
    """Prepare inspector spawn instruction for a task."""
    task = state["tasks"][task_id]
    workdir = Path(state["workdir"])
    round_num = task["current_round"]

    # Load repair report
    current_round = task["rounds"][-1]
    repair_file = Path(current_round["repair_file"])
    repair_report = {}
    if repair_file.exists():
        try:
            repair_report = json.loads(repair_file.read_text())
        except json.JSONDecodeError:
            repair_report = {"error": "repair report JSON parse failed"}

    task["status"] = "inspecting"

    # Generate task content
    task_content = generate_inspect_task(task, state, repair_report)

    output_dir = workdir / "forge-output"
    task_file = output_dir / f"{task_id}-inspect-r{round_num}.task.md"
    task_file.write_text(task_content)

    return {
        "type": "inspect",
        "task_id": task_id,
        "round": round_num,
        "task_file": str(task_file),
        "result_file": str(output_dir / f"{task_id}-inspect-r{round_num}.json"),
        "label": f"forge-inspect-{task_id}-r{round_num}",
        "model": state["config"]["model"],
        "timeout": state["config"]["inspect_timeout"],
    }


def check_repair_result(state: dict, task_id: str) -> str:
    """Check if repair result is ready. Returns: ready/waiting/blocked."""
    task = state["tasks"][task_id]
    if not task["rounds"]:
        return "waiting"

    current_round = task["rounds"][-1]
    repair_file = Path(current_round["repair_file"])

    if not repair_file.exists():
        return "waiting"

    try:
        report = json.loads(repair_file.read_text())
    except json.JSONDecodeError:
        return "waiting"

    # Check if all repairs are BLOCKED
    repairs = report.get("repairs", [])
    if repairs and all(r.get("status") == "BLOCKED" for r in repairs):
        task["status"] = "needs_human"
        task["result"] = "ALL_BLOCKED"
        current_round["repair_done"] = True
        return "blocked"

    current_round["repair_done"] = True

    # Save repair pattern to reflections (two-layer)
    pattern = report.get("repair_pattern", {})
    if pattern and pattern.get("pattern_name"):
        # Project layer: full detail (file names, paths, project-specific context)
        project_reflections = Path(state["workdir"]) / "forge-reflections.jsonl"
        with open(project_reflections, "a") as f:
            f.write(json.dumps(pattern, ensure_ascii=False) + "\n")

        # Universal layer: extract abstract pattern (no project-specific paths/filenames)
        universal_pattern = extract_universal_pattern(pattern)
        if universal_pattern:
            universal_dir = FORGE_DIR / "reflections"
            universal_dir.mkdir(parents=True, exist_ok=True)
            universal_file = universal_dir / "patterns.jsonl"
            # Dedup: skip if pattern_name already exists
            existing_names = set()
            if universal_file.exists():
                try:
                    for line in universal_file.read_text().strip().split("\n"):
                        if line.strip():
                            existing_names.add(json.loads(line).get("pattern_name", ""))
                except Exception:
                    pass
            if universal_pattern["pattern_name"] not in existing_names:
                with open(universal_file, "a") as f:
                    f.write(json.dumps(universal_pattern, ensure_ascii=False) + "\n")

    return "ready"


def check_inspect_result(state: dict, task_id: str) -> str:
    """Check inspector result. Returns: pass/fail/needs_human/waiting."""
    task = state["tasks"][task_id]
    current_round = task["rounds"][-1]
    inspect_file = Path(current_round["inspect_file"])

    if not inspect_file.exists():
        return "waiting"

    try:
        report = json.loads(inspect_file.read_text())
    except json.JSONDecodeError:
        return "waiting"

    verdict = report.get("verdict", "").upper()
    current_round["inspect_done"] = True

    if verdict == "PASS":
        task["status"] = "done"
        task["completed_at"] = datetime.now().isoformat()
        task["result"] = "PASS"
        return "pass"

    elif verdict in ("FAIL", "CONDITIONAL"):
        # Extract issues for next round
        issues = report.get("issues_found", [])
        issues_text = "\n".join(
            f"- [{i.get('severity', '?')}] {i.get('description', '?')}\n  建议: {i.get('suggestion', '')}"
            for i in issues
        )
        if not issues_text:
            issues_text = report.get("summary", "监理判定未通过，但未提供具体issues")
        current_round["inspect_issues"] = issues_text

        # Check max rounds
        if task["current_round"] >= state["config"]["max_rounds"]:
            task["status"] = "escalated"
            task["result"] = f"ESCALATED_AFTER_{MAX_ROUNDS}_ROUNDS"
            return "escalated"

        task["status"] = "repair_needed"
        return "fail"

    elif verdict == "NEEDS_HUMAN":
        task["status"] = "needs_human"
        task["result"] = "NEEDS_HUMAN"
        current_round["inspect_issues"] = report.get("summary", "需要人工判断")
        return "needs_human"

    return "waiting"


def run_advance(state: dict) -> list:
    """Advance the forge state machine. Returns spawn instructions."""
    workdir = Path(state["workdir"])
    spawn_instructions = []

    for tid, task in state["tasks"].items():
        status = task["status"]

        if status == "pending":
            # Check dependencies
            deps_met = all(
                state["tasks"].get(dep, {}).get("status") in ("done", "skipped")
                for dep in task.get("depends_on", [])
            )
            if deps_met:
                inst = prepare_repair(state, tid)
                spawn_instructions.append(inst)

        elif status == "repair_needed":
            inst = prepare_repair(state, tid)
            spawn_instructions.append(inst)

        elif status == "repairing":
            result = check_repair_result(state, tid)
            if result == "ready":
                inst = prepare_inspect(state, tid)
                spawn_instructions.append(inst)
            elif result == "blocked":
                print(f"  🚧 {tid}: 全部BLOCKED，需要人工介入")

        elif status == "inspecting":
            result = check_inspect_result(state, tid)
            if result == "pass":
                print(f"  ✅ {tid}: 监理通过!")
            elif result == "fail":
                # Auto-loop: prepare next repair round
                inst = prepare_repair(state, tid)
                spawn_instructions.append(inst)
                print(f"  🔄 {tid}: 第{task['current_round']}轮修复（监理不通过）")
            elif result == "needs_human":
                print(f"  🚨 {tid}: 需要人工判断")
            elif result == "escalated":
                print(f"  ⬆️ {tid}: {MAX_ROUNDS}轮未收敛，升级给人")

    save_state(workdir, state)

    # Detect stuck tasks (possible circular dependency)
    if not spawn_instructions:
        stuck = [tid for tid, t in state["tasks"].items()
                 if t["status"] in ("pending", "repair_needed")]
        if stuck:
            print(f"\n  ⚠️ {len(stuck)} 个任务无法推进（可能存在循环依赖）")
            print(f"     运行 'forge.py plan' 查看依赖关系")

    return spawn_instructions


# ══════════════════════════════════════════════════════════════
# Safety Checks (pre-commit)
# ══════════════════════════════════════════════════════════════

def pre_commit_check(state: dict) -> dict:
    """Run pre-commit safety checks. Returns {safe: bool, violations: [], warnings: []}."""
    workdir = Path(state["workdir"])
    result = {"safe": True, "violations": [], "warnings": []}

    try:
        # Get staged changes
        diff_result = subprocess.run(
            ["git", "diff", "--cached", "--name-only"],
            capture_output=True, text=True, cwd=str(workdir)
        )
        changed = [f.strip() for f in diff_result.stdout.strip().split("\n") if f.strip()]

        if not changed:
            # Check unstaged too
            diff_result = subprocess.run(
                ["git", "diff", "--name-only"],
                capture_output=True, text=True, cwd=str(workdir)
            )
            changed = [f.strip() for f in diff_result.stdout.strip().split("\n") if f.strip()]

        # Check protected files
        protected = state.get("protected_files", [])
        violations = check_protected_files(workdir, changed, protected)
        if violations:
            result["safe"] = False
            result["violations"] = [f"受保护文件被修改: {v}" for v in violations]

        # Check deletions
        del_result = subprocess.run(
            ["git", "diff", "--diff-filter=D", "--name-only"],
            capture_output=True, text=True, cwd=str(workdir)
        )
        deleted = [f.strip() for f in del_result.stdout.strip().split("\n") if f.strip()]
        if deleted:
            result["safe"] = False
            result["violations"].append(f"文件被删除: {', '.join(deleted)}")

        # Check change size
        stat_result = subprocess.run(
            ["git", "diff", "--stat"],
            capture_output=True, text=True, cwd=str(workdir)
        )
        # Parse "X files changed, Y insertions, Z deletions"
        stat_line = stat_result.stdout.strip().split("\n")[-1] if stat_result.stdout.strip() else ""
        numbers = re.findall(r"(\d+)", stat_line)
        if numbers and len(numbers) >= 2:
            insertions = int(numbers[1]) if len(numbers) > 1 else 0
            if insertions > 500:
                result["warnings"].append(f"改动较大: {insertions} 行插入")

    except Exception as e:
        result["warnings"].append(f"安全检查异常: {e}")

    return result


# ══════════════════════════════════════════════════════════════
# Display
# ══════════════════════════════════════════════════════════════

def show_status(state: dict):
    """Display current forge status."""
    if not state:
        print("❌ 没有进行中的forge会话。用 'forge.py init' 开始。")
        return

    tasks = state.get("tasks", {})
    total = len(tasks)
    done = sum(1 for t in tasks.values() if t["status"] == "done")
    active = sum(1 for t in tasks.values()
                 if t["status"] in ("repairing", "inspecting"))
    blocked = sum(1 for t in tasks.values()
                  if t["status"] in ("needs_human", "escalated"))
    pending = sum(1 for t in tasks.values()
                  if t["status"] in ("pending", "repair_needed"))

    print(f"\n{'='*60}")
    print(f"🔨 Forge — {state['project']}")
    print(f"   工作目录: {state['workdir']}")
    print(f"   保护文件: {len(state.get('protected_files', []))} 个")
    print(f"   任务: {done}/{total} 完成  |  {active} 进行中  |  {blocked} 阻塞  |  {pending} 待处理")
    print(f"{'='*60}")

    for tid, task in sorted(tasks.items()):
        status = task["status"]
        icon = {
            "pending": "⬜",
            "repair_needed": "🔄",
            "repairing": "🔧",
            "inspecting": "🔍",
            "done": "🟩",
            "needs_human": "🚨",
            "escalated": "⬆️",
            "skipped": "⏭️",
        }.get(status, "❓")

        rounds = f" R{task['current_round']}" if task["current_round"] > 0 else ""
        priority = f" [{task['priority']}]" if task.get('priority') else ""
        deps = ""
        if task.get("depends_on"):
            deps = f" ← {','.join(task['depends_on'])}"

        desc = task["description"][:60]
        if len(task["description"]) > 60:
            desc += "..."

        print(f"  {icon} {tid}{priority}{rounds}: {desc}{deps}")

    # Show execution plan
    groups = get_parallel_groups(state)
    if groups and any(g["type"] == "parallel" for g in groups):
        print(f"\n  📋 执行计划:")
        for i, group in enumerate(groups, 1):
            task_ids = ", ".join(group["tasks"])
            if group["type"] == "blocked":
                print(f"    🚧 阻塞: {task_ids}")
            else:
                print(f"    Wave {i}: {task_ids} (并行)")


def format_spawn_instructions(instructions: list):
    """Format spawn instructions for LLM to execute."""
    if not instructions:
        print("\n  ℹ️ 没有需要spawn的任务")
        return

    print(f"\n{'='*60}")
    print(f"🚀 SPAWN指令 — {len(instructions)} 个任务:")
    print(f"{'='*60}")

    for i, inst in enumerate(instructions, 1):
        type_icon = "🔧" if inst["type"] == "repair" else "🔍"
        print(f"\n  [{i}/{len(instructions)}] {type_icon} {inst['label']}")
        print(f"    任务文件: {inst['task_file']}")
        print(f"    结果文件: {inst['result_file']}")
        print(f"    模型: {inst['model']}")
        print(f"    超时: {inst['timeout']}s")

    print(f"\n💡 执行方法:")
    print(f"   1. 读取任务文件内容")
    print(f"   2. sessions_spawn(task=内容, label=label, model=model)")
    print(f"   3. 等待完成（subagent写入result_file）")
    print(f"   4. 再次运行: python3 forge.py run")


def check_doc_sync(state: dict) -> list:
    """Check if any modified code files have related docs that need updating.

    Looks for doc-sync-manifest.yaml in the project root. If it exists,
    cross-references modified files against the manifest to find docs
    that may be out of date. Also runs doc-sync-checker.py if available.

    Returns list of warning strings (empty = all good).
    """
    workdir = Path(state["workdir"])
    warnings = []

    # Method 1: Run doc-sync-checker.py if it exists
    checker = workdir / "scripts" / "tools" / "doc-sync-checker.py"
    if checker.exists():
        try:
            result = subprocess.run(
                [sys.executable, str(checker), "--json"],
                capture_output=True, text=True, cwd=str(workdir), timeout=30
            )
            if result.returncode == 0 and result.stdout.strip():
                try:
                    report = json.loads(result.stdout.strip())
                    stale = report.get("stale", [])
                    for item in stale:
                        doc = item.get("doc", "?")
                        authority = item.get("authority", "?")
                        warnings.append(f"{doc} 可能落后于 {authority}")
                except json.JSONDecodeError:
                    pass
        except (subprocess.TimeoutExpired, Exception):
            pass

    # Method 2: Check manifest directly
    manifest_path = workdir / "references" / "doc-sync-manifest.yaml"
    if manifest_path.exists() and not warnings:
        try:
            import yaml  # noqa: E402
            manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
            facts = manifest.get("facts", {})

            # Get list of files modified in this forge session
            modified_files = set()
            for tid, task in state.get("tasks", {}).items():
                for rnd in task.get("rounds", []):
                    repair_file = rnd.get("repair_file", "")
                    if repair_file and Path(repair_file).exists():
                        try:
                            repair_data = json.loads(Path(repair_file).read_text())
                            for r in repair_data.get("repairs", []):
                                for c in r.get("changes", []):
                                    f = c.get("file", "")
                                    if f:
                                        modified_files.add(f)
                        except (json.JSONDecodeError, KeyError):
                            pass

            # Cross-reference: if any authority file was modified, flag its consumers
            for fact_name, fact_info in facts.items():
                authority = fact_info.get("authority", "")
                consumers = fact_info.get("consumers", [])
                if authority and any(authority in mf or mf in authority for mf in modified_files):
                    for consumer in consumers:
                        warnings.append(f"{consumer} 可能需要同步更新（{fact_name} 的权威源 {authority} 已修改）")
        except ImportError:
            pass  # No yaml module, skip manifest check
        except Exception:
            pass

    return warnings


def generate_summary(state: dict) -> str:
    """Generate completion summary."""
    tasks = state.get("tasks", {})
    lines = [f"🔨 Forge 完成报告 — {state['project']}\n"]

    for tid, task in sorted(tasks.items()):
        status_icon = {"done": "✅", "needs_human": "🚨", "escalated": "⬆️",
                       "skipped": "⏭️"}.get(task["status"], "❓")
        rounds = task["current_round"]
        lines.append(f"  {status_icon} {tid}: {task['description'][:50]} (R{rounds})")

    done_count = sum(1 for t in tasks.values() if t["status"] == "done")
    total = len(tasks)
    lines.append(f"\n  📊 {done_count}/{total} 任务完成")

    # Doc-sync check
    doc_warnings = check_doc_sync(state)
    if doc_warnings:
        lines.append(f"\n  📄 文档同步检查 — {len(doc_warnings)} 个文档可能需要更新:")
        for w in doc_warnings:
            lines.append(f"    ⚠️ {w}")
        lines.append(f"\n  💡 运行 doc-sync-checker.py 查看详情，或手动检查上述文档。")
    else:
        lines.append(f"\n  📄 文档同步检查 — ✅ 无需更新（或未配置 doc-sync-manifest.yaml）")

    return "\n".join(lines)


# ══════════════════════════════════════════════════════════════
# CLI
# ══════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="🔨 Forge — 维修-监理自动循环编排器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  forge.py init --workdir /path/to/project
  forge.py add "Fix null handling in data processor" --criteria "No crash on empty input"
  forge.py add "清理废弃collector" --depends task-001
  forge.py plan
  forge.py run
  forge.py status
  forge.py reset
        """)

    sub = parser.add_subparsers(dest="command")

    # init
    p_init = sub.add_parser("init", help="初始化forge会话")
    p_init.add_argument("--workdir", type=str, default=".", help="项目工作目录")
    p_init.add_argument("--project", type=str, default="", help="项目名称")
    p_init.add_argument("--model", type=str, default=DEFAULT_MODEL, help="LLM模型")
    p_init.add_argument("--max-rounds", type=int, default=MAX_ROUNDS, help="最大循环轮数")

    # add
    p_add = sub.add_parser("add", help="添加修复任务")
    p_add.add_argument("description", type=str, help="任务描述")
    p_add.add_argument("--criteria", type=str, default="", help="验收标准")
    p_add.add_argument("--depends", type=str, nargs="*", default=[], help="依赖任务ID")
    p_add.add_argument("--priority", type=str, default="P1",
                        choices=["P0", "P1", "P2"], help="优先级")
    p_add.add_argument("--source", type=str, default="", help="来源(如 GM-R4-003)")
    p_add.add_argument("--files", type=str, nargs="*", default=[], help="相关文件提示")

    # plan
    sub.add_parser("plan", help="显示执行计划（依赖分析）")

    # run
    sub.add_parser("run", help="推进任务（准备spawn或检查结果）")

    # status
    sub.add_parser("status", help="显示当前进度")

    # advance
    p_advance = sub.add_parser("advance", help="推进指定任务")
    p_advance.add_argument("task_id", type=str, help="任务ID")

    # reset
    sub.add_parser("reset", help="清除当前forge状态")

    # check
    sub.add_parser("check", help="运行commit前安全检查")

    # summary
    sub.add_parser("summary", help="生成完成报告")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    if args.command == "init":
        workdir = Path(args.workdir).resolve()
        if not workdir.exists():
            print(f"❌ 工作目录不存在: {workdir}")
            sys.exit(1)
        existing = load_state(workdir)
        if existing and any(t["status"] not in ("done", "skipped", "needs_human", "escalated")
                           for t in existing.get("tasks", {}).values()):
            print(f"⚠️ 当前有进行中的forge任务")
            print(f"   用 'forge.py reset' 先清除")
            sys.exit(1)
        state = init_state(workdir, args.project)
        state["config"]["model"] = args.model
        state["config"]["max_rounds"] = args.max_rounds
        save_state(workdir, state)
        print(f"✅ Forge已初始化: {state['project']}")
        print(f"   工作目录: {workdir}")
        print(f"   保护文件: {len(state['protected_files'])} 个")
        print(f"\n下一步: forge.py add \"任务描述\" --criteria \"验收标准\"")
        return

    if args.command == "reset":
        # Find workdir from existing state or cwd
        workdir = Path(".").resolve()
        sf = state_path(workdir)
        if sf.exists():
            sf.unlink()
            print("✅ Forge状态已清除")
        else:
            print("ℹ️ 没有进行中的forge会话")
        return

    # All other commands need state
    workdir = Path(".").resolve()
    state = load_state(workdir)

    if not state and args.command != "init":
        print("❌ 没有forge会话。先运行: forge.py init")
        sys.exit(1)

    if args.command == "add":
        tid = add_task(state, args.description, args.criteria,
                       args.depends, args.priority, args.source, args.files)
        save_state(workdir, state)
        print(f"✅ 任务已添加: {tid}")
        print(f"   描述: {args.description[:60]}")
        if args.depends:
            print(f"   依赖: {', '.join(args.depends)}")
        show_status(state)
        return

    if args.command == "plan":
        groups = get_parallel_groups(state)
        print(f"\n📋 执行计划 ({len(state['tasks'])} 个任务)")
        print(f"{'='*60}")
        for i, group in enumerate(groups, 1):
            if group["type"] == "blocked":
                tasks = ", ".join(group["tasks"])
                print(f"  🚧 阻塞 (循环依赖): {tasks}")
            else:
                print(f"\n  Wave {i} (并行):")
                for tid in group["tasks"]:
                    task = state["tasks"][tid]
                    print(f"    {tid} [{task['priority']}]: {task['description'][:50]}")
        return

    if args.command == "run":
        instructions = run_advance(state)
        save_state(workdir, state)
        show_status(state)
        if instructions:
            format_spawn_instructions(instructions)
        else:
            all_done = all(t["status"] in ("done", "skipped", "needs_human", "escalated")
                          for t in state["tasks"].values())
            if all_done:
                print("\n🎉 所有任务已处理完毕!")
                print(generate_summary(state))
        return

    if args.command == "status":
        show_status(state)
        return

    if args.command == "advance":
        task = state["tasks"].get(args.task_id)
        if not task:
            print(f"❌ 任务不存在: {args.task_id}")
            sys.exit(1)
        # Only advance the specified task (not all tasks)
        instructions = []
        tid = args.task_id
        status = task["status"]
        if status in ("pending", "repair_needed"):
            deps_met = all(
                state["tasks"].get(dep, {}).get("status") in ("done", "skipped")
                for dep in task.get("depends_on", [])
            )
            if deps_met:
                inst = prepare_repair(state, tid)
                instructions.append(inst)
            else:
                print(f"  ⏳ {tid}: 依赖未满足")
        elif status == "repairing":
            result = check_repair_result(state, tid)
            if result == "ready":
                inst = prepare_inspect(state, tid)
                instructions.append(inst)
            elif result == "blocked":
                print(f"  🚧 {tid}: 全部BLOCKED，需要人工介入")
            else:
                print(f"  ⏳ {tid}: 等待维修结果")
        elif status == "inspecting":
            result = check_inspect_result(state, tid)
            if result == "pass":
                print(f"  ✅ {tid}: 监理通过!")
            elif result == "fail":
                inst = prepare_repair(state, tid)
                instructions.append(inst)
                print(f"  🔄 {tid}: 第{task['current_round']}轮修复")
            elif result == "needs_human":
                print(f"  🚨 {tid}: 需要人工判断")
            elif result == "escalated":
                print(f"  ⬆️ {tid}: 超轮数，升级")
            else:
                print(f"  ⏳ {tid}: 等待监理结果")
        else:
            print(f"  {tid}: {status}")
        save_state(workdir, state)
        if instructions:
            format_spawn_instructions(instructions)
        return

    if args.command == "check":
        result = pre_commit_check(state)
        if result["safe"]:
            print("✅ 安全检查通过")
        else:
            print("🚨 安全检查失败:")
            for v in result["violations"]:
                print(f"  ❌ {v}")
        for w in result.get("warnings", []):
            print(f"  ⚠️ {w}")
        return

    if args.command == "summary":
        print(generate_summary(state))
        return


if __name__ == "__main__":
    main()
