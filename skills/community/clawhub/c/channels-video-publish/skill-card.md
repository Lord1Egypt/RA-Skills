## Description:

Automates publishing prepared videos to WeChat Channels, including scheduling, batch queues, publication checks, and rescheduling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiaxinmmhh](https://clawhub.ai/user/jiaxinmmhh)

### License/Terms of Use:

MIT-0

## Use Case:

Creators and operators use this skill to upload prepared videos and captions to WeChat Channels, schedule or batch-publish posts, check publication status, and reschedule pending posts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish at an unintended date or time when the requested schedule is not fully verified.

Mitigation: Verify the complete target date and time against the requested schedule and the platform form immediately before publishing; stop if they do not match.

Risk: Rescheduling can alter an existing post description.

Mitigation: Record and preserve the original description, then compare it with the edited post before confirming the reschedule.

Risk: The documented dry-run uploads the video and saves a real platform draft.

Mitigation: Treat dry-run as a real account change; review the uploaded draft, schedule, and originality declaration, and clean up the draft if it is not intended to remain.

Risk: Browser access is required for actions on the signed-in publishing account.

Mitigation: Keep execution isolation enabled, use a dedicated browser profile, and grant only narrowly scoped browser access.

## Reference(s):

- [WeChat Channels publishing page](https://channels.weixin.qq.com/platform/post/create)
- [WeChat Channels post list](https://channels.weixin.qq.com/platform/post/list)
- [Troubleshooting guide](artifact/references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [Shell commands, Text, JSON configuration]

**Output Format:** [Shell commands with text guidance and JSON episode configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can perform browser-based upload, draft creation, publishing, and rescheduling actions.]

## Skill Version(s):

1.2.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
