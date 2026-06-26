## Description: <br>
Monitor Victron Energy power systems through the Victron VRM API and generate daily reports with battery status, solar generation, inverter/AC status, active alarms, and structured exports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lkilpatrick](https://clawhub.ai/user/lkilpatrick) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External boat owners, RV users, off-grid power-system operators, and developers use this skill to configure daily Victron VRM monitoring, automate reports, and inspect current battery, solar, AC, alarm, and gateway status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles a Victron VRM API token and private power-system telemetry. <br>
Mitigation: Use a dedicated read-only VRM token, store it in an environment variable or secret manager, never commit it to source, and rotate it if exposed. <br>
Risk: Generated reports and scheduled-run logs may disclose private power-system status, installation details, or alarm data. <br>
Mitigation: Write outputs to a private configurable directory, restrict report and log permissions, and protect cron or scheduler logs. <br>
Risk: Automated monitoring depends on external API responses and unpinned dependencies. <br>
Mitigation: Pin dependencies before scheduled use, run the script in a controlled environment, and review generated reports before relying on them for operational decisions. <br>


## Reference(s): <br>
- [Victron Attribute Codes Reference](references/victron_attributes.md) <br>
- [Victron VRM API Quick Reference](references/vrm_api_guide.md) <br>
- [Victron VRM API Endpoints](references/vrm_endpoints.md) <br>
- [Victron VRM API Docs](https://vrm-api-docs.victronenergy.com/) <br>
- [Victron VRM Access Tokens](https://vrm.victronenergy.com/access-tokens) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell snippets; the bundled script emits JSON to stdout and writes an HTML report file.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runtime behavior depends on user-provided Victron VRM token, installation IDs, network access, and configured output path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and CHANGELOG, released 2026-03-09) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
