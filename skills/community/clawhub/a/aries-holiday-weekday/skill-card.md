## Description:

Query gov.cn Chinese holiday notices to determine workdays, holidays, and make-up workdays.

This skill is ready for commercial/non-commercial use.

## Publisher:

[silent-blue](https://clawhub.ai/user/silent-blue)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to check whether China-specific dates or full months are workdays, statutory holidays, or weekend make-up workdays using official State Council holiday notices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper script can make outbound web requests and fetch notice pages.

Mitigation: Install only if outbound gov.cn access is acceptable, and restrict notice fetching to official gov.cn HTTPS hosts.

Risk: The release includes credential-like gov.cn signing material for search requests.

Mitigation: Review the signing material before deployment and replace it with an authorized configuration path where required.

Risk: The helper script can write skill-local cache files.

Mitigation: Keep cache refresh behavior documented and refresh only as needed for official annual holiday schedule updates.

## Reference(s):

- [Gov Holiday Reference](references/api_reference.md)
- [2026 State Council holiday notice](https://www.gov.cn/gongbao/2025/issue_12406/202511/content_7048922.html)
- [Aries Holiday Weekday on ClawHub](https://clawhub.ai/silent-blue/skills/aries-holiday-weekday)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown table for month queries or a short structured summary for single-date queries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use official gov.cn notices and skill-local yearly JSON cache data to classify dates.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
