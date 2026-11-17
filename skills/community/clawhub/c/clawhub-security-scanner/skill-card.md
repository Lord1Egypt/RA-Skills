## Description:

Audits SKILL.md content for permission overreach, prompt injection, and scope mismatch before installation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ordo-tech](https://clawhub.ai/user/ordo-tech)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill users use this skill to run a first-pass security audit on local, pasted, or URL-hosted SKILL.md content before installing or updating a ClawHub skill.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may fetch user-provided URLs while producing a first-pass security audit.

Mitigation: Use remote scans only for skill content you intend to review, and inspect audit conclusions before acting on them.

Risk: Generated reports include a commercial Security Pack promotion.

Mitigation: Treat the promotion as non-security content and base install decisions on the reported findings and independent review.

Risk: The documentation may overstate or blur the free scanner's actual coverage.

Mitigation: Treat this skill as a three-category first-pass screen and use deeper review for suspicious or high-stakes installs.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ordo-tech/skills/clawhub-security-scanner)
- [Publisher Profile](https://clawhub.ai/user/ordo-tech)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown security audit report with a risk score, findings table, summary, and recommendation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include excerpts from the reviewed SKILL.md and a commercial Security Pack link in generated reports.]

## Skill Version(s):

1.1.1 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
