## Description: <br>
Contract Risk Review analyzes contract PDFs or pasted text, extracts key clauses with an OpenAI-compatible model, annotates risks across supported contract types, and returns a structured report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jeffersplind92](https://clawhub.ai/user/jeffersplind92) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, legal operations teams, and business users can use this skill to triage purchase, sales, service, labor, lease, and NDA contracts by extracting terms, highlighting risk notes, and preparing a Markdown report. It is intended as structured review support, not legal advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Contract text is sent to the configured AI provider, and the supplied api_key is sent to a YK-Global verification service before processing. <br>
Mitigation: Use only with contract data and credentials you are comfortable sharing with those services; avoid real OpenAI, Azure, Claude-proxy, or DeepSeek keys unless the publisher clarifies the verification flow or separates license tokens from model-provider credentials. <br>
Risk: AI-generated contract risk annotations may be incomplete, jurisdiction-specific, or misleading. <br>
Mitigation: Treat reports as triage material and have qualified reviewers verify findings before making legal, financial, or operational decisions. <br>
Risk: Optional Feishu notification output can expose summaries and risk points to a messaging workspace. <br>
Mitigation: Send notifications only to authorized recipients and use local report output when Feishu authorization or recipient scope is uncertain. <br>


## Reference(s): <br>
- [Contract Risk Review on ClawHub](https://clawhub.ai/jeffersplind92/contract-risk-review) <br>
- [Risk Checklist](references/risk-checklist.md) <br>
- [Changelog](references/changelog.md) <br>
- [YK-Global](https://yk-global.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, configuration, guidance] <br>
**Output Format:** [Markdown risk report with structured JSON results and optional Feishu card JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a user-supplied OpenAI-compatible API key; optional Feishu notification output depends on user authorization.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
