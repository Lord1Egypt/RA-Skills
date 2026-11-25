## Description:

MCP server security registry and trust assessment — look up servers in the 1356-entry server security metadata registry, run pre-install marketplace checks, batch fleet risk scoring, assess skill file trust, and run SAST code scans. Use when the user mentions MCP server trust, registry lookup, marketplace check, or skill trust assessment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[msaad00](https://clawhub.ai/user/msaad00)

### License/Terms of Use:

Apache-2.0

## Use Case:

Developers and security engineers use this skill to look up MCP server security metadata, check packages before installation, score server inventories, assess skill files, and run SAST scans.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional Snyk vulnerability enrichment for code scans uses the sensitive SNYK_TOKEN credential.

Mitigation: Keep the token in the operator environment and out of prompts and skill output; bundled registry lookups do not require it.

## Reference(s):

- [agent-bom project](https://github.com/koda-ai-studio/agent-bom)
- [agent-bom on PyPI](https://pypi.org/project/agent-bom/)
- [OpenSSF Scorecard](https://securityscorecards.dev/viewer/?uri=github.com/koda-ai-studio/agent-bom)
- [ClawHub skill page](https://clawhub.ai/msaad00/skills/agent-bom-registry)

## Skill Output:

**Output Type(s):** [Analysis, Text, Security findings, Risk scores, Shell commands]

**Output Format:** [Structured text and security analysis]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Registry matches, trust assessments, marketplace checks, fleet risk scores, and SAST findings; registry lookups use bundled data.]

## Skill Version(s):

0.115.6 (source: frontmatter; ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
