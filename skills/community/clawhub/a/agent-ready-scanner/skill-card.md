## Description:

Agent Ready Scanner checks a website's readiness for AI agents across discoverability, content accessibility, bot access control, protocol discovery, and commerce signals, then produces a scored report with remediation guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maooson](https://clawhub.ai/user/maooson)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, site owners, and agent-readiness reviewers use this skill to scan authorized public websites for AI-agent discoverability, access, protocol, and commerce signals. The skill helps them identify missing endpoints or configuration and generate practical fix guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe URL handling can make scans risky when pointed at localhost, private networks, cloud metadata endpoints, or other unauthorized targets.

Mitigation: Run scans only against authorized public websites, preferably from an environment with egress controls that block localhost, private networks, and cloud metadata endpoints.

Risk: Generated HTML reports may contain untrusted dynamic fields.

Mitigation: Treat generated HTML reports as untrusted until dynamic report fields are escaped by the report generator.

Risk: The server security verdict is suspicious because the skill mostly matches its claims but has review-worthy security issues.

Mitigation: Review before installing and scan the skill before deployment.

## Reference(s):

- [isitagentready.com](https://isitagentready.com)
- [llms.txt](https://llmstxt.org/)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [Agent Skills](https://agentskills.io/)
- [x402](https://www.x402.org/)
- [A2A](https://a2a.io/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON scan output, and generated HTML report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [HTML reports include a readiness score, category breakdowns, check details, and fix suggestions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
