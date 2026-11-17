## Description:

Validate and ingest operator-pushed agent-bom inventory JSON from AWS, Azure, GCP, Snowflake, CMDB, or endpoint collectors for local findings, graphs, policy, provenance, and auditor-ready exports without giving agent-bom direct cloud credentials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[msaad00](https://clawhub.ai/user/msaad00)

### License/Terms of Use:

Apache-2.0

## Use Case:

Developers and security engineers can validate canonical inventory JSON produced by an operator, collector, CMDB, or agent workflow, then use agent-bom for local scans, graphs, policy checks, provenance review, and audit exports. The workflow avoids giving agent-bom direct cloud credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional vulnerability lookups contact OSV and GitHub Advisory endpoints during local scans.

Mitigation: Enable external lookups only when they are acceptable for the environment.

Risk: Optional control-plane push sends inventory to a destination supplied by the operator and uses an API token.

Mitigation: Confirm the destination and authentication method are operator-controlled, and keep the token out of chat and logs.

Risk: The security analysis was partial because a local path-like reference could not be resolved.

Mitigation: Review the skill and unresolved reference before installation; treat the benign verdict as incomplete evidence.

## Reference(s):

- [agent-bom project](https://github.com/koda-ai-studio/agent-bom)
- [agent-bom on PyPI](https://pypi.org/project/agent-bom/)
- [OSV vulnerability API](https://api.osv.dev/v1)
- [GitHub Advisory API](https://api.github.com/advisories)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Analysis, JSON, SARIF, HTML, Markdown, CycloneDX, SPDX]

**Output Format:** [Markdown guidance and shell commands; agent-bom exports findings and inventory reports as JSON, SARIF, HTML, Markdown, CycloneDX, or SPDX.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3.11+ and agent-bom 0.84.4+; inventory must conform to the packaged schema.]

## Skill Version(s):

0.115.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
