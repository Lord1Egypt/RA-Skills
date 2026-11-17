---
name: api-to-typemcp
description: Use when turning supplied API sources into a safe TypeMCP project.
version: 0.2.6
category: integration
license: MIT
metadata:
  hermes:
    tags: [mcp, api, openapi, swagger, code-generation, type-mcp]
    related_skills: []
  openclaw:
    requires:
      bins: [python3, node, npm]
    envVars:
      - name: TYPE_MCP_APPROVAL_STATE_DIR
        required: false
        description: Isolated directory for single-use generation approvals.
      - name: TYPE_MCP_BASE_URL
        required: false
        description: Local test upstream used only by contained verification.
---

# API to TypeMCP

## Overview

This released skill is a complete, bundled generator delivery unit. Its **bundled skill engine** is in `scripts/`, its controlled TypeScript output templates are in `templates/`, and its public TypeMCP runtime constraints are in [references/type-mcp-runtime.md](references/type-mcp-runtime.md).

Generated projects use the current published `@theorvane/type-mcp@0.3.2` release line and only its public package exports; they never copy TypeMCP source or use local, `file:`, `git:`, `link:`, or private runtime APIs. The npm registry `gitHead` and GitHub Release `v0.3.2` both resolve to `e75bcf6a81ef4df57301b6154a0088845020886f`.

## When to use

Use this skill with a **supplied local** OpenAPI 3.x / Swagger 2.0 JSON/YAML file, supplied Swagger UI HTML, or supplied Markdown/HTML API reference. Do not use it to crawl a bare origin, infer undocumented operations, make mutating calls by default, or publish without explicit final confirmation.

## Execution permissions and containment boundary

The engine reads only the user-supplied source and files bundled with this skill. It writes only the caller-created output directory and the optional `TYPE_MCP_APPROVAL_STATE_DIR`; it never modifies an upstream API or publishes a repository without the separate explicit gates below.

The engine invokes `python3`. Optional generated-project verification additionally invokes `npm` and `node`, uses a fresh temporary workspace, passes a credential-scrubbed environment, disables inherited npm proxy settings and lifecycle scripts, and installs exactly the generated `package-lock.json` graph with `npm ci`. That install requires outbound access to the npm registry; the generator itself performs no network fetch or crawling, and the smoke test targets only a caller-provided local test upstream.

This verifier is **process containment**, not a claim of kernel or network isolation. Run it in a container, VM, or an equivalent host sandbox when the generated project or its dependency installation is untrusted.

## Bundled engine workflow

Run the engine through its installed skill-relative path. Set `SKILL_DIR` to the directory containing this `SKILL.md`; create a **controlled temporary output directory** yourself and keep it empty.

```bash
SKILL_DIR="/absolute/path/to/api-to-typemcp"
SOURCE="/absolute/path/to/supplied-openapi.json"
OUTPUT="$(mktemp -d -t api-to-typemcp-output.XXXXXX)"
STATE="$(mktemp -d -t api-to-typemcp-state.XXXXXX)"
export TYPE_MCP_APPROVAL_STATE_DIR="$STATE"

# 1. Inspect and build the exact secret-free manifest.
python3 "$SKILL_DIR/scripts/api_to_typemcp.py" inspect --file "$SOURCE" --json
python3 "$SKILL_DIR/scripts/api_to_typemcp.py" manifest --file "$SOURCE" --json > manifest.json
DIGEST="$(python3 -c 'import json; print(json.load(open("manifest.json"))["digest"])')"

# 2. Review the manifest, then explicitly approve precisely that digest.
python3 "$SKILL_DIR/scripts/api_to_typemcp.py" approve \
  --file "$SOURCE" --manifest-digest "$DIGEST"

# 3. Render only after approval, with an exact digest confirmation.
python3 "$SKILL_DIR/scripts/api_to_typemcp.py" generate \
  --file "$SOURCE" --output "$OUTPUT" \
  --confirm-manifest-digest "$DIGEST"
```

For supplied Markdown or HTML, add an explicit origin; no page is fetched or crawled:

```bash
python3 "$SKILL_DIR/scripts/api_to_typemcp.py" manifest \
  --file "/absolute/path/to/reference.md" \
  --base-url "https://api.example.test" --json
```

Swagger UI discovery is performed by `inspect` in-memory and returns only an explicit configured spec reference. The user must separately supply that structured spec; do not fetch it automatically.

## Mandatory safety gates

