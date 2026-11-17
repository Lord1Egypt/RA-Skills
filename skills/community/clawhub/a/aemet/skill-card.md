## Description:

Weather alerts and forecasts from AEMET OpenData for Spain.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pablomartinezcrespo](https://clawhub.ai/user/pablomartinezcrespo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to retrieve official AEMET weather alerts, daily forecasts, hourly forecasts, and municipality lookup results for locations in Spain.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles a local AEMET API key and makes HTTPS requests from a shell script.

Mitigation: Store the key only in ~/.openclaw/credentials/aemet-api-key.txt with restrictive permissions and review the script before installation.

Risk: Municipality search input is interpolated into jq expressions.

Mitigation: Avoid untrusted or generated municipality search strings until the jq interpolation issue is fixed.

Risk: Installation guidance includes sudo package installation commands.

Mitigation: Review dependency installation commands before running them on a local system.

## Reference(s):

- [ClawHub Aemet Skill](https://clawhub.ai/pablomartinezcrespo/skills/aemet)
- [AEMET OpenData](https://opendata.aemet.es/)
- [AEMET API Key Registration](https://opendata.aemet.es/centrodedescargas/altaUsuario)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration guidance]

**Output Format:** [Plain text terminal output with Markdown usage guidance and inline shell command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a local AEMET API key file and uses HTTPS requests with local caching.]

## Skill Version(s):

1.0.3 (source: server evidence release.version and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
