## Description: <br>
Generates scheduled Douyin hot-list analysis reports by fetching TikHub top videos, using OpenClaw LLM analysis, writing Markdown and DOCX reports, and emailing configured recipients. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[link-1069](https://clawhub.ai/user/link-1069) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to automate recurring Douyin hot-list monitoring, generate structured video analysis reports, and deliver them by email. It is intended for configured environments with SMTP credentials, a TikHub token, and reviewed scheduling settings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recurring email automation may send reports to unintended recipients if defaults are left unchanged. <br>
Mitigation: Review and change all recipient settings before installation, and run a no-email test before enabling scheduled delivery. <br>
Risk: Cron setup creates recurring outbound activity and can continue running after initial testing. <br>
Mitigation: Inspect the generated crontab entry, confirm the schedule is intended, and remove or disable it when the report is no longer needed. <br>
Risk: SMTP credentials and API tokens are required for normal operation. <br>
Mitigation: Store credentials only in the intended environment or OpenClaw config, use limited-scope tokens where possible, and rotate any value that may have been exposed. <br>
Risk: Bundled downloader, transcription, MCP server, WebUI proxy, and Telegram artifacts broaden the capability surface beyond the daily report workflow. <br>
Mitigation: Review bundled dependencies before deployment and enable only the components needed for the planned workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/link-1069/douyin-analyse-batch) <br>
- [Deployment guide](references/DEPLOY.md) <br>
- [TikHub registration](https://user.tikhub.io) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, DOCX attachments, shell commands, and JSON status summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes reports under the configured Douyin analysis output directory and can send DOCX attachments by SMTP when credentials and recipients are configured.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
