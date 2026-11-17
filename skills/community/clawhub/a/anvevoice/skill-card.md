## Description:

Add AI voice assistants to your website. Engage visitors with natural voice conversations, capture leads, automate support, and boost conversions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anveai](https://clawhub.ai/user/anveai)

### License/Terms of Use:

MIT

## Use Case:

Website operators, support teams, marketers, and developers use AnveVoice to create and manage voice assistants that answer visitor questions, capture leads, deploy website widgets, and analyze conversations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access sensitive visitor data, including conversation transcripts, recordings, profiles, leads, billing, and credentials when the API key permits it.

Mitigation: Use narrowly scoped AnveVoice API keys, avoid Full Access unless administration is required, and require confirmation before accessing sensitive account or visitor data.

Risk: Website voice widgets may collect microphone input, recordings, transcripts, browser metadata, and contact details from visitors.

Mitigation: Add privacy notices, consent flows, retention controls, and browser security controls before deploying the embed script.

Risk: The skill exposes destructive account actions, including deleting knowledge sources, deleting or pausing bots, and revoking credentials.

Mitigation: Require explicit user confirmation before destructive actions and use separate keys for development, staging, and production.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/anveai/skills/anvevoice)
- [AnveVoice Website](https://anvevoice.com)
- [AnveVoice Developer Portal](https://anvevoice.com/developer)
- [AnveVoice Help Documentation](https://anvevoice.com/help)
- [AnveVoice Dashboard](https://anvevoice.com/dashboard)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, API calls]

**Output Format:** [Markdown guidance with JSON tool-call arguments, shell commands, and embeddable HTML snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ANVEVOICE_API_KEY; responses may include bot configuration, analytics, leads, visitor profiles, recordings, billing, and credential data based on API key scope.]

## Skill Version(s):

1.0.3 (source: server release metadata); source frontmatter reports 1.0.0

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
