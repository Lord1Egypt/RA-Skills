## Description:

Generate a personalized, breed-and-age-aware dog training program with short daily exercises, week-by-week progression, breed drive profiles, progress tracking, and referral screening for higher-risk behavior cases.

This skill is ready for commercial/non-commercial use.

## Publisher:

[voronindenis5](https://clawhub.ai/user/voronindenis5)

### License/Terms of Use:

MIT

## Use Case:

External users and agents helping with pet-care questions use this skill to generate breed-aware, force-free dog training plans, breed insight, session logging, and follow-up guidance. It is intended for common obedience, puppy, socialization, and mild behavior issues, with referral guidance for aggression, bite history, severe anxiety, or deep fear.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Training notes entered through the log feature are saved locally in the skill's scripts directory.

Mitigation: Avoid recording sensitive household details in progress notes and review or remove scripts/.trainlog.json when local logs are no longer needed.

Risk: Aggression, bite history, severe separation anxiety, or deep fear can require professional assessment rather than a do-it-yourself training plan.

Mitigation: Use the skill's referral warnings and seek a certified behaviorist or veterinary behaviorist for those cases.

## Reference(s):

- [Breed Drive Profiles](references/breed-drives.md)
- [Behavior Protocols](references/protocols.md)
- [ClawHub skill page](https://clawhub.ai/voronindenis5/skills/dog-train-o-matic)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown and plain text CLI output with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or read a local progress log at scripts/.trainlog.json when the log or today commands are used.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
