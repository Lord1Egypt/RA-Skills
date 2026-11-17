## Description:

Professional fundraising advisory skill for startups - AI-powered project assessment, pitch deck generation, valuation analysis, investor matching, and PDF processing (financial statements, OCR, reports).

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhenstaff](https://clawhub.ai/user/zhenstaff)

### License/Terms of Use:

MIT

## Use Case:

External startup founders and investors use this skill to structure fundraising analysis, generate pitch deck and business plan materials, estimate valuation ranges, match investor profiles, and prepare investment memo or due diligence guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may process confidential fundraising data or financial statements.

Mitigation: Use an isolated workspace, redact unnecessary sensitive information, and review generated materials before storing or sharing them.

Risk: PDF or report generation may save sensitive output files to paths influenced by company names.

Mitigation: Choose explicit safe output paths, sanitize file names, and disable automatic PDF generation when it is not needed.

Risk: Generated valuations, investor recommendations, and due diligence materials can be incomplete or misleading if inputs are stale or partial.

Mitigation: Treat outputs as advisory drafts and validate financial assumptions, market data, investor fit, legal issues, and accounting details with qualified reviewers.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhenstaff/skills/fundraising-advisor)
- [Project homepage from ClawHub metadata](https://github.com/ZhenRobotics/openclaw-fa)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown with structured sections and optional code or shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce fundraising assessments, pitch deck outlines, business plans, valuation summaries, investor matching lists, outreach strategies, investment memos, due diligence checklists, and optional local report files.]

## Skill Version(s):

1.0.0 (source: release evidence, SKILL.md frontmatter, pyproject.toml, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
