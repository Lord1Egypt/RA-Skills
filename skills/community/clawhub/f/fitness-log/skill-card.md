## Description:

Fitness Log tracks workouts, body weight, fitness statistics, plans, and exports for local personal use.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain1](https://clawhub.ai/user/bytesagain1)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents can use this skill to log local workout and weight data, review fitness summaries, generate simple plans, and export records without relying on external accounts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled script can turn workout or weight inputs into executable Python.

Mitigation: Review or patch the script before installation; pass values to Python through argv or environment variables and validate workout types, durations, counts, goals, formats, and weights.

Risk: The skill stores personal fitness and weight data under the user's home directory.

Mitigation: Set restrictive permissions on the local fitness directory and files before use.

Risk: Automatically forwarded or untrusted text could reach script parameters before input handling is patched.

Mitigation: Avoid using the skill with untrusted or automatically forwarded text until the script has been reviewed and fixed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bytesagain1/skills/fitness-log)
- [Fitness Log tips](artifact/tips.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and local command output descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local JSON and CSV fitness log files through the bundled shell script.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
