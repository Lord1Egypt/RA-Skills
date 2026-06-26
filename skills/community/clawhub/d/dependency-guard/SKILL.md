---
name: "dependency-guard"
version: "1.0.1"
description: "Use when a task adds, upgrades, removes, or reviews software dependencies and the agent should apply a Socket-based supply-chain guardrail before changing manifests or lockfiles. Prefer MCP `depscore` when available, otherwise use the bundled Socket CLI helper. Stop and recommend an alternative or human review when risk signals are weak."
metadata: {"openclaw":{"emoji":"🛡️","requires":{"bins":["socket"]}}}
---

# Dependency Guard

Use this skill when dependency changes are in scope for `npm`, `pnpm`, `yarn`, Python packages, or other package ecosystems supported by Socket.

## Prerequisites

- The `socket` CLI must be installed and on `PATH` (`npm install -g socket`).
- Authentication is required for CLI-based reviews. See the Authentication section below.

## Workflow

1. Confirm the exact dependency change being proposed.
2. Check whether the feature can be implemented with the standard library or an existing project dependency.
3. Prefer MCP `depscore` if the host agent exposes it.
4. Otherwise run `scripts/check_dependency.sh <ecosystem> <package> [version]`.
5. Apply the policy in `references/policy.md`.
6. Apply the decision rules in `references/decision-matrix.md`.
7. Before making the change, report:
   - why the package is needed
   - whether an existing alternative exists
   - what Socket reported
   - whether install scripts, risky capabilities, or transitive risk are present
8. If the decision is `allow_with_warning`, present the warning clearly before making the change. If the decision is `block_pending_human_review` or `block`, stop and propose either:
   - a safer dependency
   - a no-dependency implementation
   - explicit human review

## Authentication

Three authentication paths are supported, in order of preference:

1. **MCP `depscore`** — no local credentials needed; works through the host agent's MCP connection.
2. **`socket login`** — interactive CLI login; stores auth locally.
   - If your CLI supports it, pressing Enter at the token prompt uses limited public access.
   - To use a private token, paste it at the prompt instead.
3. **`SOCKET_SECURITY_API_TOKEN` env var** — set this for CI or headless environments.

> **Security:** Never paste private tokens into agent prompts. Use the env var or `socket login` instead.

> **CI note:** GitHub Actions workflows use `SOCKET_SECURITY_API_KEY` (a separate GitHub-integration key), not `SOCKET_SECURITY_API_TOKEN`. See `examples/github/dependency-guard.yml`.

## Reporting Contract

Use the short response template in `references/examples.md` when presenting the package review to the user.

## References

- Read `references/policy.md` for the canonical guardrail.
- Read `references/decision-matrix.md` for allow/block criteria.
- Read `references/examples.md` for user-facing review examples.

## Notes

- Keep `SKILL.md` lean; do not duplicate the full policy here.
- OpenClaw and ClawHub expect `metadata` to be a single-line JSON object in frontmatter, so keep the OpenClaw metadata compact.
- The `version` field in frontmatter is the single source of truth; use `publish_clawhub.sh --bump patch|minor|major` to auto-increment.
- Do not assume system-wide wrapper enforcement or shell-completion setup is desirable; keep CLI setup minimal.
- If Socket tooling is unavailable, require human review before adding the dependency.
- Review manifest and lockfile changes together.
