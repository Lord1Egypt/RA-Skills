## Description:

Extract and summarize titles, authors, updates, and content from publicly shared Dingtalk pages, apps, and group invitations without internal API access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codekungfu](https://clawhub.ai/user/codekungfu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to extract human-readable summaries and structured fields from publicly accessible DingTalk share pages, app pages, announcements, and group invitation pages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may try to apply the skill to private enterprise DingTalk content or authenticated workflows outside its defined scope.

Mitigation: Use it only with publicly accessible pages and avoid account actions, messaging, admin tasks, internal APIs, or any content that requires authentication.

Risk: Dynamic pages may be parsed before content finishes rendering, producing incomplete summaries.

Mitigation: Wait for page rendering to complete before extraction and verify key fields against the visible public page.

Risk: Repeated access to public pages can create unnecessary traffic or violate platform expectations.

Mitigation: Apply frequency controls and avoid repeated requests when collecting public page information.

## Reference(s):

- [DingTalk homepage](https://www.dingtalk.com/)
- [ClawHub skill page](https://clawhub.ai/codekungfu/skills/dingtalk-hot-trend)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or structured text summaries with extracted fields and relevant links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are limited to public DingTalk content and may include titles, authors, update times, summaries, tags, source links, app details, version information, and invitation-page notes.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
