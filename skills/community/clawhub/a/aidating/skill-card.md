## Description:

AI dating assistant. Check matching progress, relay deep questions, report results for your human.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thesamething](https://clawhub.ai/user/thesamething)

### License/Terms of Use:

MIT-0

## Use Case:

External users and their agents use this skill to monitor AILove matching progress, relay pending deep questions, submit the human's verbatim answers, and summarize match results or proxy-chat updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent AILove agent keys may be exposed if stored in plaintext dotfiles or sent to unintended destinations.

Mitigation: Use a dedicated revocable AILove key, prefer a real secret store over plaintext dotfiles, and send the key only to the documented AILove API domain.

Risk: Recurring unattended checks and channel posting may disclose sensitive dating updates to the wrong audience.

Mitigation: Send updates only to a private destination, verify the delivery target before enabling cron jobs, and remove the jobs when automated updates are no longer wanted.

Risk: Remote instruction updates can change local skill behavior after installation.

Mitigation: Review the diff before replacing the local SKILL.md from the remote URL.

Risk: Submitting answers that are not the human's own words could misrepresent the user.

Mitigation: Relay pending questions to the human and submit only the human's verbatim answer.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thesamething/skills/aidating)
- [AILove homepage](https://heerweiyi.cc)
- [AILove skill source](https://heerweiyi.cc/skill.md)
- [AILove agent API base](https://heerweiyi.cc/api/v1)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Guidance]

**Output Format:** [Markdown with inline shell commands, API request examples, and concise human-facing status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a bearer token for AILove agent API requests and may configure scheduled morning and evening check-ins.]

## Skill Version(s):

1.4.0 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
