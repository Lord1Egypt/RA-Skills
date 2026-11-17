## Description:

Scan AI agent skills for malware, credential theft, prompt injection, and dangerous permissions before installing them.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aurasecurity-creator](https://clawhub.ai/user/aurasecurity-creator)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users use this skill to submit OpenClaw, Claude MCP, or LangChain skill URLs for pre-installation security analysis and safety verdicts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends the user-provided skill URL and basic scan options to an external AURA API endpoint.

Mitigation: Scan only public or shareable skill URLs unless the user trusts the configured AURA_API_URL endpoint for private repository or internal URL data.

Risk: Scan availability and behavior depend on the configured AURA_API_URL service.

Mitigation: Configure AURA_API_URL deliberately and treat API errors or timeouts as inconclusive scan results.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aurasecurity-creator/skills/aura-security-scanner)
- [AURA Security website](https://aurasecurity.io)
- [AURA Security repository](https://github.com/aurasecurityio/aura-security)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown scan report with verdict, risk score, findings, summary, and recommendations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return a no-URL prompt or API error message when input is missing or the external scan request fails.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
