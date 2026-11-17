## Description:

Track dog health, walks, training, routines, travel, and vet coordination with species-aware memory and emergency triage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

External users use this skill to manage day-to-day dog care, including health triage preparation, walks, routines, training notes, travel planning, vet logistics, shopping, and sitter handoffs. It supports real dog-care operations and local memory when the user approves persistent storage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent dog-care memory can store dog names, routines, health notes, vet logistics, and sitter details locally.

Mitigation: Ask for explicit approval before writing local files, keep records under ~/dog/, and support explicit or topic-specific activation preferences.

Risk: Dog health or behavior guidance could be mistaken for diagnosis or emergency veterinary care.

Mitigation: Use conservative triage language, escalate emergency red flags to veterinary care, and avoid medication dosing or definitive diagnosis from chat alone.

## Reference(s):

- [ClawHub Dog Skill Page](https://clawhub.ai/ivangdavila/skills/dog)
- [Dog Skill Homepage](https://clawic.com/skills/dog)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions]

**Output Format:** [Markdown with optional inline bash code blocks and local record templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local dog-care records under ~/dog/ only after user approval.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
