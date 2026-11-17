## Description:

Your 24/7 AI front desk. Polly answers incoming calls, filters spam, takes messages, and routes important calls so you never miss what matters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hi-yox](https://clawhub.ai/user/hi-yox)

### License/Terms of Use:

MIT-0

## Use Case:

External users, small business owners, freelancers, and developers use this skill to activate a PollyReach phone number, place outbound calls, answer inbound calls, retrieve call summaries, and customize receptionist behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends call tasks, prompts, phone numbers, recordings, and transcripts to PollyReach.

Mitigation: Use explicit user confirmation before placing calls, enabling polling, sharing the assigned number, or submitting sensitive call content.

Risk: The skill stores a persistent local bearer token for the PollyReach API.

Mitigation: Store the token only in the configured local credentials file, restrict file access where possible, and rotate or remove the token if the device or workspace is shared.

Risk: Calls may be recorded or transcribed, creating privacy and consent obligations for third parties.

Mitigation: Review applicable consent and privacy requirements before recording, transcribing, or publicly using the assigned receptionist number.

Risk: Polling and outbound call actions can trigger real-world communications and credit consumption.

Mitigation: Confirm polling cadence and outbound call details with the user, monitor balance, and stop or adjust polling when the service is no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hi-yox/skills/ai-receptionist-skills)
- [PollyReach homepage](https://pollyreach.ai)
- [PollyReach agent dashboard](https://agent.pollyreach.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with shell command invocations and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses curl-based helper scripts to register, activate, send call tasks, poll results, check balance, retrieve inbound summaries, and update prompts.]

## Skill Version(s):

1.0.0 (source: frontmatter and release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
