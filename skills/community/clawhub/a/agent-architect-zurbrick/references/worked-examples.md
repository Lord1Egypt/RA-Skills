# Worked Examples

Use these examples to reduce misclassification in mixed failures.

## 1. Rules vs Memory

**Symptom:**
The agent knows it should verify before external delivery, but it keeps missing one specific recipient exception or standing instruction.

**Diagnosis:**
Primary lane = **memory**
Secondary lane = **rules**

**Fix type:**
**Memory tweak**

**Why:**
The rule already exists. The repeated failure is retention of an exception or standing fact, not missing policy.

**Patch target:**
- `MEMORY.md` or a focused memory/bank note
- only touch rules if the rule itself is unclear

---

## 2. Memory vs Skills

**Symptom:**
The agent keeps handling the same recurring workflow ad hoc and forgets important steps each time.

**Diagnosis:**
Primary lane = **skills**
Secondary lane = **memory**

**Fix type:**
**Skill change**

**Why:**
This is not mainly about storing one more fact. The agent lacks a reusable workflow for a repeatable job.

**Patch target:**
- existing skill `SKILL.md`
- skill `references/`
- or one new narrow skill only if reuse is real

---

## 3. Persona vs Rules

**Symptom:**
The agent sounds too soft and hesitant in situations where it should make a call.

**Diagnosis:**
Primary lane = **rules**
Secondary lane = **persona**

**Fix type:**
**Rule change** or **plain edit**

**Why:**
If the hesitancy comes from unclear authority or escalation logic, tone edits alone will not fix it.

**Patch target:**
- `AGENTS.md` / `OPERATIONS.md`
- only patch persona if the style remains off after the rule is clear

---

## 4. Skills vs Rules

**Symptom:**
Someone proposes a new skill after one bad run where the agent skipped a basic check.

**Diagnosis:**
Primary lane = **rules**

**Fix type:**
**No change** or **plain edit**

**Why:**
A missing verification habit is not automatically a skill gap.

**Patch target:**
- existing operational rule
- do not create a new skill from one anecdote

---

## 5. State / retry ambiguity

**Symptom:**
The agent takes an action, gets partial output, then retries blindly without first checking whether the system state already changed.

**Diagnosis:**
Primary lane = **rules**
Secondary lane = **skills**

**Fix type:**
**Rule change** or **plain edit**

**Why:**
The agent's main failure is lack of post-action state verification and recovery discipline, not missing memory. Only promote to a skill change if the same recovery workflow repeats often enough to deserve reusable guidance.

**Patch target:**
- `AGENTS.md` / `OPERATIONS.md`
- optionally a skill workflow only if the recovery loop is genuinely recurring

---

## 6. Do-nothing case

**Symptom:**
The agent had one sloppy answer during a long, noisy session, but the behavior has not repeated.

**Diagnosis:**
Primary lane = **none yet**

**Fix type:**
**No change**

**Why:**
One bad run is weak evidence. Log it, watch for recurrence, and avoid architecture inflation.

**Patch target:**
- none
- optionally note the incident for later review
