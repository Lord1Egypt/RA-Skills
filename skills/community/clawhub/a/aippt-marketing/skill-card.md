## Description:

小方同学营销方案 Agent helps an agent turn a topic, file, or link into a structured marketing plan and generated PPT-style visuals through the AIPPT marketing API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaok8700](https://clawhub.ai/user/xiaok8700)

### License/Terms of Use:

MIT-0

## Use Case:

External users and marketing teams use this skill with an agent to create marketing plan drafts, presentation-style visuals, and downloadable deliverables from a topic, file, or web link. It is intended for users who have an AIPPT account and the member credits required by the service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Marketing briefs, uploaded documents, customer data, and generated outputs may be sent to AIPPT and exposed through tmpfiles.org public links.

Mitigation: Use non-confidential inputs unless data sharing is approved, and review generated files and public links before sharing them.

Risk: The skill can handle account credentials and bearer tokens during login.

Mitigation: Prefer browser-based login over giving the assistant a password, use a low-risk account, and avoid storing tokens outside the active session.

Risk: Generated marketing plans may contain inaccurate claims or brand-inappropriate recommendations.

Mitigation: Have a qualified reviewer check factual claims, legal compliance, and brand suitability before publication.

## Reference(s):

- [小方同学营销 API 详细参考](references/api-details.md)
- [AIPPT Homepage](https://www.aippt.cn)
- [ClawHub Skill Page](https://clawhub.ai/xiaok8700/skills/aippt-marketing)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, files, guidance]

**Output Format:** [Markdown responses with generated marketing-plan text, page image embeds, and downloadable PDF/Markdown file links.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an AIPPT account, member credits, browser or API login, and review before sharing generated public links.]

## Skill Version(s):

1.2.9 (source: package.json and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
