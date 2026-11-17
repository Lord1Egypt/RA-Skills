## Description:

Query top N suppliers or buyers by trade volume for a country pair and year, with cursor-based pagination for ranked customs-trade analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[upkuajing](https://clawhub.ai/user/upkuajing)

### License/Terms of Use:

MIT-0

## Use Case:

Sourcing agents, export teams, and trade analysts use this skill to identify leading suppliers or buyers for global customs routes, evaluate market concentration, and page through ranked trading counterparties.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses an UpKuaJing API key and may create or read a plaintext key file under `~/.upkuajing`.

Mitigation: Check only whether the key is present, avoid printing `.env` contents, restrict local file permissions, and rotate the key if exposure is suspected.

Risk: Top-N queries are paid API calls.

Mitigation: Inform the user that the request incurs a fee and wait for explicit confirmation in a separate message before running a paid query.

Risk: Account, top-up, error-report, telemetry, and update-check flows send data to UpKuaJing services.

Mitigation: Use these flows only when needed, review payment or report details before submission, and omit sensitive request or response data from error reports where possible.

## Reference(s):

- [Customs Overview Top N API Reference](references/customs-overview-top-n-api.md)
- [Skill Error Report API Reference](references/skill-error-report-api.md)
- [UpKuaJing Skill Page](https://clawhub.ai/upkuajing/skills/customs-overview-top-n)
- [UpKuaJing Publisher Profile](https://clawhub.ai/user/upkuajing)
- [UpKuaJing Homepage](https://www.upkuajing.com)
- [UpKuaJing Open Platform](https://developer.upkuajing.com/)
- [UpKuaJing API Pricing](https://www.upkuajing.com/web/openapi/price.html)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, API calls, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python and UPKUAJING_API_KEY; paid API calls require explicit user confirmation before execution.]

## Skill Version(s):

1.0.1 (source: server evidence and SKILL.md metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
