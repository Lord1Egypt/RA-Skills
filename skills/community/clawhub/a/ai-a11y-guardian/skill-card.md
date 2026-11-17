## Description:

AI辅助无障碍合规守护者 — 自动化检测网页/移动端H5的无障碍问题，生成修复建议并出具合规报告

This skill is ready for commercial/non-commercial use.

## Publisher:

[zlszhonglongshen](https://clawhub.ai/user/zlszhonglongshen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, accessibility testers, and compliance teams use this skill to audit Web and mobile H5 pages against WCAG 2.1/2.2 and generate structured findings, repair guidance, and compliance report cards.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow opens supplied pages in Chromium, executes page JavaScript, and captures rendered DOM, screenshots, and iframe content for analysis.

Mitigation: Run it only on approved public or authorized pages, and avoid private, authenticated, internal, regulated, or secret-bearing pages unless data handling has been approved.

Risk: AI-generated WCAG findings and repair snippets may miss issues or produce guidance that still needs validation.

Mitigation: Treat the report as an accessibility triage aid and verify important findings with manual review and assistive-technology testing before relying on it for formal compliance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zlszhonglongshen/skills/ai-a11y-guardian)
- [ClawHub publisher profile](https://clawhub.ai/user/zlszhonglongshen)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance, files]

**Output Format:** [Markdown or structured text with accessibility findings, WCAG references, repair snippets, and optional report card image files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include severity ratings, accessibility scores, affected page context, and generated compliance summary cards.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
