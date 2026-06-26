---
name: claude-handoff
version: 1.0.0
description: |
  Writes a structured handoff package when local agent determines cloud
  Claude Code is needed. This is the ONLY path from local pipeline to cloud —
  the agent never auto-invokes Claude. The user reviews the handoff, decides
  whether to run Claude Code, and retains full control over Max quota spend.
triggers:
  - hard gate hit (iOS .swift file in scope)
  - soft gate exceeded (escalation score >= 8)
  - build feedback exhausted (3 failed iterations)
  - reflection confidence LOW after max passes
  - explicit user request: "hand this to Claude"
tools:
  - file-system
  - shell
  - notify
inputs:
  - task: original user request
  - reason: why we're escalating ("hard_gate" | "build_failed" | "reflection_low_confidence" | "user_request")
  - context_gathered: RAG chunks, file reads, investigation done so far
  - proposed_approach: plan from decompose-plan (if any)
  - build_errors: remaining compiler errors (if build_failed)
  - critique_history: findings from reflection passes (if any)
  - files_in_scope: list of affected file paths
outputs:
  - handoff_path: path to written handoff.md
  - command: ready-to-paste claude command
  - summary: one-sentence description for user
metadata:
  openclaw:
    category: coding
    tags:
      - coding
      - handoff
      - escalation
      - claude-code
    requires_openclaw: ">=2026.3.31"
    binaries:
      - python3
---

# Claude Code Handoff

## The principle: never auto-invoke Claude

Claude Max quota is finite. Auto-invoking on every hard task burns it
unnecessarily and removes user control. This skill ALWAYS produces a file
and notifies the user — it never calls the Claude API directly.

The user reviews the handoff, decides if they want to spend quota on it,
then runs Claude Code themselves. This is the contract.

## Handoff package format

Written to `{project_root}/.openclaw-skills/handoffs/{timestamp}-{slug}.md`

```markdown
---
timestamp: 2026-04-21T14:32:18Z
task_slug: add-swiftdata-cloudkit-migration
reason: iOS domain (hard gate)
orchestrator_version: 1.0.0
local_model: m27-jangtq-crack
---

# Handoff: Add SwiftData + CloudKit migration for iOS 26

## Original request
[verbatim user request]

## Why this is being handed off
**Reason**: iOS domain hard gate

Local M2.7 JANGTQ-CRACK's Swift training data is stale on SwiftData + CloudKit
migrations for iOS 26. This is a case where Claude Sonnet 4.6's more recent
training plus 1M context beats retrieved RAG snippets.

## Context gathered locally

### Files read
- `App/AppDelegate.swift` (112 lines)
- `Models/User.swift` (48 lines)
- `Models/UserDataSource.swift` (204 lines)
- `Views/ContentView.swift` (89 lines)

### Codebase patterns identified
- Project uses SwiftData with `@Model` macro
- Existing SwiftData stack in `Models/UserDataSource.swift:42`
- No CloudKit integration yet
- Deployment target: iOS 18, need to upgrade to iOS 26 first

### Relevant Apple documentation retrieved
1. [SwiftData CloudKit integration guide (iOS 26)](ref-link)
2. [iOS 26 migration patterns for SwiftData](ref-link)
3. [CloudKit schema synchronization](ref-link)

### Related Stack Overflow patterns
[if any]

## Proposed approach (from local planning)

Sub-problems identified:
1. **Update deployment target to iOS 26** (AppDelegate, Info.plist)
2. **Add CloudKit entitlement** (project settings)
3. **Migrate UserDataSource to use CloudKit-backed ModelContainer**
   - Depends on sub-problem 1
4. **Add migration plan for existing local data**
   - Depends on sub-problem 3
5. **Update Views to handle CloudKit sync state**
   - Depends on sub-problem 3

APIs involved:
- `ModelConfiguration(cloudKitDatabase:)` — iOS 26+
- `CKContainer.applicationDefault()` — iOS 8+
- `SchemaMigrationPlan` — iOS 26+

Risks:
- HIGH: Existing local user data could be lost if migration not handled
- MEDIUM: CloudKit development vs production environment confusion
- LOW: iOS version compatibility for existing users on < 26

## What local attempted and failed

[if build_failed]
Generated code that attempted the migration. Compile errors:
- Error 1: `cannot find 'cloudKitDatabase' in scope at ModelConfiguration.swift:12`
  (Fixed in iteration 2 — was missing import)
- Error 2: `'SchemaMigrationPlan' is only available in iOS 26.0 or newer`
  (Unable to fix — need guidance on availability strategy)

## Suggested Claude Code prompt

Copy-paste this into Claude Code:

```
Read /Users/stephen/projects/myapp/.openclaw-skills/handoffs/2026-04-21T14:32:18Z-add-swiftdata-cloudkit-migration.md

