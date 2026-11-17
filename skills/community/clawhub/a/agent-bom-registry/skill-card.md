## Description:

MCP server security registry and trust assessment — look up servers in the 1320-entry server security metadata registry, run pre-install marketplace checks, batch fleet risk scoring, assess skill file trust, and run SAST code scans. Use when the user mentions MCP server trust, registry lookup, marketplace check, or skill trust assessment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[msaad00](https://clawhub.ai/user/msaad00)

### License/Terms of Use:

Apache-2.0

## Use Case:

Developers and security engineers use the skill to look up MCP server trust metadata, check packages before installation, assess fleets and skill files, and run optional code security scans.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional Snyk enrichment for code scans contacts a third-party endpoint and requires an operator token.

Mitigation: Use enrichment only when the external service is appropriate, and keep SNYK_TOKEN in the operator environment.

Risk: A benign scan does not guarantee that the skill fits a particular environment or is risk-free.

Mitigation: Review the skill and decide whether it suits your needs before using it.

## Reference(s):

- [agent-bom project](https://github.com/koda-ai-studio/agent-bom)
- [agent-bom on PyPI](https://pypi.org/project/agent-bom/)
- [OpenSSF Scorecard](https://securityscorecards.dev/viewer/?uri=github.com/koda-ai-studio/agent-bom)

## Skill Output:

**Output Type(s):** [Analysis, Guidance]

**Output Format:** [Text summaries with registry results, trust assessments, and scan findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results may include optional Semgrep SAST or Snyk vulnerability-enrichment findings.]

## Skill Version(s):

0.115.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
