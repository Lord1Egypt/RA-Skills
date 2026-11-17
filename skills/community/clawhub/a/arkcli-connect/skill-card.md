## Description:

arkcli +connect installs ArkCLI's embedded AI skills into detected local AI agents, and can list supported agents or uninstall managed skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jasonstarlight](https://clawhub.ai/user/jasonstarlight)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and local AI agent users use this skill to install ArkCLI's embedded skills into detected agent directories, inspect supported agents, or remove managed skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Default synchronization may remove installed skills and change request routing.

Mitigation: Review the affected skills and routing before installing; use --path to limit installation to a specific skills directory when appropriate.

Risk: The supplied artifact references a shared rules file that is not included, leaving some reference coverage incomplete.

Mitigation: Verify the shared rules file and review its guidance before relying on the skill's full behavior description.

## Reference(s):

- [ArkCLI Connect detailed reference](references/arkcli-connect.md)
- [ArkCLI Connect evaluation cases](references/evals.md)
- [ClawHub skill release](https://clawhub.ai/jasonstarlight/skills/arkcli-connect)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands]

**Output Format:** [Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands and routing guidance for arkcli +connect operations.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