Then implement the 5 sub-problems in order. You have write access to the
project. Run `swift build` after each sub-problem to verify.

When done, produce a summary of what changed and any remaining concerns.
```

Or run from terminal:
```bash
cd /Users/stephen/projects/myapp
claude "Read .openclaw-skills/handoffs/2026-04-21T14:32:18Z-add-swiftdata-cloudkit-migration.md and implement the plan"
```

## Estimated Claude quota cost
Based on context size: ~12K input tokens + ~8K output = ~20K tokens.
Sonnet 4.6: ~20K × $3/$15 per MTok = ~$0.15 in direct API equivalent.
Via Max plan: draws modestly from your daily quota.

---
*Generated by coding-orchestrator v1.0.0*
```

## Execution

```python
import asyncio
import json
import re
from pathlib import Path
from datetime import datetime, timezone


HANDOFF_TEMPLATE = """---
timestamp: {timestamp}
task_slug: {slug}
reason: {reason_detail}
orchestrator_version: 1.0.0
local_model: m27-jangtq-crack
---

# Handoff: {task_title}

## Original request
{task}

## Why this is being handed off
**Reason**: {reason_detail}

{reason_explanation}

## Context gathered locally

### Files read
{files_read_section}

### Codebase patterns identified
{patterns_section}

### Relevant documentation retrieved
{docs_section}

## Proposed approach (from local planning)
{plan_section}

## What local attempted and failed
{attempt_section}

## Suggested Claude Code prompt

Copy-paste this into Claude Code:

```
Read {handoff_path}

Then implement the plan above. You have write access to the project.
{execution_guidance}

