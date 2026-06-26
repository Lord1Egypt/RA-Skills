# migration notes

## From `acpx-codex-playbook` to `acpx-agent-playbook`

Use `acpx-agent-playbook` as the canonical skill for all new work.

Keep these migration rules:

- if an old prompt asks for `acpx-codex-playbook`, treat it as an alias
- preserve Codex as the default safest delivery path unless another agent has fresher passing artifact proof in the current workspace
- do not copy new operational guidance back into the deprecated skill unless required for compatibility

## What changed

Old model:
- skill centered on Codex-specific delivery tactics

New model:
- skill centered on acpx as the control plane
- agent choice becomes an explicit decision
- verification ladder applies to any agent
- permission policy and CLI-shape checks are first-class troubleshooting steps

## Canonical re-verification ladder

Before trusting an agent for real deliverables:
1. fixed-text response
2. minimal file write
3. one real artifact task

Only after passing all three should the agent be treated as delivery-capable in the current environment.
