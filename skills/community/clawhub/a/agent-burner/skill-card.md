## Description:

Disposable email API for creating temporary inboxes, receiving messages, reading email contents, and extracting URLs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jsemldonado](https://clawhub.ai/user/jsemldonado)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use Agent Burner to create short-lived disposable email inboxes for low-sensitivity testing workflows, then list messages, fetch full content, and extract URLs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill steers agents to process full email contents and verification-style messages through a third-party no-auth disposable inbox service.

Mitigation: Use only for low-sensitivity disposable email testing; do not use for account recovery, high-value logins, MFA or OTP messages, passwords, personal data, confidential business mail, or regulated information.

Risk: Inbox keys are the only credential for accessing received messages.

Mitigation: Treat inbox keys like secrets, avoid exposing them in shared logs or transcripts, and delete inboxes when no longer needed.

Risk: Loading a mutable remote skill file can change agent behavior after review.

Mitigation: Prefer installing a pinned reviewed release version instead of loading a mutable remote skill file.

Risk: The API is rate limited to 10 inbox creations per minute per IP.

Mitigation: Design workflows to handle HTTP 429 responses with backoff or retry later.

## Reference(s):

- [Agent Burner Skill Page](https://clawhub.ai/jsemldonado/skills/agent-burner)
- [Agent Burner Homepage](https://agentburner.com)
- [Agent Burner Skill File](https://agentburner.com/skill.md)
- [Agent Burner API Base](https://api.agentburner.com)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance, API calls]

**Output Format:** [Markdown guidance with REST examples and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returned inbox keys authorize access to messages until expiration and should be treated as secrets.]

## Skill Version(s):

0.2.1 (source: server release metadata; artifact frontmatter lists 0.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
