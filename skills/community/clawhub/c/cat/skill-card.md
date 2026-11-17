## Description:

Track cat health, litter, routines, behavior, travel, and vet coordination with species-aware memory and emergency triage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to manage real-world cat care, including health triage, litter and behavior tracking, routines, travel preparation, records, and vet coordination.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may store cat-care records locally under ~/cat/ if memory is approved.

Mitigation: Install only if local cat-care storage is acceptable, avoid highly sensitive documents or unnecessary contact details, and keep memory limited to durable care facts.

Risk: Unsafe folder names could create confusing or path-like local record locations.

Mitigation: Use simple cat folder names without slashes, dot-dot sequences, or path-like characters.

Risk: Cat-care guidance could be mistaken for veterinary diagnosis or emergency care.

Mitigation: Use the skill's emergency triage rules, do not treat it as a diagnosis source, and seek veterinary care when red flags are active.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/skills/cat)
- [Skill Homepage](https://clawic.com/skills/cat)
- [Cat Triage](artifact/triage.md)
- [Memory Template](artifact/memory-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with optional shell command blocks and local record templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose local files under ~/cat/ only after user approval.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
