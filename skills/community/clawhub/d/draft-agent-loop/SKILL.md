---
name: draft-agent-loop
version: "1.6.0"
description: >
  Enforce a Human-in-the-Right-Loop (HITRL) lifecycle for remote agents.
  Use this skill when the user wants structured oversight over an agent task: plan approval before execution, evidence-logged execution, and result sign-off before closure.
  Trigger phrases: "work on this with my oversight", "check with me before you start", "use HITRL for this", "I want to review your plan first", "use draft-agent-loop".
  DO NOT use for tasks where the user simply asks to do something without requesting approval gates. Use draft-cli for raw Draft commands.
  This skill depends on the canonical draft-cli skill. It assumes headless page workflows under `draft ... --runtime v2`, which fit remote OpenClaw-style isolated environments.
metadata:
  clawdis:
    emoji: "🔄"
    dependencies:
      - name: "toliuweijing/draft-cli"
        type: "other"
        url: "https://clawhub.ai/toliuweijing/draft-cli"
    requires:
      bins:
        - "draft"
    install:
      - id: "npm"
        kind: "node"
        package: "@innosage/draft-cli"
        bins:
          - "draft"
        label: "Install draft-cli (npm)"
    envVars:
      - name: "GLOBAL_INVITE_CODE"
        required: false
        description: "The invite code used to publish Draft pages safely. Defaults to `innosage` during the free beta publish flow."
---

# Draft Agent Loop Skill (HITRL)

Use this skill to implement a rigorous human-agent collaboration loop. This is the "Human-in-the-Right-Loop" (HITRL) method, designed to eliminate "blind box" agent outcomes by forcing plan approval and result verification.

> **Scope**: This skill orchestrates remote agent workflows using the `draft` CLI. All persistence is through Draft pages (via the canonical `draft-cli` dependency). It does not write to local disk or agent memory.

## Trigger Guidance

Trigger this skill when:

- "Work on this task and check with me before and after."
- "I want to review your plan first before you do anything."
- "Use HITRL / use draft-agent-loop for this."
- "Apply structured oversight to this task."
- New task received where the user's intent is high-stakes or complex enough to warrant human gates.
- A new iteration is requested after a Phase 3 sign-off.

Do NOT trigger this skill when:

- The user asks to do a task directly with no mention of approval or review gates.
- The user only asks about raw Draft commands or page automation without approval gates (use `draft-cli`).
- The user wants a local-file authoring workflow (authorship in local markdown).

## Core Rules

- **Source of Truth**: The "Task Journal" Draft page. All plans, logs, and results live there.
- **Environment**: Always use headless page mode through `draft ... --runtime v2`.
- **Runtime dependency**: Follow the startup and page-operation rules from `draft-cli`.
- **Handoff Mode**: **Blocking**. STOP and wait for human approval/sign-off in the chat before proceeding to the next phase.
- **No Sensitive Data in Logs**: Do NOT include credentials, secrets, tokens, or PII in execution log entries or plan documents. Limit evidence to status indicators and non-sensitive file names.

## Phase 0: Setup & Connection

Before doing anything, establish a stable Draft connection:

```bash
# 1. Start the daemon in headless runtime v2
draft start-server

# 2. Confirm the session is READY before proceeding
draft status --json
```

If `draft status` does not show a healthy `v2` headless session, follow the `draft-cli` recovery pattern:
- `DAEMON_OFFLINE` → re-run `draft start-server`
- wrong runtime selected → stop and correct runtime before writing
- Only proceed once `draft status --json` shows a healthy headless `v2` session

## Phase 1: Plan (Proposal & Approval)

Before executing any code or changes:

1.  **Create Journal**: Create a new Draft page titled `<Task Name> - Task Journal`.
    ```bash
    draft page create "<Task Name> - Task Journal" --json
    ```
