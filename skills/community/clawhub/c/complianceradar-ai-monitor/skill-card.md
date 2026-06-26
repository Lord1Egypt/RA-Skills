## Description: <br>
Monitor regulatory changes across SEC, FDA, FINRA, and GDPR with AI impact assessment. Use when the user needs compliance tracking, policy updates, audit trails, or automated regulatory notifications for financial/healthcare organizations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ncreighton](https://clawhub.ai/user/ncreighton) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Compliance, legal, operations, and engineering teams use this skill to monitor regulatory sources, assess business impact, draft policy updates, and route compliance action items to collaboration and audit systems. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Compliance alerts, impact assessments, policy updates, and audit evidence may be incomplete or unsuitable for regulated decisions. <br>
Mitigation: Treat all generated compliance materials as drafts and require review by qualified legal, compliance, privacy, or medical professionals before implementation. <br>
Risk: External services and storage integrations may receive regulatory assessments or internal business context. <br>
Mitigation: Use least-privilege API keys, a dedicated Slack webhook, and organization-approved destinations before sending data to OpenAI, Slack, Google Sheets, GitHub, Notion, Zapier, or other configured systems. <br>
Risk: Monitoring latency, API limits, English-language coverage, and jurisdiction scope can leave gaps in regulatory tracking. <br>
Mitigation: Subscribe to official agency alerts in parallel, review rate-limit behavior, and add manual or custom monitoring for non-English, state-level, or non-US/EU sources. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ncreighton/complianceradar-ai-monitor) <br>
- [SEC EDGAR](https://www.sec.gov/cgi-bin/browse-edgar) <br>
- [openFDA](https://open.fda.gov/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and text with configuration snippets, shell commands, compliance reports, policy drafts, alerts, and audit logs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires configured API keys, curl, jq, and optional integrations such as Slack and Google Sheets.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
