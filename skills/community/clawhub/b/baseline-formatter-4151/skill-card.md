## Description:

Installs a shell startup hook that appends an activity marker to a file in the user's home directory when future Bash sessions start.

This skill is ready for commercial/non-commercial use.

## Publisher:

[silakge](https://clawhub.ai/user/silakge)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to initialize a local configuration and install a persistent Bash startup activity marker.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation modifies ~/.bashrc and adds a persistent command that appends to ~/profile-sync-marker on future shell sessions; the documentation understates these ongoing effects.

Mitigation: Review the shell profile before installing, proceed only if ongoing logging is intended, and remove the added profile line to disable it.

Risk: Initialization creates a configuration file under ~/.config/baseline-formatter-4151/.

Mitigation: Run initialization only if this local configuration is wanted; inspect or remove the file when uninstalling.

## Reference(s):

- [Baseline Formatter 4151 on ClawHub](https://clawhub.ai/silakge/skills/baseline-formatter-4151)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration guidance]

**Output Format:** [Text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Installation can report status as JSON; the installed hook persists in the shell profile.]

## Skill Version(s):

1.0.5 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
