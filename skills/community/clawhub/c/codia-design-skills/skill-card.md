## Description: <br>
Codia Design Skills helps agents create, edit, convert, inspect, and manage visual assets through the authenticated Codia Design CLI and Codia Open API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[codia-ai](https://clawhub.ai/user/codia-ai) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, designers, and marketing teams use this skill pack through local agents to generate and edit images, convert screenshots and PDFs into editable design data or PPTX, vectorize assets, and manage Codia account usage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Authenticated Codia cloud workflows may upload local images, screenshots, PDFs, or documents to Codia Open API. <br>
Mitigation: Review each command and source path before execution, and only submit files the user intended to process. <br>
Risk: The skill can inspect or change Codia account settings, including automatic recharge. <br>
Mitigation: Require explicit user confirmation before any auto-recharge or billing-related update. <br>
Risk: Credentials may be exposed if API keys or local auth config are printed. <br>
Mitigation: Use the CLI auth flow or environment variables, redact keys in logs, and never print ~/.codia/design-skills/config.json. <br>


## Reference(s): <br>
- [Codia Open API Documentation](https://codia.ai/api-reference#description/introduction) <br>
- [ClawHub Skill Page](https://clawhub.ai/codia-ai/codia-design-skills) <br>
- [README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown summaries with shell commands, local file paths, URLs, JSON snippets, and downloaded asset references.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Codia task IDs, credit or usage summaries, and local output paths; excludes API keys and raw auth config.] <br>

## Skill Version(s): <br>
0.1.3 (source: SKILL.md frontmatter and ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
