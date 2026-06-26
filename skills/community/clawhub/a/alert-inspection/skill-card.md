## Description: <br>
When a user requests device health inspection, alert review, inspection report generation, or monitored-alert export to Excel, this skill uses Python to fetch monitoring data, generate a Markdown inspection report, and export a four-sheet Excel workbook. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Lerwee](https://clawhub.ai/user/Lerwee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Operations engineers and monitoring administrators use this skill to inspect Lerwee-monitored device health, review active alerts, and produce paired Markdown and Excel inspection deliverables. It supports full inspections, classification-filtered inspections, and reuse of existing host and problem JSON data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a monitoring API secret to access the Lerwee backend. <br>
Mitigation: Use a least-privilege API secret, store it in the configured environment file or environment variables, and rotate it if it is exposed. <br>
Risk: Generated Markdown, JSON, and Excel files may contain hostnames, IP addresses, alert details, and raw backend records. <br>
Mitigation: Treat generated inspection artifacts as sensitive operational data and store or share them only in approved locations. <br>
Risk: The skill depends on network access to the monitoring API for live inspections. <br>
Mitigation: Prefer HTTPS or a trusted internal network, and use the local JSON reuse mode when live API access is unavailable or inappropriate. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Lerwee/alert-inspection) <br>
- [Publisher Profile](https://clawhub.ai/user/Lerwee) <br>
- [Excel Export Template](artifact/references/export_excel_template.py) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files] <br>
**Output Format:** [Markdown report, normalized JSON files, and a four-sheet Excel workbook] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LWJK_API_URL and LWJK_API_SECRET for live API collection; can also reuse existing hosts and problems JSON files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
