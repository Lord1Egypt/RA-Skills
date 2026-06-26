# Artifact Review

Use the artifact workflow when the agent proposes file changes and the user wants to inspect, approve, or reject them interactively.

## Workflow

Open the Artifact Review Panel with `Ctrl+R`.

1. Navigate files with arrow keys.
2. Preview an individual file inline with `p`; previews are truncated.
3. Press `Enter` on a file for a full-screen diff.
4. Approve with `y` or reject with `n`.
5. Bulk approve with `Shift+A`; bulk reject with `Shift+R`.
6. Press `Esc` to save state and return to the prompt.

## Organization

- Actionable code files require explicit approve/reject.
- Images and videos are grouped in a separate media drawer; expand with `Enter`.
- Plans, code diffs, architecture diagrams, images, and browser recordings can all appear as artifacts depending on task and surface.

## Detail viewer

Open a code or markdown artifact with `Enter` on the row or focused `open` button.

Useful controls:

- `j` / `k` or arrow keys: line scrolling.
- `PgUp` / `PgDown`: page scrolling.
- `g` / `Shift+G`: jump to top/bottom.
- `l`: toggle the line-number gutter.
- `c`: add an inline comment on the focused line.
- `d`: delete the active inline comment on the focused line.
- `m`: cycle Mermaid rendering modes when a diagram is present.
- `Ctrl+=` / `Ctrl+-`: zoom graphical Mermaid output when supported.

Use inline comments to steer the agent before approving plans or code changes.

## Safe defaults

- Review generated code before approval in untrusted repositories.
- Avoid `--dangerously-skip-permissions` when artifact approval matters.
- For headless tasks, ask the agent to print a patch summary or commands run because the review panel is interactive.
- Prefer review-requesting policies for complex or multi-file tasks; use always-proceed only for trusted, low-risk automation.
