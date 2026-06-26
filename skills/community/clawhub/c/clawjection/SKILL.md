---
name: clawjection
description: Install and apply ClawJection bundles when a user asks to install a ClawJection, run a ClawJection, or configure an OpenClaw instance from a ClawJection repo, archive, or local bundle.
---

# ClawJection

Use this skill when the user asks you to install or run a ClawJection.

## What ClawJection Is

ClawJection is a bundle format for modifying a local OpenClaw instance so it adopts a specific role or capability set.

A ClawJection bundle has:
- a required `clawjection.yaml`
- an entrypoint declared by that manifest
- arbitrary bundle internals chosen by the bundle author

The entrypoint is expected to:
- modify the OpenClaw workspace or local runtime
- install tools, skills, or auth setup when needed
- return a structured result JSON with ordered `followups`

## Install Flow

1. Get the bundle locally.
2. Find the bundle root by locating `clawjection.yaml`.
3. Read `clawjection.yaml` and resolve `entrypoint.path`.
4. Run the entrypoint from the bundle root with the `apply` action.
5. By default, let the entrypoint discover OpenClaw config from `~/.openclaw/openclaw.json`.
6. If needed, pass `--openclaw-config-path <path>`.
7. Treat stdout as agent-readable hints.
8. Read the structured result JSON from `CLAWJECTION_RESULT_PATH`.
9. Execute the returned ordered `followups`.

## Source Types

### Git repository

- Clone the repo to a temporary local directory.
- If the repo contains multiple bundles, choose the directory containing the intended `clawjection.yaml`.

### Archive URL or local zip

- Download or unpack it to a temporary local directory.
- Identify the bundle root by locating `clawjection.yaml`.

### Local directory

- Use it directly if it contains `clawjection.yaml`.

## Execution Rules

- Run from the bundle root so relative paths in the bundle resolve correctly.
- Do not assume the bundle layout beyond `clawjection.yaml` and the declared entrypoint.
- If the bundle installs CLIs or skills, verify they were actually installed before claiming success.
- If the result says `needs_user_action`, do not treat the setup as finished; perform the `followups`.

## Safety

- Review what the entrypoint appears to do before running untrusted bundles.
- Tell the user when a bundle will overwrite core OpenClaw files such as `IDENTITY.md`.
- Never claim a remote skill or CLI is installed unless the install command succeeded.
- Keep secrets out of workspace files unless the bundle explicitly requires that behavior and the user agrees.

## References

- Read `standard/v1.md` in this repo for the full execution contract.
- Read `schemas/clawjection.schema.json` and `schemas/result.schema.json` when you need the exact manifest or result structure.
