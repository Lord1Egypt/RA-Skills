## Description: <br>
AI-powered CNC machining quote system with risk detection, material optimization, and multi-channel integration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[timo2026](https://clawhub.ai/user/timo2026) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External manufacturers, machine shops, procurement teams, and developers use this skill to calculate CNC machining quotes, surface risk flags, generate optimization suggestions, and integrate quoting through bot, email, or API channels. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Quote requests and learning workflows may involve customer, pricing, or manufacturing data. <br>
Mitigation: Keep quote and customer data sanitized, limit access to stored data, and enable bot, email, or API channels only with appropriate authentication and data controls. <br>
Risk: AI-enabled behavior may require a DashScope API key. <br>
Mitigation: Use a dedicated API key, store it outside shared source files, rotate it if exposed, and scope it to the deployment where possible. <br>
Risk: Automated CNC quotes can be incorrect for unusual materials, process conflicts, or incomplete order details. <br>
Mitigation: Treat risk flags, confidence values, and optimization suggestions as decision support, and require human review before issuing binding quotes. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/timo2026/cnc-quote-skill) <br>
- [Installation Guide](examples/INSTALLATION.md) <br>
- [Use Cases](examples/USE_CASES.md) <br>
- [OpenClaw Documentation](https://docs.openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Python, JSON, and shell command examples; quote outputs may include numeric totals, confidence values, risk flags, and suggestions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require CNC order details, material and process data, optional historical quote data, and a DashScope API key for AI features.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, SKILL.md frontmatter, _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
