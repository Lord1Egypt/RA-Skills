## Description:

Builds audience segment plans from the user's own customer, CRM, or GA4 exports, including seed audiences, value-based lookalike seed lists, suppression segments, and a platform-neutral funnel-stage targeting map.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaron-he-zhu](https://clawhub.ai/user/aaron-he-zhu)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing teams and advertising operators use this skill to turn first-party customer, CRM, and GA4 exports into named paid-media audience buckets, lookalike seed definitions, suppression rules, and a reusable funnel-stage targeting map.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may require customer or analytics exports that contain sensitive customer data.

Mitigation: Provide only data allowed by policy, avoid raw customer PII unless necessary, and work from hashed or aggregate descriptions where possible.

Risk: Generated segment plans could misclassify customers or create unsuitable advertising audiences.

Mitigation: Review generated segment files and suppression rules before reuse or activation in ad platforms.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aaron-he-zhu/skills/audience-segment-builder)
- [Project homepage](https://github.com/aaron-he-zhu/aaron-marketing-skills)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown segment plan and handoff summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces named audience buckets, suppression rules, and a platform-neutral funnel-stage map; generated segment files should be reviewed before reuse.]

## Skill Version(s):

19.0.0 (source: server evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
