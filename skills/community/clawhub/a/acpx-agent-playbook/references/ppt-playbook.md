# PPT playbook for acpx agents

Use this pattern when the user wants an acpx-driven agent to generate a `.pptx` or similar structured artifact.

## Recommended flow

```bash
acpx <agent> sessions new --name ppt
acpx <agent> set-mode -s ppt full-access
acpx <agent> -s ppt -f prompt.txt
```

Replace `<agent>` with the currently verified delivery agent in this workspace.

## Prompt template

```text
Task: Create a real PPTX deliverable.

Environment constraints:
- Use a persistent session
- If python-pptx is unavailable, either install it locally in a project/local venv or fall back to a stdlib-only approach
- Do not assume global install rights
- If ACP file-edit tools fail, write files through shell heredoc or Python scripts

Output rules:
- Write intermediate files under /tmp
- Final PPTX path: /tmp/output.pptx
- Report path: /tmp/output-report.txt

Validation:
- Verify the file exists
- Verify PPTX zip structure parses
- Confirm slide count
- Record model name if visible

Final output:
- Print exact output path
- Print model used if visible
```

## Why this works

- prompt file avoids quoting bugs
- persistent session preserves context across retries
- `full-access` reduces session friction
- `/tmp` avoids many workspace path edge cases
- shell/Python writes are often more reliable than ACP file-write handlers for large generated files
- the same prompt structure can be reused across Codex, Claude, and other acpx agents after minimal smoke-test verification

## When dependencies are missing

Prefer local installs:

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install python-pptx
```

If network or package install is unavailable, instruct Codex to fall back to a stdlib-only generator.

## Validation checklist

- `.pptx` exists
- zip opens
- `[Content_Types].xml` exists
- `ppt/presentation.xml` exists
- expected slide count matches request
- report file exists
