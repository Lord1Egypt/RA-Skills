## Description:

Twitter/X research, monitoring, watchlists, and OAuth-approved posting through AIsa for agents that need relay-based reads and OAuth-gated text or media posting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[baofeng-tech](https://clawhub.ai/user/baofeng-tech)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to research Twitter/X accounts, timelines, mentions, trends, lists, communities, and Spaces, and to draft or publish approved posts through the AIsa relay. It is intended for workflows that can use AISA_API_KEY and relay-based access instead of password, cookie, or browser credential extraction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The OAuth posting client can print the raw AISA_API_KEY in command output, which can expose credentials in logs or agent transcripts.

Mitigation: Do not run the OAuth posting client with a real key until outputs mask or remove the key; rotate the key if it has already appeared in logs or transcripts.

Risk: Relay-based Twitter/X requests send API requests, post content, selected media files, and AISA_API_KEY to the AIsa service.

Mitigation: Use this skill only when the user trusts the AIsa relay for those requests and files, and keep OAuth approval explicit before any external posting.

Risk: External posts can be misreported if the agent assumes success before the relay confirms publication.

Mitigation: Report a post as published only after the API returns a successful publish result, tweet link, or tweet ID.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/baofeng-tech/skills/aisa-twitter-api-aisa)
- [AIsa homepage](https://aisa.one)
- [AIsa API relay](https://api.aisa.one)
- [AIsa Twitter OAuth posting guide](references/post_twitter.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON command outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3, AISA_API_KEY, internet access to api.aisa.one, and explicit OAuth approval before posting.]

## Skill Version(s):

1.0.6 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
