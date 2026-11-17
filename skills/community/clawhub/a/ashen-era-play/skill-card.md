## Description:

Ashen Era Playtest launches the appropriate bundled Ashen Era CLI build, plays one real run, and produces a first-person post-run report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ssochi](https://clawhub.ai/user/ssochi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to have an agent launch Ashen Era, complete a genuine CLI play session, and write a concrete first-person report of the run.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill launches a local game CLI through a shell script.

Mitigation: Install only when comfortable executing the packaged CLI and review the package before running it.

Risk: The inspected package is missing the referenced release archives and may fail to run unless those assets are supplied separately.

Mitigation: Confirm the release archives are present and trusted before execution.

## Reference(s):

- [Ashen Era Playtest on ClawHub](https://clawhub.ai/ssochi/skills/ashen-era-play)
- [Publisher profile: ssochi](https://clawhub.ai/user/ssochi)
- [CLI Surface](references/cli-surface.md)
- [Report Contract](references/report-contract.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown narrative report with launch command details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes executable target, command, class, seed, locale, final result, important actions, key choices, turning points, and retrospective.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
