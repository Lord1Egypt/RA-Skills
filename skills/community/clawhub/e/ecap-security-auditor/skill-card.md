## Description: <br>
Security audit framework for AI agent skills, MCP servers, and packages. Your LLM does the analysis; the skill provides structure, prompts, and a shared trust database. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[starbuck100](https://clawhub.ai/user/starbuck100) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to check skills, MCP servers, and npm or pip packages before installation, then produce structured audit findings, trust-score decisions, peer-review guidance, and registry upload commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Audit reports can upload information about local packages to an external registry. <br>
Mitigation: Use the skill mainly on public packages or code approved for external reporting, and review generated reports before running upload commands. <br>
Risk: Custom registry configuration can redirect registration or upload traffic. <br>
Mitigation: Keep ECAP_REGISTRY_URL unset unless the alternate registry is trusted and expected. <br>
Risk: Documentation includes live-looking bearer tokens or API examples. <br>
Mitigation: Treat any documented bearer token as exposed and rotate or remove it before relying on the skill. <br>
Risk: Automatic audits read target package files before producing findings. <br>
Mitigation: Do not run auto-audit on private repositories or sensitive source trees until data handling and upload behavior are approved. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/starbuck100/ecap-security-auditor) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>
- [Audit prompt](prompts/audit-prompt.md) <br>
- [Review prompt](prompts/review-prompt.md) <br>
- [Trust Registry](https://skillaudit-api.vercel.app) <br>
- [Trust Registry docs](https://skillaudit-api.vercel.app/docs) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON report examples and shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read local package files and may upload audit reports to an external registry when the user runs the provided scripts.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
