## Description:

Discover Snowflake Cortex, Snowpark, notebook, Streamlit, MCP, and AI-observability assets from the operator's environment, emit canonical agent-bom inventory JSON, and scan it without giving agent-bom long-lived Snowflake credentials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[msaad00](https://clawhub.ai/user/msaad00)

### License/Terms of Use:

Apache-2.0

## Use Case:

Developers and cloud operators use this skill to inventory Snowflake Cortex and related AI assets from operator-approved accounts with read-only access. It writes canonical inventory JSON for an optional local agent-bom scan when the operator requests findings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment has medium confidence and is incomplete because a referenced local path was missing.

Mitigation: Check that the skill fits the intended use and review the referenced material if it is available before installing.

Risk: Snowflake discovery uses authenticated access to account metadata and AI workload information.

Mitigation: Use only operator-approved accounts and read-only roles, prefer existing SSO, OAuth, or key-pair authentication, and never paste passwords, private keys, passphrases, or tokens into chat.

## Reference(s):

- [agent-bom project repository](https://github.com/koda-ai-studio/agent-bom)
- [agent-bom on PyPI](https://pypi.org/project/agent-bom/)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Configuration guidance]

**Output Format:** [Canonical JSON inventory file and Markdown guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Inventory is written to an operator-selected path; credential-like values are redacted before persistence or export.]

## Skill Version(s):

0.115.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
