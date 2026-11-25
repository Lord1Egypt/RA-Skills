## Description:

Inventory GCP-hosted AI agent and MCP-relevant assets, export canonical agent-bom JSON, and optionally scan the inventory using operator-controlled read-only credentials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[msaad00](https://clawhub.ai/user/msaad00)

### License/Terms of Use:

Apache-2.0

## Use Case:

Developers and cloud security engineers use this skill to inventory approved GCP projects for Vertex AI, Cloud Run, Cloud Functions, GKE, and related agentic infrastructure. It writes a canonical inventory file and can scan that file when requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The partial security scan classified the skill as suspicious because it flagged references to Google Cloud credential files and could not resolve a local script reference; this does not establish malicious intent.

Mitigation: Review credential handling and resolve the local script reference before installing. Use operator-approved projects and read-only credentials, and never paste or display credential values.

## Reference(s):

- [Project homepage](https://github.com/koda-ai-studio/agent-bom)
- [PyPI package](https://pypi.org/project/agent-bom/)

## Skill Output:

**Output Type(s):** [JSON, Analysis]

**Output Format:** [Canonical agent-bom inventory JSON, with optional scan findings JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Inventory is written to an operator-selected path; scanning occurs only when requested.]

## Skill Version(s):

0.115.6 (source: frontmatter, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
