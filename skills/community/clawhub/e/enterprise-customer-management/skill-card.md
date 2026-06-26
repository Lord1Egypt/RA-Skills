## Description: <br>
Provides Excel-backed customer profile lookup, customer portrait analysis, risk alerts, and customer timelines for an enterprise service assistant. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[perrykono-debug](https://clawhub.ai/user/perrykono-debug) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Business service employees use this skill to query tenant records, summarize customer activity, identify payment or retention risks, and produce customer timelines from a local Excel ledger. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles real tenant, contact, contract, payment, service, and risk information from a local Excel ledger. <br>
Mitigation: Use only in an authorized business environment and restrict access to users who are permitted to view the underlying customer records. <br>
Risk: An embedded WeCom webhook and optional scheduled reports could send customer or risk data outside the local workspace. <br>
Mitigation: Remove and rotate the exposed webhook, keep local-only mode as the default, and require explicit approval before enabling outbound messages or scheduled pushes. <br>
Risk: Generated customer portraits, risk lists, or Tencent Docs exports may expose tenant, contact, payment, or risk details. <br>
Mitigation: Redact sensitive fields and review outputs before sharing them through WeCom, Tencent Docs, or other collaboration channels. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/perrykono-debug/enterprise-customer-management) <br>
- [Publisher profile](https://clawhub.ai/user/perrykono-debug) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown with structured customer summaries, risk lists, Python examples, and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read local customer Excel data and optionally produce scheduled risk reports, WeCom group messages, or Tencent Docs outputs when configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
