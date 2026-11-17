## Description:

Retrieves aggregated annual trade totals, quarterly trade volume, and supplier and buyer counts for country-pair trade analysis using the UpKuaJing Open Platform API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[upkuajing](https://clawhub.ai/user/upkuajing)

### License/Terms of Use:

MIT-0

## Use Case:

External users, export teams, trade analysts, and market researchers use this skill to retrieve macro-level customs trade summaries by country pair and year. It supports market sizing, trade volume snapshots, supplier and buyer count review, and partner ecosystem analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API credentials may be exposed or persisted in `~/.upkuajing/.env`.

Mitigation: Use a secure environment mechanism for `UPKUAJING_API_KEY`, restrict permissions on any saved `.env` file, and avoid commands that print the file contents.

Risk: Paid API calls and top-up utilities can create charges or payment flows.

Mitigation: Tell the user when an operation may incur fees and wait for explicit confirmation before running query or billing scripts.

Risk: Diagnostic reporting and version checks can send data to UpKuaJing services.

Mitigation: Run error reporting only after user confirmation and disclose that version checks may contact UpKuaJing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/upkuajing/skills/customs-overview-summary)
- [UpKuaJing homepage](https://www.upkuajing.com)
- [UpKuaJing Open Platform](https://developer.upkuajing.com/)
- [UpKuaJing OpenAPI pricing](https://www.upkuajing.com/web/openapi/price.html)
- [Overview Summary API reference](references/customs-overview-summary-api.md)
- [Skill Error Report API reference](references/skill-error-report-api.md)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Natural-language guidance with optional shell commands and JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires UPKUAJING_API_KEY; paid API calls require explicit user confirmation before execution.]

## Skill Version(s):

1.0.1 (source: SKILL.md metadata and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
