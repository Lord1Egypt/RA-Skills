## Description:

Mental Models helps agents analyze genuine judgment calls through a lattice of Munger-style meta-lenses and twenty disciplinary mental models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[romanluoman00007](https://clawhub.ai/user/romanluoman00007)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to help an agent surface framing shifts, risks, incentives, and tensions when evaluating personal, product, investment, or strategy decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may maintain cross-session notes about reasoning, blind spots, risk profile, or decision context.

Mitigation: Review profile behavior before installation and require explicit approval before storing or updating personal decision-context notes.

Risk: Automatic personalization can silently mutate a long-term user profile.

Mitigation: Keep the profile file inspectable, limit stored observations to necessary context, and disable automatic profile updates when persistent personalization is not desired.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/romanluoman00007/skills/botlearn-mental-models)
- [SKILL.md](artifact/SKILL.md)
- [User profile template](artifact/assets/user-profile-template.md)
- [Mental model reference files](artifact/models/)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with structured latticework analysis and occasional shell setup commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May personalize analysis from a local profile and record repeated learning patterns when the lattice is used.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
