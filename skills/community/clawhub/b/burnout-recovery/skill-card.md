## Description:

Structured burnout recovery protocol based on clinical burnout dimensions. Use when someone is exhausted, cynical about work, feels ineffective, can't disconnect, or says they're burned out.

This skill is ready for commercial/non-commercial use.

## Publisher:

[howtousehumans](https://clawhub.ai/user/howtousehumans)

### License/Terms of Use:

MIT-0

## Use Case:

Individuals and supporting agents use this skill to assess burnout severity, choose staged recovery actions, set workplace boundaries, track energy patterns, and know when to seek professional or crisis support.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive burnout scores, workplace details, reflections, activity patterns, and job-exit decisions may be persisted across sessions or in local plaintext.

Mitigation: Require explicit opt-in before saving recovery data, use a private storage location, and provide clear ways to inspect and delete saved data.

Risk: The skill handles severe burnout and possible crisis signals, which can exceed the scope of self-guided recovery.

Mitigation: Keep guidance supportive rather than diagnostic, encourage professional care when symptoms persist or worsen, and preserve the skill's crisis-resource escalation for urgent situations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/howtousehumans/skills/burnout-recovery)
- [Gerber et al., Aerobic exercise training and burnout](https://doi.org/10.1186/1756-0500-6-78)
- [988 Suicide & Crisis Lifeline](https://988lifeline.org/)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance with assessment questions, checklists, boundary scripts, reminder suggestions, and recovery notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create calendar reminders and local recovery notes when the agent has calendar and filesystem tools.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
