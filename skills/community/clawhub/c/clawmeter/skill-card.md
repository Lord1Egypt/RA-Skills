## Description: <br>
Clawmeter tracks OpenClaw API usage and spending with a self-hosted dashboard, cost breakdowns, and configurable budget alerts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Someone0070](https://clawhub.ai/user/Someone0070) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, teams, and OpenClaw users use Clawmeter to monitor session-log usage, estimate API spend by model or session, and receive budget threshold alerts before costs exceed planned limits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local Clawmeter API is unauthenticated and may be exposed more broadly than intended. <br>
Mitigation: Bind the service explicitly to localhost, avoid exposing port 3377, or place it behind authentication before broader network use. <br>
Risk: The service indexes OpenClaw usage metadata and stores it in a local SQLite database. <br>
Mitigation: Protect the SQLite database path and restrict filesystem permissions to the intended user or service account. <br>
Risk: Optional Telegram and SMTP alerts require credentials in local configuration. <br>
Mitigation: Use dedicated alerting credentials, keep the .env file private, and rotate credentials if the configuration is shared or exposed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Someone0070/clawmeter) <br>
- [README](artifact/README.md) <br>
- [Architecture](artifact/docs/ARCHITECTURE.md) <br>
- [Quick Start](artifact/docs/QUICKSTART.md) <br>
- [Changelog](artifact/CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, configuration examples, and local API response summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces cost-tracking guidance for an agent and points to a local dashboard/API for live usage data.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata; artifact package metadata and changelog report 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
