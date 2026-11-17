## Description:

Scans explicit public social profile URLs before a date and produces a Date Intel Report with interest mapping, personality and values observations, red and green flags, and conversation suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sophie-xin9](https://clawhub.ai/user/sophie-xin9)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to review a date prospect's public social media profiles and receive a concise pre-date report. The report is intended to support conversation planning and cautious interpretation, not background investigation or conclusions about private traits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bundled deep-profile collectors can collect broad account-linked data from the user's logged-in social-media sessions.

Mitigation: Run only against explicit public profile URLs, avoid running bundled collectors while logged in to personal accounts, and review collected data before sharing or relying on it.

Risk: ManoBrowser access and API keys can expose browser automation capabilities to untrusted endpoints.

Mitigation: Pin or manually review ManoBrowser before loading it, and do not pass ManoBrowser API keys on the command line or to untrusted endpoints.

Risk: The generated profile can overstate conclusions from limited public social-media signals.

Mitigation: Keep report language probabilistic, avoid sensitive inferences, cite public-data basis for conclusions, and treat the report as a conversation aid rather than a decision record.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sophie-xin9/skills/blind-date-mirror)
- [ClawHub publisher profile](https://clawhub.ai/user/sophie-xin9)
- [ManoBrowser dependency](https://github.com/ClawCap/ManoBrowser)

## Skill Output:

**Output Type(s):** [markdown, text, guidance, shell commands]

**Output Format:** [Markdown report with structured sections and occasional inline shell commands for setup or browser-connectivity checks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local raw-data JSON and report files during collection workflows.]

## Skill Version(s):

1.0.0 (source: evidence.release.version and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
