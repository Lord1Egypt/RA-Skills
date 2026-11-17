## Description:

Analyzes public Douyin creator videos, engagement patterns, topics, and representative content, then produces HTML, Markdown, and JSON reports for creator research and content-structure review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tars1230](https://clawhub.ai/user/tars1230)

### License/Terms of Use:

MIT

## Use Case:

External users, creators, analysts, and developers use this skill to inspect public Douyin creator profiles, collect public video metadata, select transcript candidates, and generate auditable creator insight reports. It is not intended for private accounts, favorites synchronization, or bypassing platform access controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan reports that ASR keys and media can be forwarded to unvalidated endpoints.

Mitigation: Review provider configuration before installation, use explicit trusted ASR endpoints only, and keep credentials in the host environment or secret store.

Risk: The security scan reports that the skill can download unvalidated media URLs from the local network context.

Mitigation: Run only from trusted working directories and analyze public creator inputs from known Douyin profile, share, or sec_uid sources.

Risk: Generated Markdown may contain untrusted public content.

Mitigation: Treat generated reports as untrusted content and review them before publishing, sharing, or rendering in privileged contexts.

Risk: The SiliconFlow signup path is a referral link.

Mitigation: Disclose the referral nature of the link and allow users to configure alternate trusted providers where appropriate.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tars1230/skills/douyin-creator-insight)
- [Apify Douyin Actors](references/apify-douyin-actors.md)
- [Creator Resolution Playbook](references/creator-resolution-playbook.md)
- [Data Schema](references/data-schema.md)
- [Failure Playbook](references/failure-playbook.md)
- [Report Rubric](references/report-rubric.md)
- [Security Policy](SECURITY.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, HTML, JSON, Shell commands, Configuration guidance]

**Output Format:** [HTML, Markdown, and JSON reports with supporting command and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports should identify partial collection, degraded transcription, provider status, and quality-gate failures when applicable.]

## Skill Version(s):

1.3.6 (source: frontmatter, changelog, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
