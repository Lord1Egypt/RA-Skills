## Description: <br>
Daily emails listing recent A-share IPOs and selected stocks priced under 20 yuan, including key trading details. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[batype](https://clawhub.ai/user/batype) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to fetch A-share IPO and low-price stock data, format the results, and send the daily summary by email. The generated market data is for reference and does not constitute investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles SMTP credentials and includes a hardcoded recipient address. <br>
Mitigation: Review and change the recipient, replace any exposed SMTP password, and use a dedicated app password or low-privilege SMTP account before running it. <br>
Risk: Scheduled outbound email may send market summaries automatically. <br>
Mitigation: Confirm that scheduled email is acceptable for the deployment context and review any cron or OpenClaw schedule before enabling it. <br>
Risk: Credential exports in shell startup files can broaden secret exposure. <br>
Mitigation: Avoid storing SMTP secrets in shell startup files; prefer a local environment file or secret manager with restricted access. <br>
Risk: The DNS repair path can modify /etc/hosts. <br>
Mitigation: Do not run fix-hosts.sh unless the operator understands the host-file changes and can undo them. <br>
Risk: The SMTP TLS configuration may disable certificate validation. <br>
Mitigation: Remove rejectUnauthorized:false before relying on SMTP credentials in regular use. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/batype/astock-daily) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [README](artifact/README.md) <br>
- [Configuration guide](artifact/CONFIG.md) <br>
- [SMTP troubleshooting](artifact/README-SMTP.md) <br>
- [DNS fix guide](artifact/DNS-FIX.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown guidance with shell command snippets; generated HTML email and JSON data files when executed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May send scheduled outbound email and write daily data or email fallback files.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata, package.json, README changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
