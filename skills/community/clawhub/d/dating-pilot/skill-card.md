## Description:

Tinder dating assistant - swipe with filters (age/distance), conversation manager with smart replies, follow-up messaging. Use when user wants help managing their Tinder profile and conversations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[seraphetx](https://clawhub.ai/user/seraphetx)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to manage Tinder profile review, filtered swiping, chat monitoring, smart reply drafting, follow-up messaging, and profile photo diagnosis through the dating-pilot CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The npm package source is unavailable and the release installs an executable that can access a logged-in Tinder session.

Mitigation: Review the package before deployment, run it in a separate browser profile when possible, and avoid trusting it automatically.

Risk: The skill can swipe and send real messages from the user's Tinder account.

Mitigation: Start with small chat limits, review message quality before scaling, and avoid proactive messaging unless the user accepts that behavior.

Risk: The skill handles sensitive dating data and AI API credentials.

Mitigation: Use a dedicated low-privilege AI API key, avoid cleartext HTTP endpoints, and keep configuration local.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/seraphetx/skills/dating-pilot)
- [tinder-automation npm package](https://www.npmjs.com/package/tinder-automation)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Guidance]

**Output Format:** [JSON command output with brief Markdown summaries for heartbeat monitoring]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may operate a logged-in Tinder browser session, call a user-configured Anthropic-format AI endpoint, and store configuration locally.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
