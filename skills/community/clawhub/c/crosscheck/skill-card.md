## Description:

Crosscheck sends drafts, delivered work, or skills for independent review and returns a JSON verdict with findings and a signed receipt.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maxugc](https://clawhub.ai/user/maxugc)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use Crosscheck to get an independent review of drafts for factual, arithmetic, consistency, placeholder, confidentiality, commitment, and tone issues before sharing them. They can also review delivered work or a skill, and check x402 seller endpoints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scanner flagged unpinned npm commands that could run changing package versions with local permissions; scan coverage is incomplete.

Mitigation: Use a reviewed, pinned package version with verified integrity, and limit the client's access to local files and environment data.

Risk: Drafts and skill files submitted for review are sent to the service.

Mitigation: Keep confidential material out of submissions.

## Reference(s):

- [Crosscheck HTTP API reference](references/API.md)
- [Crosscheck API overview](https://crosscheckapi.com/llms.txt)
- [Crosscheck source bundle checksums](https://crosscheckapi.com/skill/SHA256SUMS)
- [Crosscheck ClawHub release](https://clawhub.ai/maxugc/skills/crosscheck)

## Skill Output:

**Output Type(s):** [Analysis, JSON verdicts, Review findings, Signed receipts, Seller reports]

**Output Format:** [Structured JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Verdicts include findings; receipts are signed.]

## Skill Version(s):

0.6.0 (source: server-resolved ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
