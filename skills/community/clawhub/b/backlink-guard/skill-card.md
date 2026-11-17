## Description:

Checks backlink sources before submission, verifies live listings, and audits backlink profiles for link-spam patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhuyansen](https://clawhub.ai/user/zhuyansen)

### License/Terms of Use:

MIT-0

## Use Case:

Site owners and SEO practitioners use it to find and assess link opportunities, verify published listings, audit backlink profiles, and inspect competitor or AI search visibility.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research queries are sent to external API providers when their optional keys are configured.

Mitigation: Use providers you trust and review the query information before running API-backed research.

Risk: Paid calls can cost more than their estimates.

Mitigation: Review estimated costs and use --max-usd where available; treat it as a cap on estimates, not a guaranteed billing ceiling.

Risk: Logs, paid answers, and observed networks persist locally.

Mitigation: Review the local state directory and use BACKLINK_GUARD_STATE when a different storage location is appropriate.

Risk: A suggested listing or submission may be unsuitable or misleading.

Mitigation: Review the evidence and proposed text, and obtain explicit user approval before submitting anything.

## Reference(s):

- [Backlink Guard on ClawHub](https://clawhub.ai/zhuyansen/skills/backlink-guard)
- [Glasser API](https://link.glasser.ai/JasonZhu)
- [AIsa API](https://go.aisa.one/yansen-zhu)
- [GoAnyAPI](https://goanyapi.com/r/ga-95708898fb)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown reports with optional JSON CLI output and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Research results may be estimates; paid queries can exceed estimated costs, and findings are guidance rather than Google's verdict.]

## Skill Version(s):

0.11.2 (source: server-resolved release metadata; pinned in SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
