# Workflows

Operational workflows for Agent OS.

---

## 1. Daily Light Check

**When**: Start of each agent session / daily automated check.

**Steps**:

1. Check `findings.jsonl` for open P0/P1 items
2. Verify the latest context pack covers upcoming work
3. Check for stale items (no update in >48h)
4. Flag any items needing human decision
5. If no issues: log "no new blockers" in session memory
6. If P0/P1 found: update findings or create new ones

**Output**: Brief status note in session memory; update mission control if significant changes.

---

## 2. Weekly Review

**When**: Once per week (recommended: end of work week).

**Steps**:

1. **Findings metrics**: Count new, fixed, verified, closed, deferred this week
2. **Repeated issues**: Check for recurring patterns (same repo, same category)
3. **Context pack quality**: Were packs actually read and useful?
4. **Mission control coverage**: Was it generated daily?
5. **Flight recorder coverage**: Are key runs being recorded?
6. **Experience log review**: Any learnings ready for promotion?

**Output**: Weekly review memo; update roadmap if needed.

---

## 3. Upgrade Self-Check

**When**: Before adding new directories, schemas, automations, or collaboration rules.

**Before upgrading**:

1. Read the current directory protocol in `SKILL.md`
2. Check for existing mechanisms that solve the same problem
3. Verify the change is backward-compatible

**During upgrade**:

1. New files must have clear: owner, inputs, outputs, consumer
2. Schema changes must be backward-compatible or include migration notes
3. All human-facing output defaults to the workspace language

**After upgrade**:

1. Update `CHANGELOG.md`
2. Regenerate mission control to reflect behavior changes
3. If new data directory added, update schemas in `references/schemas.md`

---

## 4. Compile Context Pack (Workflow)

**When**: At session start or before agent handoff.

**Steps**:

1. Read `findings.jsonl` — extract open P0/P1 relevant to the task
2. Read the latest mission control
3. Scan workspace for relevant recent changes
4. Identify must-read files for the upcoming task
5. List forbidden actions (from findings, rules, or human instructions)
6. Define expected output
7. Write to `.agent-os/context-packs/YYYY-MM-DD-<label>.md`

**Script**: `scripts/compile_context_pack.py` automates steps 1-7.

---

## 5. Record Flight (Workflow — MVP)

**When**: After any significant agent run (automation, handoff, audit).

**Steps**:

1. Document the run ID, agent name, and task
2. List inputs consumed (context packs, findings, files)
3. Record key decisions and reasoning
4. List files changed and commands run
5. Note verification steps and results
6. Record any failures or anomalies
7. Note downstream impact
8. Append as JSONL line to `.agent-recorder/YYYY-MM-DD.jsonl`

**Template**: See `references/templates.md` → Flight Record.

**Script**: Planned for v0.2.0.

---

## 6. Compress Decisions (Workflow — MVP)

**When**: When the human has pending action items from multiple sources.

**Steps**:

1. Scan open findings with `owner` = human
2. Check mission control for items requiring human intervention
3. For each item, determine:
   - Is this a real decision or can the agent handle it?
   - What happens if it's deferred?
   - What's the recommended action?
4. Group into 1-3 decision briefs maximum
5. Write into the "Human Decisions Needed" section of mission control

**Template**: See `references/templates.md` → Decision Brief.

**Script**: Planned for v0.2.0.

---

## 7. Promote Learning (Workflow — MVP)

**When**: After resolving a finding, fixing a recurring issue, or discovering a non-obvious constraint.

**Steps**:

1. Write a concise learning statement
2. Classify by impact:
   - `rule` — Agent behavior constraint
   - `test` — Should become an automated test
   - `gate` — Release/deployment check
   - `prompt` — Automation prompt update
   - `doc` — Documentation-only
3. Identify the target (where this learning should be applied)
4. Append to `.agent-os/experience-log.jsonl`
5. If classification is `test` or `gate`, create a finding to track implementation

**Template**: See `references/templates.md` → Experience Entry.

**Script**: Planned for v0.2.0.

---

## 8. Agent Onboarding

**When**: A new agent (or new agent instance) joins the workspace.

**Minimum steps**:

1. Read the latest context pack in `.agent-os/context-packs/`
2. Query `.agent-os/findings.jsonl` for open items relevant to its domain
3. Read the latest `.agent-os/mission-control/` for project health
4. After completing work: update findings or append flight records
5. Optionally register in the workspace's agent directory

**Optional declaration** (for multi-agent registries):

```json
{
  "agent": "<name>",
  "domain": "<scope>",
  "inputs": ["context-pack", "mission-control", "findings"],
  "outputs": ["handoff", "finding-update", "flight-record"]
}
```

---

## 9. Leverage Audit

**When**: As part of Codex daily audit or weekly review.

**Steps**:

1. Scan daily logs in `.workbuddy/memory/` for the past 7 days
2. Count output items by leverage annotation:
   - 🔴 strategic (new capabilities, architecture, research breakthroughs)
   - 🟡 tactical (feature iteration, doc updates, issue resolution)
   - 🔵 maintenance (bug fixes, refactoring, cleanup)
3. Compute `strategic_ratio = 🔴 / (🔴 + 🟡 + 🔵)`

**Health thresholds**:
| Ratio | Status | Action |
|-------|--------|--------|
| ≥30% | 🟢 Healthy | No action needed |
| 15-30% | 🟡 Warning | Note in audit: "战略占比偏低，注意平衡维护与创新" |
| <15% | 🔴 Critical | Flag as finding: "过去一周维护类产出占比过高，检查是否陷入整理旧账循环" |

**Audit entry format**:
```
[LEVERAGE] Audit Day -7 to Day 0: strategic_ratio = X% → 🟢/🟡/🔴
  Strategic: N  Tactical: N  Maintenance: N  Total: N
  Action: <none / 标注预警 / 生成 finding>
```

**Auto-trigger**: Include this check automatically in Codex daily audit routines.