1. **Manifest first.** Treat every source as untrusted. Review canonical secret-free manifest data before generation.
2. **Receipt gate.** `approve` issues a HMAC-protected, digest-bound, single-use receipt. A changed, expired, tampered, or already-consumed receipt stops `generate`.
3. **Output gate.** The output directory must already exist and be empty unless `--replace` is explicitly supplied. Symlinks and `..` traversal are rejected.
4. **Runtime policy.** `GET`/`HEAD`/`OPTIONS` are read operations. `POST`/`PUT`/`PATCH`/`DELETE` are protected writes and require exact known IDs in `TYPE_MCP_ALLOW_PROTECTED_OPERATIONS` **before URL, query, headers, body, authentication, or dispatch**. Unknown methods deny.
5. **Containment.** Verify generated projects in a scrubbed temporary workspace, after package inspection and with a generated lockfile. Use `npm ci --ignore-scripts` with inherited proxy settings disabled, then typecheck, test, build, and run a local MCP stdio smoke test. Use a container, VM, or equivalent host sandbox when the project or dependency graph is untrusted.
6. **Agent installation (optional).** After a verified project is generated, ask whether the user wants **project only** or **project + agent installation**. Project-only is the default. For installation, detect clients read-only, present the detected targets and exact config paths/command/args/cwd/env *names* plus backup paths, and require a separate final confirmation bound to the reviewed installation plan. Never read `.env`, copy secret values, silently replace a server name, or mutate an undetected/unsupported client; provide a portable `mcpServers.json` export instead.
7. **Publication.** **Immediately before GitHub publication**, record owner/org, repository name, visibility, and source branch. Resolve the actual checked-out/ref-to-publish branch and stop unless it exactly equals the recorded source branch. Ask for explicit user confirmation before the publication action.

## Optional agent installation workflow

Only use this after generated-project verification succeeds. Read-only discovery covers Hermes, Claude Code, Codex, Cursor, VS Code/Copilot, Gemini CLI, and OpenCode. This release has verified native config adapters for **Codex, Cursor, VS Code/Copilot, Gemini CLI, and OpenCode**, plus official CLI adapters for **Hermes** (`hermes mcp add` then `hermes mcp test`) and **Claude Code** (`claude mcp add --transport stdio` then `claude mcp list`). Hermes and Claude Code configuration files are never guessed or edited directly. If either CLI is missing or its add/verification action fails, the adapter removes a just-added server when possible and reports the target as failed; use portable export instead.

```bash
# 1. The assistant asks: "프로젝트만 생성할까요, 아니면 생성 후 에이전트에 탑재할까요?"
# 2. For install, inspect and show a secret-free plan before any config write.
python3 "$SKILL_DIR/scripts/api_to_typemcp.py" install-plan \
  --project "$OUTPUT" --targets "cursor,gemini-cli"

# 3. Review the preview, then explicitly issue the plan-bound one-time confirmation.
PLAN_DIGEST="...shown by install-plan..."
python3 "$SKILL_DIR/scripts/api_to_typemcp.py" install-approve --plan-digest "$PLAN_DIGEST"

# 4. Apply only the unchanged approved plan. Native registration is fail-closed
#    unless the selected client already has a detected regular config file. Each
#    target gets a 0600 backup; a later target failure restores earlier targets,
#    and every write is reread/parsed before success is reported.
python3 "$SKILL_DIR/scripts/api_to_typemcp.py" install-apply \
  --project "$OUTPUT" --targets "cursor,gemini-cli" --confirm-plan-digest "$PLAN_DIGEST"
```

For no-write portability, use `install-export --project "$OUTPUT"`; it writes only
`$OUTPUT/agent-install/mcpServers.json`, never an agent configuration. Preview and
receipts expose `env_names` only—never `.env` content or credential values.

## Runtime compatibility

Read [references/type-mcp-runtime.md](references/type-mcp-runtime.md) before modifying generated TypeScript. The default generated standard ESM path uses the public ESM/NodeNext decorator import:

```ts
import { McpServer, McpTool } from "@theorvane/type-mcp";
```

Use only `McpServer`, `McpTool`, `createMcpServer`, `startStdioServer`, `zod`, and an explicit `InstanceResolver` from the public contract. Legacy decorators are a separate, opt-in compatibility surface for CommonJS/Node16 projects that enable `experimentalDecorators`:

```ts
import { McpServer, McpTool } from "@theorvane/type-mcp/legacy";
```

These are distinct entrypoints with distinct decorator semantics. Do not change the generator templates to the legacy/CommonJS path; generated projects remain standard ESM consumers and never copy runtime source.

## Verification checklist

- [ ] Source is supplied explicitly; no origin crawling occurred.
- [ ] Manifest is secret-free, evidence-backed, and canonically digested.
- [ ] Digest approval and a valid single-use receipt precede generation.
- [ ] Output target passed the empty/replace and traversal/symlink safety gates.
- [ ] Protected writes are authorized before request construction.
- [ ] Generated project uses the published `@theorvane/type-mcp@0.3.2` release line only and includes a reviewed `package-lock.json`; confirm registry provenance before changing this version.
- [ ] Contained `npm ci --ignore-scripts`/typecheck/test/build/MCP smoke passes; external sandboxing is used for untrusted dependency installation.
- [ ] Immediately before GitHub publication, user confirms owner/name/visibility/source branch and the resolved branch matches.
