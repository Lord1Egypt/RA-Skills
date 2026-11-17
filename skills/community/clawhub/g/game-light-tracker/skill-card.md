## Description:

Track live NFL, NBA, NHL, or MLB games and automatically change Hue light colors based on which team is leading.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xadamsu](https://clawhub.ai/user/0xadamsu)

### License/Terms of Use:


## Use Case:

External users and smart-home operators use this skill to ask an agent to monitor live sports games and keep Hue lights synchronized with the leading team's configured color.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The tracker can control the configured Home Assistant light using credentials stored in a local configuration file.

Mitigation: Use a dedicated least-privileged Home Assistant token and restrict permissions on the configuration file.

Risk: The supervisor starts a background PowerShell process that can restart the tracker automatically.

Mitigation: Run the tracker visibly when possible, record process IDs, and stop only the recorded tracker and supervisor processes.

Risk: The documented broad force-kill command can terminate unrelated PowerShell sessions.

Mitigation: Avoid broad process matching; stop only known tracker and supervisor process IDs.

## Reference(s):

- [ESPN NFL Teams](https://www.espn.com/nfl/teams)
- [ESPN NBA Teams](https://www.espn.com/nba/teams)
- [ESPN NHL Teams](https://www.espn.com/nhl/teams)
- [ESPN MLB Teams](https://www.espn.com/mlb/teams)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline PowerShell commands and configuration steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include sport, team, light entity, RGB color, Home Assistant URL, and API token setup details.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
