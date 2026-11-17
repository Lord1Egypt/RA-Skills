## Description:

Helps agents diagnose arkcli profile and configuration precedence, manage update settings, and troubleshoot local configuration safely.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jasonstarlight](https://clawhub.ai/user/jasonstarlight)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to identify which profile, environment, API key, or base URL arkcli will use, and to manage local profiles and update settings. It guides users through configuration changes while accounting for commands that can write local settings or key data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence notes a concern about global arkcli installation beyond the skill's configuration purpose.

Mitigation: Review any global installation or replacement command before running it, and proceed only when that change is intended.

Risk: Profile show, list, and key-list commands may synchronize remote keys and write local key state.

Mitigation: Use these commands only when profile or key details are requested, and explain the possible local changes first.

Risk: arkcli config reset removes the local configuration files.

Mitigation: Confirm the reset's scope before running it; the skill notes that credential cleanup requires the separate arkcli auth logout flow.

Risk: The security evidence says four path-like references were unresolved, leaving the scan incomplete.

Mitigation: Review those references before installation when a fuller assessment is needed.

## Reference(s):

- [ClawHub arkcli-config release page](https://clawhub.ai/jasonstarlight/skills/arkcli-config)
- [arkcli-config profile guidance](artifact/references/arkcli-config-profile.md)
- [arkcli-config initialization guidance](artifact/references/arkcli-config-init.md)
- [arkcli-config evaluation cases](artifact/references/evals.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Some documented commands can change local configuration or key state; follow the described confirmation and side-effect safeguards.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact SKILL.md frontmatter reports 1.2.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
