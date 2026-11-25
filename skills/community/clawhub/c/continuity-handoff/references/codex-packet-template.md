---
type: Continuity Handoff
title: "<human task title>: compact continuation"
description: Continue accepted work without inheriting the legacy transcript.
tags: [continuity, handoff]
status: active
generated:
  by: "<agent or operator>"
  at: "<ISO-8601 timestamp>"
sources:
  - id: source-task
    resource: "urn:codex:thread:<thread-id>"
    title: "<human source title>"
  - id: decision-anchor
    resource: "<commit, issue, URL, or document title>"
    title: "<human anchor title>"
continuity:
  schema_version: "0.3"
  source_mode: legacy-task
  destination_mode: fresh-native-task
  transcript_inherited: false
  acknowledgement_required: true
  historical_recall: bounded-read-only-question-driven
---

# Mission

<One paragraph describing the current outcome, not the whole project history.>

# Work

- Work: <portable human-readable work identity>.
- Work slug: `<stable-lowercase-slug>`.

# Current Goal And Resume Checkpoint

- Active goal: <goal or explicitly none>.
- Completed checkpoint: <last proven checkpoint>.
- Resume point: <one exact next action>.
- Authorization boundary: <what this packet does and does not authorize>.
- Inherited goal lineage: <source goal ID/state/usage, or explicitly none>.

# Source Thread And Portable Identity

- Thread ID: `<source-thread-id>`.
- Human title: <source title>.
- Profile: <source profile name>.
- Profile Placement: <primary, secondary, or another explicit placement>.
- Device: <stable device name>.
- Project Binding: <portable project identity>.
- Repository: <portable owner/name>.
- Branch: `<branch>`.
- HEAD: `<commit>`.
- This is semantic continuation, not transcript migration.

# Device Observations

These paths are local observations for the recorded Device. They are not
canonical Work identity and must not be guessed on another Device.

- Binding Model: `<single-root or project-root-with-nested-repo>`.
- Codex Project Root: `<outer directory saved by the Codex project>`.
- Canonical Repo Root: `<directory containing .git and AGENTS.md>`.
- Operational CWD: `<working directory inside the canonical repo>`.
- CODEX_HOME: `<exact source profile CODEX_HOME>`.
- rollout_path: `<exact resolved source rollout path>`.

# Accepted Decisions

- <Decision and rationale.>

# Failures And Do Not Repeat

- <Rejected action, measured consequence, and required invariant.>

# Ledger Snapshot And Canonical References

- <Reference authoritative files, commits, issues, tests, and ledgers.>
- <Include only the current checkpoint and strongest proof.>
- Live repository and runtime truth override stale references.

# Protected State

- <Exact source task and unrelated user-owned state that must remain untouched.>

# Historical Recall Handle

```yaml
work: "<portable work identity>"
title: "<human source title>"
thread_id: "<source task id>"
profile: "<profile>"
profile_placement: "<primary or secondary>"
device: "<device>"
project_binding: "<portable project identity>"
device_observation:
  binding_model: "<single-root or project-root-with-nested-repo>"
  codex_project_root: "<saved Codex project root>"
  canonical_repo_root: "<Git root containing .git>"
  operational_cwd: "<working directory inside canonical repo>"
  codex_home: "<source CODEX_HOME>"
  rollout_path: "<verified rollout path>"
access_policy: "bounded-read-only-question-driven"
```

# Inherited Usage And Evidence Lineage

- Source usage observation: <exact source usage evidence or unavailable>.
- Target native counters: separate; record only after Target creation.
- Evidence Lineage: <source goal, proof, timestamps, and retrieval locators>.
- Do not add Source usage to Target native counters.

# Known Historical Gaps

- <Facts deliberately omitted or not verified.>
- Absence from this packet means unknown, not false.

# Independent Review Before Implementation

Read repo instructions and verify branch, HEAD, dirty state, cited canon, and
the smallest relevant implementation surface. Stop on contradiction.

# Validation

- Target Thread ID: `<assigned only after fresh native creation>`.
- Target ID differs from Source ID: <pending/pass>.
- Required acknowledgement: <pending/pass>.
- Exact-source bounded Recall: <pending/pass and evidence locator>.
- Project Binding validation: <pending/pass; include model and all three roots>.
- Source unchanged proof: <pending/pass and before/after evidence>.
- The handoff is not accepted while any item is pending.

# Suggested Skills

- <Only capabilities relevant to the next bounded action.>

# Required Acknowledgement

Reply first with:

1. mission and resume checkpoint;
2. accepted versus unverified facts;
3. exact next read-only action;
4. protected state;
5. confirmation that implementation has not started.
