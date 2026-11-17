## Description:

Converts currency amounts in real time using Frankfurter/ECB reference rates, with support for major currencies, rate listing, and amount conversion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tonyhuya](https://clawhub.ai/user/tonyhuya)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to query current foreign exchange rates, convert amounts between major currencies, and list supported currency pairs from the command line.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts the Frankfurter/ECB exchange-rate API over the network and is unsuitable for strict offline or no-network environments.

Mitigation: Use it only where outbound HTTPS access to Frankfurter is permitted, or adapt it to an approved internal exchange-rate source.

Risk: Exchange-rate data is external reference data and may not satisfy regulated trading, accounting, or audit requirements.

Mitigation: Review the returned data date and validate rates against the required authoritative source before business-critical use.

Risk: The bundled usage text and command output are primarily Chinese, which can limit usability for English-only audiences.

Mitigation: Localize the help text and user-facing output before deployment to audiences that require English documentation.

## Reference(s):

- [Frankfurter API](https://www.frankfurter.app/)
- [Frankfurter latest rates endpoint](https://api.frankfurter.app/latest)
- [ClawHub skill page](https://clawhub.ai/tonyhuya/skills/fx-converter)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text command-line output with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, python3, and outbound HTTPS access to Frankfurter/ECB exchange-rate data.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
