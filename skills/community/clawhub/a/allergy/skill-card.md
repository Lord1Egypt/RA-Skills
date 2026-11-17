## Description:

Log allergens, track reactions, and chart symptom patterns over time. Use when identifying triggers, preparing reports, or setting reminders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckchzh](https://clawhub.ai/user/ckchzh)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to keep local notes about allergens, reactions, reminders, and symptom patterns for personal tracking and report preparation. It should be treated as a simple local logger rather than a medical or allergy-analysis tool.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Allergy and wellness notes may contain sensitive health-style information and are stored as plaintext local files.

Mitigation: Use only on a trusted local machine, review permissions on ~/.local/share/allergy, and avoid entering sensitive medical details unless plaintext storage is acceptable.

Risk: The export interface is described as available but the security summary flags it as misleading or broken.

Mitigation: Review export behavior before relying on it for backup or portability, and manually inspect local log files when preserving records.

Risk: The skill may be mistaken for medical or allergy-analysis software.

Mitigation: Use it only as a personal logging aid and rely on qualified medical guidance for diagnosis, treatment, or emergency decisions.

## Reference(s):

- [Allergy skill page](https://clawhub.ai/ckchzh/skills/allergy)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, shell commands, files, guidance]

**Output Format:** [Plain text command output and Markdown guidance; local log files with optional JSON, CSV, or TXT export behavior described by the artifact.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores entries locally under ~/.local/share/allergy.]

## Skill Version(s):

2.0.1 (source: server release evidence; artifact files declare 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
