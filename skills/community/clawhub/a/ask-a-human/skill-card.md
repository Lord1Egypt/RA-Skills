## Description:

Request judgment from random humans when uncertain about subjective decisions, including crowdsourced opinions on tone, style, ethics, and reality checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[manuelkiessling](https://clawhub.ai/user/manuelkiessling)

### License/Terms of Use:

MIT

## Use Case:

OpenClaw users and agent developers use this skill to ask a pool of human respondents for subjective judgment on wording, tone, ethics, appropriateness, reality checks, and similar decisions when asynchronous feedback is acceptable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts are sent to an external service and may be shown to random human respondents.

Mitigation: Require explicit user approval, preview the exact outbound prompt, and remove secrets, personal data, customer details, proprietary code, non-public security findings, and confidential business context before submission.

Risk: Human responses can be delayed, incomplete, or absent.

Mitigation: Use polling with timeouts, keep a fallback plan, and proceed with the agent's own judgment when responses do not arrive in time.

Risk: Returned text is untrusted opinion and may be unsuitable as instructions or lasting preference data.

Mitigation: Treat responses as advisory only and avoid storing or acting on them as persistent user preferences unless the owner explicitly confirms them.

## Reference(s):

- [Ask-a-Human Web App](https://app.ask-a-human.com)
- [Ask-a-Human API Documentation](https://api.ask-a-human.com/docs)
- [OpenClaw Documentation](https://docs.clawd.bot)
- [ClawHub Skill Page](https://clawhub.ai/manuelkiessling/skills/ask-a-human)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Text, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ASK_A_HUMAN_AGENT_ID and asynchronous polling for responses.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
