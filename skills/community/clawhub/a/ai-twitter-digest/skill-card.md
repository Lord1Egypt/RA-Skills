## Description:

Monitors curated AI/tech Twitter/X accounts, summarizes important daily posts with an LLM, and delivers a formatted digest to a configured chat channel.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fredhjc](https://clawhub.ai/user/fredhjc)

### License/Terms of Use:


## Use Case:

Developers, technical operators, and community managers use this skill to configure scheduled or one-shot AI Twitter/X digests and deliver summaries to Discord or another configured messaging channel.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup flow can copy existing API credentials into a plaintext local environment file.

Mitigation: Use dedicated low-scope API keys with spending limits, avoid copying credentials from existing OpenClaw auth where possible, and protect or remove scripts/.env after setup.

Risk: LLM-generated digests and links may be influenced by monitored tweets and then posted to messaging channels.

Mitigation: Treat generated digest content and links as untrusted, review high-impact outputs before redistribution, and configure only the exact delivery channel and target intended.

## Reference(s):

- [Default Monitored Accounts](references/accounts.md)
- [AISA API](https://aisa.one)
- [ClawHub Skill Page](https://clawhub.ai/fredhjc/skills/ai-twitter-digest)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown-formatted digest messages with setup and run commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a text summary and optional link-preview message for the configured delivery target, with deduplication state for previously seen tweets.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
