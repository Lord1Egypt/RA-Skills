## Description:

Defense Rehearsal helps users prepare for, rehearse, and debrief academic defenses by generating mock committee questions, scanning cited-literature weak spots, and reviewing Tencent Meeting transcripts or summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[j-levee](https://clawhub.ai/user/j-levee)

### License/Terms of Use:

MIT-0

## Use Case:

External academic users use this skill to rehearse proposal, mid-term, or graduation defenses. It creates role-based committee questions, identifies references the user may not understand well enough to defend, and turns authorized Tencent Meeting records into delivery feedback and a debrief report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mock defenses and meeting transcripts may contain sensitive academic work, personal speech, or participant information.

Mitigation: Share only materials appropriate for the services involved, obtain consent from recorded participants, and confirm authorization before accessing Tencent Meeting data.

Risk: The skill records local method-level usage tags by default, which some users may not want retained.

Mitigation: Tell the agent '别记了' to disable local method-tag recording.

Risk: Generated committee questions and literature weak-spot analysis may miss issues that a human advisor or committee member would catch.

Mitigation: Use the output as rehearsal support and review it alongside supervisor, peer, or committee feedback before relying on it for a real defense.

## Reference(s):

- [Capability Coverage](references/coverage.md)
- [ClawHub Skill Page](https://clawhub.ai/j-levee/skills/defense-rehearsal)

## Skill Output:

**Output Type(s):** [guidance, markdown, text]

**Output Format:** [Markdown or plain text rehearsal plans, question lists, weak-spot summaries, and debrief reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May depend on user-provided defense materials, cited references, and authorized Tencent Meeting transcripts or summaries.]

## Skill Version(s):

2.0.1 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
