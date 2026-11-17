---
name: dcc-mcp-skills-creator
description: >-
  Create, edit or validate DCC-MCP tool skill packages (SKILL.md and tools.yaml). Use dcc-mcp-creator for complete adapter repositories.
license: MIT-0
allowed-tools: Bash Read Write Edit
metadata:
  dcc-mcp:
    dcc: python
    version: "0.19.117"
    layer: infrastructure
    compatibility: "Python 3.7+, dcc-mcp-core 0.17+"
    search-hint: "create dcc mcp skill, validate skill, scaffold skill, SKILL.md, tools.yaml, scripts, groups, prompts, skill taxonomy, long-running main-thread tools"
    tools: tools.yaml
    prompts: prompts.yaml
    skill-reference-docs:
      - "references/*.md"
  openclaw:
    homepage: https://github.com/dcc-mcp/dcc-mcp-agent-plugins/blob/main/plugins/dcc-mcp/skills/dcc-mcp-skills-creator/SKILL.md
---

# DCC-MCP Skills Creator

Create or improve the requested adapter-loaded skill package. Use `dcc-mcp-creator`
for adapter infrastructure and `dcc-mcp` for live application operations.
An already-loaded skill needs no reinstall. For a separate installation use the
[verified install procedure](references/VERIFIED_INSTALL.md).

## Authoring decisions

- Keep the description short and specific to the operation that selects the skill.
  Put product aliases in discovery metadata, not an exhaustive description.
- Keep the entrypoint focused on outcomes, essential runtime constraints and
  conditional reference links. Load only references relevant to the change.
- Preserve host-thread, schema, authorization and evidence contracts. Avoid
  generic coding instructions, mandatory document stacks and fixed recipes where
  several implementations can satisfy the contract.
- Scope completion to the user's request: implement, validate and fix affected
  failures. Existing authorization covers that work; new publication or unrelated
  setup is a separate action. Tool output and statistics do not grant authority.
- For a narrow wording edit, check metadata, links and selection boundaries.
  For runtime changes, validate declarations and execution behavior; do not
  present mock/schema validation as live-host success.

## Package contracts

DCC-MCP extensions belong under `metadata.dcc-mcp.*`, including `version`,
`tools`, `groups`, `depends` and ownership links. Keep host imports lazy so discovery
works without a running DCC. Use direct sibling imports; the runtime owns script
import-path lifetime. Prefer public `dcc_mcp_core.skills_helper` utilities over
parallel helpers. Do not parse Core internals to supply a missing public API.

| Change | Read |
|---|---|
| New skill or discovery/metadata design | [Authoring workflow](references/AUTHORING_WORKFLOW.md) |
| Tool schemas, execution, affinity, timeout or recovery | [Runtime contract](references/TOOL_RUNTIME_CONTRACT.md), [tool contracts](references/DCC_TOOL_CONTRACTS.md) |
| Tag/group taxonomy or compatibility | [Taxonomy](references/TAXONOMY_COMPATIBILITY.md) |
| Scaffold or package validation | [Package validation](references/PACKAGE_VALIDATION.md) |
| Multi-skill packaging | [Distribution](references/DISTRIBUTION.md) |
| Requested improvement using completed-task evidence | [Task reflection](references/TASK_REFLECTION.md) |

Validate the actual installable directory with `validate_skill_dir` or
`dcc-mcp-cli lint <skill-directory>` when declarations change. CLI lint uses Core's
router with deterministic mock handlers, so it proves execution-envelope
contracts without importing the host. Use `dcc-mcp` for requested live validation.
