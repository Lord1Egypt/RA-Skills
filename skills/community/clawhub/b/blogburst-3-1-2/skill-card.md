## Description:

BlogBurst is an AI marketing agent that generates and repurposes content, manages social posting and engagement, runs SEO and GEO audits, tracks competitors, and scans communities for marketing opportunities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xspeter](https://clawhub.ai/user/0xspeter)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to connect an OpenClaw assistant to BlogBurst for content generation, content repurposing, social media automation, analytics, and marketing audits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup flow can expose the BlogBurst API key through command output, shell history, profile files, or logs.

Mitigation: Use a secret manager or a temporary environment variable, avoid printing the key, and rotate any key that has already appeared in output or logs.

Risk: The skill can enable public social-media actions such as posting, replying, liking, following, and running auto-pilot automation.

Mitigation: Connect only accounts the user is comfortable letting BlogBurst manage, and require previews or explicit confirmation before enabling automation or public engagement.

Risk: Prompts, draft content, account state, analytics, and marketing data may be sent to the BlogBurst API.

Mitigation: Avoid sending sensitive or confidential marketing material unless the user has approved the third-party data flow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/0xspeter/skills/blogburst-3-1-2)
- [BlogBurst website](https://blogburst.ai)
- [BlogBurst API docs](https://api.blogburst.ai/docs)
- [BlogBurst API keys](https://blogburst.ai/dashboard/api-keys)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, shell commands, configuration, guidance]

**Output Format:** [Markdown and text responses with curl commands and JSON API payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires BLOGBURST_API_KEY and sends user marketing requests to the BlogBurst API.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
