## Description:

This skill helps retainer-based podcast clipping agencies turn episodes into branded short clips, obtain client approval, schedule posts, track status, report results, and offboard clients.

This skill is ready for commercial/non-commercial use.

## Publisher:

[social-media-skills](https://clawhub.ai/user/social-media-skills)

### License/Terms of Use:

MIT

## Use Case:

Podcast clipping agencies use the skill to manage each client’s workflow from episode intake and clip production through review, posting, and monthly reporting. It helps an agency’s AI agent keep approvals, client accounts, and publishing records organized.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags RSS input and upload destinations for review.

Mitigation: Check the episode source and intended destination before processing or uploading; keep each client’s posts within that client’s project.

Risk: The security review flags API credential handling.

Mitigation: Treat API keys as passwords; do not put them in shared chats or commit them to files.

Risk: The security review flags approval handling, including silence-based approval.

Mitigation: Use silence as approval only when the client agreed to it in writing; otherwise hold clips until an explicit approval is recorded.

## Reference(s):

- [Clip rubric](artifact/references/clip-rubric.md)
- [Approval workflow](artifact/references/approval.md)
- [Client and episode configuration](artifact/references/client-file.md)
- [WoopSocial setup and posting workflow](artifact/references/woopsocial.md)
- [WoopSocial agent setup](https://woopsocial.com/agents?utm_source=clipping-agency-skill&utm_medium=skill)

## Skill Output:

**Output Type(s):** [Video clips, HTML approval pages, JSON records, Markdown schedules and reports, Shell commands]

**Output Format:** [Video files, HTML, JSON, and Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Clip counts and platform-specific formats follow each client’s configuration.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
