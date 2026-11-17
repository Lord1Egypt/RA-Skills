## Description:

Builds responsive email HTML and render-QA handoffs from approved email creative or existing HTML, including dark-mode, accessibility, image-off, client-render, and plain-text parity checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaron-he-zhu](https://clawhub.ai/user/aaron-he-zhu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, email marketers, and marketing operations teams use this skill to convert approved email creative into responsive table-based HTML and to produce a render-QA report across common email clients. It is intended for build and QA work, not copywriting, scoring, or campaign sending.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated email HTML or render-QA guidance may be incorrect for a target client if it is not verified with a real seed-list or inbox-preview test.

Mitigation: Treat untested render results as Estimated, run a seed or inbox-preview test for important sends, and review the client-render matrix before deployment.

Risk: A live ESP render test can send email if the user explicitly chooses that path.

Mitigation: Use only verified sender identities and the user's own test inboxes, and treat any live send as an explicit action requiring confirmation.

Risk: The skill may save render-QA handoff summaries to memory after confirmation.

Mitigation: Review saved handoffs for sensitive campaign, brand, or customer data before confirming persistence.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/aaron-he-zhu/skills/email-render-builder)
- [Project Homepage](https://github.com/aaron-he-zhu/aaron-marketing-skills)
- [Email Render Specs](references/email-render-specs.md)
- [Client Render Matrix](references/client-render-matrix.md)

## Skill Output:

**Output Type(s):** [Markdown, Code, Configuration instructions, Guidance]

**Output Format:** [Markdown with email HTML code and render-QA checklist sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include client-render pass/fail rows, accessibility and dark-mode checks, image-off fallback notes, plain-text parity, and handoff summary text.]

## Skill Version(s):

19.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
