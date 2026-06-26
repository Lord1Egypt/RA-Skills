## Description: <br>
Weather alerts and forecasts from AEMET OpenData for Spain <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pablomartinezcrespo](https://clawhub.ai/user/pablomartinezcrespo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to query official AEMET OpenData alerts, daily forecasts, hourly forecasts, and municipality lookups for Spain from an agent workflow. <br>

### Deployment Geography for Use: <br>
Spain <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores and reads a personal AEMET API key from the local filesystem. <br>
Mitigation: Keep the key file private, restrict file permissions, and do not commit it to repositories. <br>
Risk: The documented setup installs system command-line dependencies before use. <br>
Mitigation: Review the install commands and install dependencies only from trusted operating-system package sources. <br>
Risk: The package includes an extra test-skill.md file that is unrelated to the AEMET workflow. <br>
Mitigation: Treat it as packaging clutter and remove it in a future release to avoid confusion during review. <br>


## Reference(s): <br>
- [AEMET OpenData](https://opendata.aemet.es/) <br>
- [AEMET API key registration](https://opendata.aemet.es/centrodedescargas/altaUsuario) <br>
- [ClawHub skill page](https://clawhub.ai/pablomartinezcrespo/aemet) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown-oriented agent guidance with shell command examples and plain-text weather output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local AEMET API key and command-line dependencies such as curl, jq, and optionally xmllint and coreutils.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
