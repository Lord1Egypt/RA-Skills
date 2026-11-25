## Description:

Find Xiaohongshu (RedNote) accounts, retrieve creator profiles, and list their notes with engagement counts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[data-x-api](https://clawhub.ai/user/data-x-api)

### License/Terms of Use:

MIT-0

## Use Case:

External users such as marketers and researchers use the skill to find creator or brand accounts, check profile metrics and verification, review notes, and compare accounts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill recommends an unpinned third-party CLI and sending full share links or text to DataXAPI, which may expose information the user did not intend to share.

Mitigation: Prefer sharing only the needed profile ID, verify the package version and API destination, and consider whether sending any full link or text is appropriate.

Risk: The security scan inspected only one Markdown component and could not resolve some local references, so review coverage is incomplete.

Mitigation: Review the unresolved references and verify the package version and API destination before installation.

## Reference(s):

- [DataXAPI Xiaohongshu creator profile API](https://dataxapi.com/apis/xiaohongshu/users/get/)
- [DataXAPI Xiaohongshu account search API](https://dataxapi.com/apis/xiaohongshu/users/search/)
- [DataXAPI Xiaohongshu notes API](https://dataxapi.com/apis/xiaohongshu/users/notes/list/)
- [DataXAPI agent setup guide](https://dataxapi.com/agents.md)

## Skill Output:

**Output Type(s):** [API data, JSON, Text]

**Output Format:** [Structured JSON data summarized as text or Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creator profile fields, note details and engagement counts; results may be paginated and calls are paid.]

## Skill Version(s):

1.0.0 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