When done, produce a summary of what changed and any remaining concerns.
```

Or run from terminal:
```bash
cd {project_root}
claude "Read {handoff_path_relative} and implement the plan"
```

## Estimated Claude quota cost
Based on context size: ~{input_tokens}K input + ~{output_tokens}K output = ~{total_tokens}K tokens.

---
*Generated by coding-orchestrator v1.0.0*
"""


REASON_EXPLANATIONS = {
    "hard_gate": """Local M2.7 JANGTQ-CRACK's Swift training data is 2+ years stale.
iOS/Swift work consistently benefits from Sonnet 4.6's more recent training
and deeper Apple framework knowledge.""",

    "build_failed": """Local model generated code that failed to compile after 3
iterations. The remaining errors suggest the model is missing context that
isn't in our RAG — likely an API interaction or constraint not present in
training or retrieved docs.""",

    "reflection_low_confidence": """After reflection passes, local model's confidence
in its own output is LOW. This usually means the model recognizes the code
might work but isn't sure — a strong signal to get a second opinion.""",

    "user_request": """User explicitly requested Claude Code handoff.""",

    "context_overflow": """Task requires more context than M2.7's practical window can
accommodate. Sonnet 4.6's 1M context is the right tool.""",

    "soft_gate": """Escalation score exceeded threshold based on task complexity,
file count, and uncertainty signals.""",
}


async def claude_handoff(
    task: str,
    reason: str,
    context_gathered: dict = None,
    proposed_approach: dict = None,
    build_errors: list = None,
    critique_history: list = None,
    files_in_scope: list = None,
    project_root: str = None,
):
    timestamp = datetime.now(timezone.utc).isoformat()
    slug = _slugify(task)[:50]
    project_root = Path(project_root or ".")

    # Build each section
    sections = {
        "timestamp": timestamp,
        "slug": slug,
        "reason_detail": _reason_to_human(reason),
        "reason_explanation": REASON_EXPLANATIONS.get(reason, ""),
        "task": task,
        "task_title": _summarize_task(task),
        "files_read_section": _format_files(context_gathered),
        "patterns_section": _format_patterns(context_gathered),
        "docs_section": _format_docs(context_gathered),
        "plan_section": _format_plan(proposed_approach),
        "attempt_section": _format_attempt(build_errors, critique_history),
        "input_tokens": _estimate_input_tokens(context_gathered, proposed_approach) // 1000,
        "output_tokens": 8,
        "total_tokens": 20,
        "execution_guidance": _execution_guidance(proposed_approach, files_in_scope),
    }

    # Write handoff file
    handoff_dir = project_root / ".openclaw-skills" / "handoffs"
    handoff_dir.mkdir(parents=True, exist_ok=True)
    handoff_path = handoff_dir / f"{timestamp.replace(':', '-')}-{slug}.md"

    sections["handoff_path"] = str(handoff_path.absolute())
    sections["handoff_path_relative"] = str(handoff_path.relative_to(project_root))
    sections["project_root"] = str(project_root.absolute())

    content = HANDOFF_TEMPLATE.format(**sections)
    handoff_path.write_text(content)

    # Build the paste-ready command
    command = (
        f'cd {project_root.absolute()} && '
        f'claude "Read {sections["handoff_path_relative"]} and implement the plan"'
    )

    # Summary for user notification
    summary = f"Handoff ready: {_summarize_task(task)} → Claude Code"

    # Notify user via OpenClaw messaging channels
    await notify_user(
        title="🤖 Claude Code handoff ready",
        body=f"{summary}\n\nPath: {sections['handoff_path_relative']}\n\n"
             f"Run: {command}",
        level="info"
    )

    return {
        "handoff_path": str(handoff_path.absolute()),
        "command": command,
        "summary": summary
    }


def _slugify(text):
    """Convert task text to filesystem-safe slug."""
    slug = re.sub(r'[^\w\s-]', '', text.lower())
    slug = re.sub(r'[\s_-]+', '-', slug)
    return slug.strip('-')


def _reason_to_human(reason):
    mapping = {
        "hard_gate": "iOS domain (hard gate)",
        "build_failed": "Build errors unfixable locally",
        "reflection_low_confidence": "Low reflection confidence",
        "user_request": "User requested handoff",
        "context_overflow": "Task exceeds local context",
        "soft_gate": "Complexity threshold exceeded",
    }
    return mapping.get(reason, reason)


def _summarize_task(task):
    """Extract first sentence or 80 chars for title."""
    first_sentence = task.split('.')[0].strip()
    if len(first_sentence) > 80:
        return first_sentence[:77] + "..."
    return first_sentence


def _format_files(ctx):
    if not ctx or "files_read" not in ctx:
        return "(none)"
    lines = []
    for f in ctx["files_read"]:
        if isinstance(f, dict):
            lines.append(f"- `{f['path']}` ({f.get('lines', '?')} lines)")
        else:
            lines.append(f"- `{f}`")
    return "\n".join(lines)


def _format_patterns(ctx):
    if not ctx or "patterns" not in ctx:
        return "(none identified)"
    return "\n".join(f"- {p}" for p in ctx["patterns"])


def _format_docs(ctx):
    if not ctx or "retrieved_docs" not in ctx:
        return "(none retrieved)"
    return "\n".join(
        f"{i+1}. {d.get('title', d['url'])}"
        for i, d in enumerate(ctx["retrieved_docs"])
    )


def _format_plan(plan):
    if not plan:
        return "(no plan developed — task escalated before planning)"

    output = ["Sub-problems identified:"]
    for i, sp in enumerate(plan.get("sub_problems", []), 1):
        output.append(f"{i}. **{sp['title']}**")
        output.append(f"   {sp.get('description', '')}")
        if sp.get("depends_on"):
            output.append(f"   Depends on: {', '.join(sp['depends_on'])}")
        output.append("")

    if plan.get("apis"):
        output.append("\nAPIs involved:")
        for api in plan["apis"]:
            output.append(f"- `{api['name']}` — {api.get('version_requirement', 'any')}")

    if plan.get("risks"):
        output.append("\nRisks:")
        for r in plan["risks"]:
            output.append(f"- {r.get('severity', 'MEDIUM').upper()}: {r['risk']}")
            if r.get("mitigation"):
                output.append(f"  Mitigation: {r['mitigation']}")

    return "\n".join(output)


def _format_attempt(build_errors, critique_history):
    if not build_errors and not critique_history:
        return "(no prior attempts — escalated before code generation)"

    output = []
    if build_errors:
        output.append("Build errors remaining after fix attempts:")
        for err in build_errors[:10]:  # cap at 10
            output.append(f"- `{err['file']}:{err['line']}`: {err['message']}")
        if len(build_errors) > 10:
            output.append(f"- ... and {len(build_errors) - 10} more")

    if critique_history:
        output.append("\nReflection pass findings:")
        for pass_result in critique_history:
            output.append(f"\n**Pass {pass_result['pass']}**:")
            output.append(pass_result['critique'][:500])

    return "\n".join(output)


def _execution_guidance(plan, files):
    if not plan:
        return "Investigate the codebase, form a plan, then implement."

    order = plan.get("order", [])
    if order:
        return f"Implement the {len(order)} sub-problems in the listed order. "\
               f"Run tests after each sub-problem."
    return "Implement the proposed approach."


def _estimate_input_tokens(ctx, plan):
    """Rough token estimate for quota budgeting."""
    total = 1000  # base overhead
    if ctx:
        for f in ctx.get("files_read", []):
            total += f.get("lines", 100) * 8  # ~8 tokens per line
        for d in ctx.get("retrieved_docs", []):
            total += 500
    if plan:
        total += 1000
    return total


async def notify_user(title, body, level="info"):
    """Send notification via OpenClaw's messaging channels."""
    # OpenClaw notifies via WhatsApp, Telegram, Discord based on user config
    await openclaw.notify(title=title, body=body, level=level)
    # Also write to a dashboard file for status checking
    status_file = Path(".openclaw-skills/last_notification.json")
    status_file.write_text(json.dumps({
        "title": title, "body": body, "timestamp": datetime.now().isoformat()
    }))
```

