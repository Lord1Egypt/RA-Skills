## Description:

Reviews drafts, delivered work, and skill files for issues before they are shared, accepted, or installed, returning a verdict and signed receipt.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maxugc](https://clawhub.ai/user/maxugc)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and developers use Crosscheck to review drafts before sharing them, check another agent's deliverable against its task, or inspect skill and MCP files before installation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An unpinned npm package receives a wallet private key.

Mitigation: Use a verified or pinned package version and a dedicated low-balance wallet; set a strict spending limit before use.

Risk: Drafts and selected skill files are sent to a third-party review service.

Mitigation: Exclude confidential or regulated material unless sharing is explicitly approved.

## Reference(s):

- [Crosscheck API reference](references/API.md)
- [Crosscheck service documentation](https://crosscheckapi.com/llms.txt)
- [Crosscheck release on ClawHub](https://clawhub.ai/maxugc/skills/crosscheck)
- [Package checksums](https://crosscheckapi.com/skill/SHA256SUMS)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Text]

**Output Format:** [JSON verdict and signed receipt; concise review guidance for the agent]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Verdicts may identify issues, unmet requirements, or skill-security findings; paid checks return a receipt.]

## Skill Version(s):

0.5.5 (source: ClawHub release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
