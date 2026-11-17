## Description:

Build practical beauty routines with skincare basics, makeup strategy, and hair care plans tailored to skin type, budget, and schedule.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to build practical skincare, makeup, haircare, and grooming routines adapted to skin and hair profile, budget, schedule, and event context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may retain beauty preferences and routine context locally under ~/beauty when the user approves memory.

Mitigation: Ask for explicit confirmation before writing memory, avoid saving medical diagnoses or sensitive identifiers, and review or delete ~/beauty/memory.md when retained context is no longer wanted.

Risk: Beauty recommendations can be unsafe when treated as medical advice or when several active products are changed at once.

Mitigation: Use patch tests, introduce one new variable at a time, stop on burning, swelling, or persistent redness, and recommend licensed medical care for persistent, painful, scarring, or severe reactions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/skills/beauty)
- [Beauty Skill Homepage](https://clawic.com/skills/beauty)
- [Setup](setup.md)
- [Safety and Hygiene Guardrails](safety.md)
- [Memory Template](memory-template.md)
- [Universal Beauty Frameworks](frameworks.md)
- [Routine Templates](routines.md)
- [Product Selection Rules](products.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with optional inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Instruction-only output; optional local memory is used only with explicit user approval.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
