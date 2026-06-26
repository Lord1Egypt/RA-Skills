---
name: acpx-codex-playbook
description: Practical playbook for running Codex through acpx in persistent sessions, especially when the task needs reliable file creation, local dependency installs, shell-based writes, or structured delivery such as PPTX, reports, generated assets, and multi-step coding work. Use when the user wants work done via acpx/Codex instead of direct edits, or when prior acpx attempts failed because of quoting, session mode, fs/write_text_file permission issues, sandbox boundaries, or confusion about full-access vs true system privilege.
---

# acpx-codex-playbook

Use acpx as a structured control plane for Codex. Prefer persistent sessions, prompt files, and shell-based file generation over fragile one-shot prompts and tool-native file writes.

## Quick start

Run this default flow for any non-trivial task:

```bash
acpx codex sessions new --name task
acpx codex set-mode -s task full-access
acpx codex -s task -f prompt.txt
```

Prefer this over `acpx codex exec ...` when the task needs iteration, file output, validation, or retries.

## Workflow

### 1. Choose session type

Use `exec` only for small one-shot tasks.

Use a persistent session when the task involves any of the following:
- generating files
- multiple retries
- long prompts
- validation steps
- local installs or virtual environments
- deliverables such as `.pptx`, `.docx`, reports, videos, or scripts

### 2. Set mode explicitly

For practical work, set mode before prompting:

```bash
acpx codex set-mode -s task full-access
```

Interpretation:
- `read-only`: inspect only
- `auto`: moderate default behavior
- `full-access`: broader session capability, including easier file edits and broader path/network freedom

Do **not** assume `full-access` means sudo or root. It relaxes the ACP session; it does not guarantee system-level privilege escalation.

### 3. Use prompt files, not huge shell strings

For long or delicate instructions, always write a prompt file and pass `-f`:

```bash
cat > prompt.txt <<'TXT'
Task: ...
Constraints: ...
Outputs: ...
Validation: ...
TXT

acpx codex -s task -f prompt.txt
```

This avoids shell quoting failures and makes retries reproducible.

### 4. Prefer shell/Python file writes over ACP fs writes

If the task must create or rewrite files, instruct Codex to prefer:
- shell heredocs
- `python - <<'PY' ... PY`
- direct command-line generation

Prefer these over tool-native `fs/write_text_file` style edits when prior attempts showed permission failures.

Recommended instruction snippet:

```text
If built-in file-editing tools fail, write files via shell heredoc or Python scripts instead of ACP fs write calls.
```

### 5. Use writable output paths first

For fragile generation tasks, write outputs under `/tmp` first, validate them, then move/copy them into the target workspace.

Recommended pattern:
- generate under `/tmp/...`
- validate structure and existence
- copy to final destination only after success

This is especially useful for generated binaries like `.pptx`.

### 6. Validate before declaring success

Always ask Codex to verify outputs.

Examples:
- file exists
- zip/XML structure parses for `.pptx`
- image dimensions or PDF page count
- report file with output path, validation result, and model if visible

## Practical patterns

### Pattern: generated deliverables

For PPT/report/document generation, require all of the following in the prompt:
- exact output path
- exact report path
- validation steps
- final two-line summary with model/path if possible

See `references/ppt-playbook.md` for a concrete template.

### Pattern: local dependency installs

If non-stdlib packages are needed, prefer project-local installs:

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install <package>
```

Avoid assuming global install rights. Use system-level installs only when explicitly intended and actually permitted by the host.

### Pattern: troubleshooting failed writes

If `touch` or shell writes work but ACP file edits fail, treat it as an ACP handler or sandbox-path issue, not proof that Codex itself lacks capability. Switch the generation strategy to shell/Python writes.

## Decision rules

- If the task is small and read-heavy: `exec` is acceptable.
- If the task must create deliverables: use a persistent session.
- If the prompt is long: use `-f prompt.txt`.
- If file editing fails once: switch to shell/Python write strategy.
- If dependencies are missing: try local `.venv` install before changing system state.
- If a binary artifact is required: generate in `/tmp`, validate, then move.

## Anti-patterns

Avoid these common failure modes:
- stuffing long multilingual prompts directly into one shell string
- assuming `full-access` equals sudo/root
- relying only on ACP fs writes for large generated files
- declaring success before validating output structure
- writing the final artifact directly into a path that may be sandbox-restricted

## References

- Read `references/ppt-playbook.md` when the task is to generate a PPT or similar structured binary deliverable via acpx/Codex.
- Read `references/troubleshooting.md` when acpx sessions start but file creation, mode behavior, or sandbox boundaries are unclear.
