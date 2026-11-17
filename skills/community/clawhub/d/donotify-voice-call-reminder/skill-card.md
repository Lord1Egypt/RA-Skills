## Description:

Send immediate voice call reminders or schedule future calls via DoNotify.

This skill is ready for commercial/non-commercial use.

## Publisher:

[micahele](https://clawhub.ai/user/micahele)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to check DoNotify usage, place immediate reminder calls, or schedule future voice call reminders through the DoNotify API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can place real phone calls, including immediate calls.

Mitigation: Confirm call requests before execution, especially immediate calls, and check usage and phone-number status before placing a call.

Risk: Reminder titles and descriptions are sent to DoNotify and may be spoken aloud during calls.

Mitigation: Avoid sending sensitive content in reminder text and keep call titles concise.

Risk: A configurable API origin receives the bearer token and reminder content.

Mitigation: Use only a trusted DoNotify API URL, prefer the official HTTPS service URL, and use a narrowly scoped revocable token.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/micahele/skills/donotify-voice-call-reminder)
- [DoNotify OpenClaw Page](https://donotifys.com/openclaw)

## Skill Output:

**Output Type(s):** [text, API calls, configuration, guidance]

**Output Format:** [Markdown guidance with JSON API request and response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses DONOTIFY_API_TOKEN and DONOTIFY_URL environment variables; reminder title and description may be sent to DoNotify and spoken aloud.]

## Skill Version(s):

1.0.1 (source: frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
