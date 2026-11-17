## Description:

监控ADC新申请、专利族、法律状态和竞争风险。

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

Patent intelligence and portfolio teams use this skill to generate ADC patent monitoring reports for a selected week, covering new WO applications, patent family context, legal status, and competitive risk signals. It is intended for Eureka Desktop workflows that collect structured PatSnap patent evidence before rendering an HTML report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The packaged skill references a renderer script that is not present in the artifact.

Mitigation: Obtain and inspect the expected build_adc_report.py renderer before relying on the skill for production patent reports.

Risk: Generated reports load third-party Chart.js from a CDN without integrity protection.

Mitigation: Use a bundled or SRI-protected Chart.js dependency, or review generated reports before opening them with network access.

Risk: The workflow depends on PatSnap MCP/API access and stores generated patent data locally.

Mitigation: Configure credentials only in the approved MCP server and handle local patent data according to the organization’s data retention and access policies.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuanzhian-patsnap/skills/adc-patent-monitoring)
- [ADC report HTML template](artifact/references/adc_report_template_v4.1.html)
- [Publisher profile](https://clawhub.ai/user/yuanzhian-patsnap)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown instructions and rendered HTML report artifacts generated from structured patent data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Eureka Desktop with PatSnap MCP/API access; generated patent data is written locally before report rendering.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