2.  **Submit Plan**: Author a detailed Task Journal using the mandatory template. Append it to the Journal.
    ```bash
    cat << 'EOF' | draft page append <id> --json
    # 📋 Task: [Title]

    ## Context
    [Detailed background and motivation]

    ## Problem / Goal
    [Specific issue being solved or feature being added]

    ## Acceptance Criteria (Outcome-Focused)
    - [ ] [Criterion 1]
    - [ ] [Criterion 2]

    ## Implementation Notes
    [Current state analysis, relevant files, suggested approach, technical considerations]

    ## Test Coverage
    [Test strategy, scenarios to test, existing tests to reference]
    EOF
    ```
3.  **Confirm Before Publishing**: Before publishing, explicitly confirm with the user: "I am about to publish the Task Journal for external review. Please confirm."
4.  **Handoff**: On confirmation, publish the page and ask for approval.
    ```bash
    draft page publish <id> --invite-code "${GLOBAL_INVITE_CODE:-innosage}" --json
    ```
    **Handoff Phrase**: "I have initialized the Task Journal with the plan and requirements: [URL]. Please review the context and acceptance criteria. Once you are ready for me to proceed, please reply with **APPROVED** or **LGTM** here in the chat."

5.  **Wait**: STOP. Do not proceed until the user explicitly tells you to continue in the chat. Note: Do not rely on Draft page comments for approval on remote/public pages.

## Phase 2: Execute (Action & Logging)

Once approved:

1.  **Verify Approval**: Confirm the user has provided approval in the chat.
2.  **Execute**: Perform the tasks outlined in the plan.
3.  **Log Evidence**: For every significant action, append a concise, non-sensitive log entry to the Journal under a `# 📜 Execution Log` section. Do NOT include raw command output, file contents, or credentials.
    ```bash
    cat << 'EOF' | draft page append <id> --json
    ### [Timestamp] Action: [Description]
    - **Status**: Success/Failure
    - **Evidence**: [e.g., "Modified src/components/Button.tsx — added reveal prop"]
    EOF
    ```

## Phase 3: Verify (Result & Sign-off)

Once the execution is complete:

1.  **Submit Results**: Append a `# ✅ Final Results` summary to the Journal. Include links to artifacts (e.g., PR URL, Draft page URL). Do not include raw file dumps.
2.  **Confirm Before Publishing**: Explicitly confirm with the user before re-publishing.
3.  **Handoff**: On confirmation, re-publish the page.
    ```bash
    draft page publish <id> --invite-code "${GLOBAL_INVITE_CODE:-innosage}" --json
    ```
    **Handoff Phrase**: "I have completed the task. Please verify the results in the Task Journal: [URL]. If satisfied, reply with **DONE** or **✅** here in the chat."

4.  **Wait**: STOP. If the user provides sign-off (**DONE** / **✅**), proceed to Phase 4. If feedback is received, enter the Iteration Loop.

## Phase 4: Archive (Draft Page Only)

After sign-off, append a final summary to the existing Task Journal page. This keeps all persistence within Draft — no local filesystem writes.

```bash
cat << 'EOF' | draft page append <id> --json
# 🗂 Task Complete — Summary
- **Outcome**: [Brief description of what was achieved]
- **Key Decisions**: [Any notable trade-offs or design choices]
- **Artifacts**: [Links to PR, relevant files, or external references]
EOF
```

> The Draft page itself (with its page ID and URL) is the durable record. No additional writes to `TASK_LOG.md`, `knowledge/`, or other filesystem locations are required or expected.

## Iteration Loop

If the user provides feedback or requests changes after Phase 3:
1.  **Acknowledge**: Acknowledge the feedback in the chat.
2.  **Start New Iteration**: Enter Phase 1 again to propose how you will address the feedback.
3.  **Append to Same Page**: Do NOT create a new page. Append the new plan to the existing Task Journal under a new heading: `# 📋 Iteration [N]: Addressing Feedback`.
4.  **Template**: Use the mandatory Phase 1 template for each new iteration to maintain context and traceability.

## Non-Goals

- Do NOT use browser-backed v1 or `--mode workspace`.
- Do NOT skip the plan approval gate.
- Do NOT execute multiple un-logged steps.
- Do NOT write to local agent filesystem (no `TASK_LOG.md`, no `knowledge/` writes).
- Do NOT include credentials, PII, or sensitive command outputs in Draft page content.
