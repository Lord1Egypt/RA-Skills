## Description: <br>
Crypto Search Advisor analyzes cryptocurrency screenshots and search results to classify assets, flag market risks, and produce quick scans followed by deeper analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[haiyanzhuang5-cyber](https://clawhub.ai/user/haiyanzhuang5-cyber) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and analysts use this skill to interpret cryptocurrency exchange screenshots and public market information for observation, risk awareness, and independent decision support. It is not a trading terminal and should not be used to execute trades or replace professional financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can provide actionable cryptocurrency market analysis while presenting the output as informational. <br>
Mitigation: Treat outputs as observation support only, verify prices and risks independently, and do not connect the skill to automated trading or account operations. <br>
Risk: User screenshots may contain balances, account identifiers, wallet details, or other private financial information. <br>
Mitigation: Review and redact screenshots before upload, and avoid sharing any image that exposes private financial or account data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/haiyanzhuang5-cyber/crypto-search-advisor) <br>
- [README](README.md) <br>
- [OpenClaw integration guide](OPENCLAW_INTEGRATION.md) <br>
- [Output format specification](FORMAT.md) <br>
- [Core rules](RULES.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown and structured JSON, with optional CLI shell commands for local analysis workflows] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Two-stage response pattern: a quick scan first, followed by deeper analysis when available.] <br>

## Skill Version(s): <br>
2.5.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