## Integration with other skills

- Invoked by `coding-orchestrator` at multiple points (hard gate, after
  failed build, after failed reflection)
- Reads context from `task.scratchpad` populated by earlier steps
- Writes to project's `.openclaw-skills/handoffs/` directory
- Adds entry to global handoff log at `~/.openclaw-skills/handoff-log.sqlite`

## Handoff log for analytics

Every handoff gets logged to SQLite:

```sql
CREATE TABLE handoff_log (
    id INTEGER PRIMARY KEY,
    timestamp TEXT NOT NULL,
    task_slug TEXT NOT NULL,
    reason TEXT NOT NULL,
    project_root TEXT,
    estimated_tokens INTEGER,
    user_ran_claude BOOLEAN,  -- updated when user runs claude
    claude_succeeded BOOLEAN,  -- updated manually or via claude output log
    notes TEXT
);
```

Query this log periodically to understand your escalation patterns:
- Which reasons are most common? (if "build_failed" dominates, improve
  your iOS system prompt or RAG)
- How often do handoffs actually get run? (if low, your escalation threshold
  is too aggressive)
- How often does Claude Code succeed? (if it fails too, the task genuinely
  needs architectural input from you)

## What handoff does NOT do

- Does not execute Claude Code
- Does not read your Claude Max quota
- Does not cache or share handoffs between users
- Does not modify source code (only writes to `.openclaw-skills/handoffs/`)

These are all explicit user actions. The skill's job is to prepare the best
possible brief and then step aside.
