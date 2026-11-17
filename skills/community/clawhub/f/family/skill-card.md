## Description:

Coordinate family schedules, household tasks, school logistics, care routines, and private-versus-shared memory with a structured family system.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

External users and household coordinators use this skill to plan shared schedules, chores, meals, school logistics, care routines, appointments, documents, and follow-ups while separating private notes from shared household operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may persist sensitive household, child, medical, pickup, medication, document, or incident details in local files.

Mitigation: Confirm each write before saving, keep entries minimal, avoid secrets and document numbers, and store ~/family/ somewhere protected from shared accounts, cloud sync, and broad backups.

Risk: Private member details could be promoted into shared household context more broadly than needed.

Mitigation: Default new details to private, promote only coordination-critical facts, and share the minimum information another household member needs to act.

Risk: Care, medical, legal, financial, or custodial topics could be over-treated as agent authority.

Mitigation: Use the skill for logistics and documentation only, identify the responsible adult, and escalate unclear health, legal, financial, or safety issues to a qualified person.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/family)
- [Skill homepage](https://clawic.com/skills/family)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown guidance, checklists, handoff notes, and local file templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or update local ~/family/ Markdown files after explicit user confirmation.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
