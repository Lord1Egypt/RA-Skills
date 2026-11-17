## Description:

Discover Snowflake Cortex, Snowpark, notebook, Streamlit, MCP, and AI-observability assets from the operator's environment, emit canonical agent-bom inventory JSON, and scan it without giving agent-bom long-lived Snowflake credentials. Use when a user asks to inventory Snowflake AI or Cortex infrastructure as canonical inventory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[msaad00](https://clawhub.ai/user/msaad00)

### License/Terms of Use:

Apache 2.0

## Use Case:

Developers and platform engineers use this skill to inventory Snowflake AI, Cortex, and related workload assets through operator-approved read-only access. It saves schema-validated inventory JSON for an optional agent-bom scan when requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review was partial because a referenced local path could not be resolved; a benign verdict is not a guarantee of safety.

Mitigation: Review the referenced path and skill instructions when available before installing or running the skill.

Risk: Snowflake discovery uses authenticated account access and can save inventory to a local file.

Mitigation: Use operator-approved read-only roles, keep credentials in the operator environment, and write inventory only to a path you chose.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/msaad00/skills/agent-bom-discover-snowflake)
- [agent-bom project repository](https://github.com/koda-ai-studio/agent-bom)
- [agent-bom on PyPI](https://pypi.org/project/agent-bom/)

## Skill Output:

**Output Type(s):** [JSON files, Shell commands, Guidance]

**Output Format:** [Canonical inventory JSON and optional scan findings JSON; shell commands in Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Inventory is written to an operator-selected path; credential-like values are redacted.]

## Skill Version(s):

0.115.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
