## Description:

Generate private meeting briefings from Fulcra calendar data with optional CRM notes and web research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arc-claw-bot](https://clawhub.ai/user/arc-claw-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and external-facing teams use this skill to prepare for upcoming meetings using Fulcra calendar facts, optional CRM notes, and permitted public research. It is intended to produce concise private briefings and concrete follow-up questions while failing closed when evidence is too thin.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles private calendar, CRM, attendee, token, and location data.

Mitigation: Keep sensitive meeting details out of shared outputs and use synthetic examples for public documentation or tests.

Risk: The skill asks users to run an unpinned external Fulcra CLI.

Mitigation: Use only a vetted, pinned Fulcra CLI version from a trusted source and avoid running it in environments with unrelated secrets or broad file access.

Risk: Briefings can become misleading when meeting context is too thin.

Mitigation: Fail closed, return a short diagnostic, or say no reliable briefing can be generated instead of adding filler.

## Reference(s):

- [Fulcra Dynamics](https://fulcradynamics.com)
- [ClawHub Skill Page](https://clawhub.ai/arc-claw-bot/skills/fulcra-meeting-briefing)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with concise prose and optional inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Private meeting details are summarized only when supported by calendar, CRM, or permitted research evidence.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
