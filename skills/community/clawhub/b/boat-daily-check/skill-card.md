## Description:

Monitor Victron Energy power systems and generate daily reports with battery status, solar generation, inverter or AC status, active alarms, and hardware telemetry from the Victron VRM API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lkilpatrick](https://clawhub.ai/user/lkilpatrick)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers with Victron Energy power systems use this skill to configure and run daily monitoring for boats, RVs, off-grid homes, and similar installations. It helps collect battery, solar, inverter, alarm, and gateway status into human-readable reports and machine-readable exports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Victron API tokens and installation telemetry.

Mitigation: Use a dedicated read-only Victron token stored in an environment variable or secret store, and avoid placing real tokens in source files.

Risk: Generated reports can expose operational details about power systems and installation status.

Mitigation: Restrict report recipients, output directories, and retention for generated HTML, JSON, and CSV files.

Risk: The release security guidance identifies gaps in email delivery behavior, a pg_data bug, HTML escaping, and dependency pinning.

Mitigation: Review and fix those issues before relying on unattended daily monitoring or automated email distribution.

## Reference(s):

- [Victron VRM API Docs](https://vrm-api-docs.victronenergy.com/)
- [Victron VRM Access Tokens](https://vrm.victronenergy.com/access-tokens)
- [Victron Attribute Codes Reference](references/victron_attributes.md)
- [Victron VRM API Quick Reference](references/vrm_api_guide.md)
- [VRM Endpoints Used](references/vrm_endpoints.md)
- [Victron VRM API Reference Implementation](https://github.com/dirkjanfaber/victron-vrm-api)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Code, HTML, JSON, CSV, Guidance]

**Output Format:** [Markdown guidance with Python and shell examples; runtime outputs are HTML, JSON, and CSV files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Victron VRM API token and installation IDs; generated reports may contain sensitive power-system telemetry.]

## Skill Version(s):

1.0.0 (source: release metadata and changelog, released 2026-03-09)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
