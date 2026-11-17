## Description:

Designs B2B cold-outbound sequence maps, reply-triage branches, warmup and send-throttle schedules, jurisdiction guardrails, and a SEND S-dimension deliverability read.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaron-he-zhu](https://clawhub.ai/user/aaron-he-zhu)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing and sales operations users use this skill to plan B2B cold-outbound programs before email copy is written or campaigns are sent. It produces the sequence structure, reply routing, warmup and throttle plan, compliance guardrails, and deliverability-focused SEND S read needed for downstream review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cold-outbound planning can lead to campaigns being sent without adequate consent, lawful-basis, or jurisdiction review.

Mitigation: Require accurate list-source, jurisdiction, and consent or lawful-basis records, and have jurisdiction-specific compliance reviewed by counsel before sending.

Risk: Local memory notes may contain list-source, jurisdiction, or deliverability details from a campaign plan.

Mitigation: Store only necessary planning summaries and handle them according to the workspace's data-retention and access rules.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/aaron-he-zhu/skills/cold-outbound-sequencer)
- [Project Homepage](https://github.com/aaron-he-zhu/aaron-marketing-skills)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Configuration instructions, Guidance]

**Output Format:** [Markdown with tables, schedules, guardrail notes, and handoff summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local memory notes when the user confirms saving results.]

## Skill Version(s):

19.0.0 (source: evidence.json release.version and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
