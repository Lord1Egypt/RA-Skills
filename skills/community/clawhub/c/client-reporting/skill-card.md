## Description: <br>
Automated client reporting for agencies and freelancers using OpenClaw. Pull data from Google Analytics, Google Search Console, social media platforms, and custom sources to generate branded weekly/monthly reports. Auto-deliver via email or Slack. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[reighlan](https://clawhub.ai/user/reighlan) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Agencies and freelancers use this skill to set up client workspaces, pull analytics and search metrics, generate branded weekly or monthly reports, and deliver them through email or Slack. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Client configuration and service account credentials may expose sensitive analytics or delivery access if stored or shared carelessly. <br>
Mitigation: Keep client configs and service account keys out of source control, restrict file permissions, and review the configuration model before installation. <br>
Risk: Report delivery can send client data to unintended email recipients or Slack webhooks. <br>
Mitigation: Validate report recipients and Slack webhooks before enabling delivery. <br>
Risk: The scripts perform outbound network requests for metrics and delivery. <br>
Mitigation: Use the skill only where outbound domains and client names are tightly controlled, especially on shared infrastructure. <br>


## Reference(s): <br>
- [Google Analytics 4 API Setup](references/ga4-setup.md) <br>
- [Report Customization](references/report-customization.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/reighlan/client-reporting) <br>
- [Publisher Profile](https://clawhub.ai/user/reighlan) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with bash commands, JSON configuration examples, and generated report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can generate Markdown, HTML, and PDF-style client reports when configured with the required templates and conversion tooling.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
