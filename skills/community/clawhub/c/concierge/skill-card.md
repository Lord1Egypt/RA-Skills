## Description:

Find accommodation contact details and run AI-assisted booking calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arein](https://clawhub.ai/user/arein)

### License/Terms of Use:

MIT

## Use Case:

Travelers, assistants, and agents use this skill to find accommodation contact details from listing URLs and place goal-directed booking calls through configured telephony and AI providers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can place real phone calls through third-party telephony and AI providers, which may incur costs or contact unintended recipients.

Mitigation: Confirm the destination, call goal, user authorization, consent, disclosure obligations, and account balance before dialing.

Risk: The skill requires telephony, AI, and tunnel-provider credentials for full call functionality.

Mitigation: Use tightly scoped credentials, protect the local configuration file, avoid sharing logs, and rotate keys if exposure is suspected.

Risk: Call audio, transcripts, contact details, and booking context may be sent to third-party services during operation.

Mitigation: Limit use to intended accommodation workflows, minimize sensitive personal information, and confirm privacy and legal requirements before use.

Risk: Auto-managed local infrastructure and tunneling can expose a local call server if configured carelessly.

Mitigation: Prefer pinned, auditable package versions, restrict tunnel use to the active call workflow, and do not expose the local server directly.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/arein/skills/concierge)
- [README](artifact/README.md)
- [Skill Definition](artifact/SKILL.md)
- [Voice Call Setup Guide](artifact/CALL-SETUP.md)
- [Phone Call Skill](artifact/skills/phone-call/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands and optional JSON CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May initiate real phone calls and write local run logs when configured by the user.]

## Skill Version(s):

1.5.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
