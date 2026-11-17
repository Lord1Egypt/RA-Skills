## Description:

Consent Registry records and queries pseudonymous opt-in, lawful-basis, suppression, restore, and erasure evidence through an append-only consent stream.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaron-he-zhu](https://clawhub.ai/user/aaron-he-zhu)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing operations and compliance teams use this skill to record and query pseudonymous consent, lawful-basis, suppression, restore, and erasure events. It helps agents keep suppression decisions current without storing raw contact PII or declaring lists safe to send.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The registry affects persistent consent and suppression records when used in a live environment.

Mitigation: Install only where the agent is intended to maintain consent or suppression state, and confirm the host runtime and registry script are trusted before mutation.

Risk: Consent or suppression records may be incomplete if required proof, authorization, timestamp, or source fields are missing.

Mitigation: Return the documented handoff or missing-field response, and avoid claiming a mutation occurred until the host runtime appends and verifies the event.

Risk: Raw contact PII in consent records would increase privacy exposure.

Mitigation: Use only pseudonymous subject IDs, opaque proof references, and subject-free reason codes.

Risk: Cached projections can drift from authoritative consent state.

Mitigation: Replay the consent event stream and use the live suppression query after mutations or send-eligibility checks.

## Reference(s):

- [Consent Registry on ClawHub](https://clawhub.ai/aaron-he-zhu/skills/consent-registry)
- [Project homepage](https://github.com/aaron-he-zhu/aaron-marketing-skills)
- [Distribution manifest](artifact/distribution-manifest.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown responses with handoff details and shell command invocations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses pseudonymous subject IDs and minimum proof references; raw contact PII should not be included.]

## Skill Version(s):

19.0.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
