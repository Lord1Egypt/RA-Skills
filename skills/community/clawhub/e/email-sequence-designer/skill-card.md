## Description:

Email Sequence Designer helps agents design lifecycle email automation flows with triggers, timing, branches, frequency governance, sunset paths, and a SEND N score.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaron-he-zhu](https://clawhub.ai/user/aaron-he-zhu)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing operators and lifecycle email teams use this skill to plan welcome, abandoned-cart, browse-abandon, post-purchase, light re-engagement, and cold-outbound sequences before copywriting or quality auditing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated lifecycle plans or broadcast requests could be approved without checking consent, suppression, or send readiness.

Mitigation: Review generated broadcast requests before live sends and keep consent and suppression checks in place.

Risk: Marketing-platform exports or connector workflows may contain untrusted or incomplete operational data.

Mitigation: Treat imported exports as input evidence only and confirm triggers, segments, cadence, and complaint signals before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/aaron-he-zhu/skills/email-sequence-designer)
- [Project Homepage](https://github.com/aaron-he-zhu/aaron-marketing-skills)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with structured flow maps, cadence plans, SEND N scoring notes, handoff summaries, and optional shell command previews]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write reusable handoff summaries to memory and propose hot-cache or open-loop updates when supported by the host agent.]

## Skill Version(s):

19.0.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
