---
name: acpx-agent-playbook
description: Practical playbook for running agents through acpx in persistent sessions, especially when Claude, Codex, Pi, Gemini, OpenCode, or other ACP-compatible agents need reliable file creation, local installs, shell-based writes, or structured deliverables such as PPTX, reports, generated assets, and multi-step coding work. Use when work should be done via acpx rather than direct edits, or when prior acpx attempts failed because of quoting, session mode, permission policy, fs/write_text_file issues, sandbox boundaries, agent-specific CLI differences, or confusion about full-access vs true system privilege.
---

# acpx-agent-playbook

Use acpx as a structured control plane for delivery-oriented agent work. Prefer persistent sessions, prompt files, explicit validation, and shell/Python fallback writes over fragile one-shot prompts and optimistic tool assumptions.

## Quick start

Run this default flow for any non-trivial task:

```bash
acpx <agent> sessions new --name task
acpx <agent> set-mode -s task full-access
acpx <agent> -s task -f prompt.txt
```

Replace `<agent>` with `codex`, `claude`, `pi`, `gemini`, `opencode`, or another supported agent.

Prefer this over `acpx <agent> exec ...` when the task needs iteration, file output, validation, or retries.

## Workflow

### 1. Choose agent deliberately

Pick the agent based on workflow risk, not branding preference alone.

Default heuristics in this workspace:
- **Codex**: safest default for deadline-sensitive artifact delivery and multi-step coding work
- **Claude**: acceptable when freshly re-verified for text + file writes + target artifact flow
- **Other agents**: treat as unverified until they pass the same smoke tests

If reliability matters more than style, prefer the agent with the freshest passing artifact-generation proof in the current environment.

### 2. Choose session type

Use `exec` only for small one-shot tasks.

Use a persistent session when the task involves any of the following:
- generating files
- multiple retries
- long prompts
- validation steps
- local installs or virtual environments
- deliverables such as `.pptx`, `.docx`, reports, videos, or scripts

### 3. Set mode explicitly

For practical work, set mode before prompting:

```bash
acpx <agent> set-mode -s task full-access
```

Interpretation:
- `read-only`: inspect only
- `auto`: moderate default behavior
- `full-access`: broader session capability, including easier file edits and broader path/network freedom

Do **not** assume `full-access` means sudo or root. It relaxes the ACP session; it does not guarantee system-level privilege escalation.

### 4. Use prompt files, not huge shell strings

For long or delicate instructions, always write a prompt file and pass `-f`:

```bash
cat > prompt.txt <<'TXT'
Task: ...
Constraints: ...
Outputs: ...
Validation: ...
TXT

acpx <agent> -s task -f prompt.txt
```

This avoids shell quoting failures and makes retries reproducible.

### 5. Check permission policy before blaming the agent

If the agent can answer text but cannot write files, inspect acpx permission configuration first.

In this workspace, a blocking configuration was:

```json
{
  "defaultPermissions": "approve-reads",
  "nonInteractivePermissions": "fail"
}
```

A working baseline for non-interactive delivery flows was:

```json
{
  "defaultPermissions": "approve-all",
  "nonInteractivePermissions": "deny"
}
```

Do not assume the failure is prompt quality or provider incompatibility until this is checked.

### 6. Respect agent-specific CLI differences

Do not assume all agents accept the same flags on the same subcommand.

Example from this environment:
- top-level `acpx` supports `--cwd`
- `acpx claude` may reject `--cwd` on the agent subcommand

If a command fails before the model meaningfully starts, verify CLI shape before diagnosing provider or model problems.

### 7. Prefer shell/Python file writes over ACP fs writes when needed

If the task must create or rewrite files, instruct the agent to prefer:
- shell heredocs
- `python - <<'PY' ... PY`
- direct command-line generation

Prefer these over tool-native `fs/write_text_file` style edits when prior attempts showed permission failures.

Recommended instruction snippet:

```text
If built-in file-editing tools fail, write files via shell heredoc or Python scripts instead of ACP fs write calls.
```

### 8. Use writable output paths first

For fragile generation tasks, write outputs under `/tmp` first, validate them, then move/copy them into the target workspace.

Recommended pattern:
- generate under `/tmp/...`
- validate structure and existence
- copy to final destination only after success

This is especially useful for generated binaries like `.pptx`.

### 9. Validate before declaring success

Always ask the agent to verify outputs.

Examples:
- file exists
- zip/XML structure parses for `.pptx`
- image dimensions or PDF page count
- report file with output path, validation result, and model if visible

## Practical patterns

### Pattern: generated deliverables

For PPT/report/document generation, require all of the following in the prompt:
- exact output path
- exact report path if needed
- validation steps
- final short summary with model/path if possible

See `references/ppt-playbook.md` for a concrete template.

### Pattern: local dependency installs

If non-stdlib packages are needed, prefer project-local installs:

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install <package>
```

Avoid assuming global install rights. Use system-level installs only when explicitly intended and actually permitted by the host.

### Pattern: re-verification ladder for a new agent/provider

Before trusting a new agent or relay for delivery work, run this sequence:
1. fixed-text response
2. minimal file-write task
3. one real artifact task

If any stage fails, do not market the path as production-ready.

## Decision rules

- If the task is small and read-heavy: `exec` is acceptable.
- If the task must create deliverables: use a persistent session.
- If the prompt is long: use `-f prompt.txt`.
- If file editing fails once: inspect permissions, then switch to shell/Python write strategy.
- If dependencies are missing: try local `.venv` install before changing system state.
- If a binary artifact is required: generate in `/tmp`, validate, then move.
- If one agent is flaky and the user still needs a real artifact fast, route the deliverable to the currently verified agent instead of burning retries.

## Anti-patterns

Avoid these common failure modes:
- stuffing long multilingual prompts directly into one shell string
- assuming `full-access` equals sudo/root
- relying only on ACP fs writes for large generated files
- declaring success before validating output structure
- writing the final artifact directly into a path that may be sandbox-restricted
- assuming one agent's CLI flags or permission behavior apply to all other agents

## References

- Read `references/ppt-playbook.md` when the task is to generate a PPT or similar structured binary deliverable via acpx.
- Read `references/troubleshooting.md` when acpx sessions start but file creation, mode behavior, permissions, or sandbox boundaries are unclear.
- Read `references/provider-compat.md` when comparing agents for provider compatibility, relay flakiness, file-write reliability, or ACPX permission confusion.
- Read `references/agent-matrix.md` when you need a quick choice among Codex, Claude, and other agents for delivery work in this workspace.
- Read `references/migration.md` when older prompts, habits, or automations still mention `acpx-codex-playbook` and you need to preserve compatibility while using the new canonical skill.
