## Description:

Generate elevator pitch for conference posters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[googolme](https://clawhub.ai/user/googolme)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, students, and conference presenters use this skill to draft short practice scripts for academic poster sessions at 30, 60, or 180 seconds.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs a local Python script.

Mitigation: Review the command and run it in a sandboxed workspace before relying on generated pitch text.

Risk: The documentation mentions saved output files, but the inspected implementation only prints pitch text.

Mitigation: Do not rely on file persistence unless the implementation is updated and rescanned.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/googolme/skills/conference-poster-pitch)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text pitch script with a short heading]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports 30, 60, and 180 second pitch lengths.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
