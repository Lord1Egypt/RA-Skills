## Description: <br>
Guide for developing AstrBot plugins that match the AstrBot main repo, pass astr-plugin-reviewer checks, and cover commands, filters, hooks, LLM integrations, and agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[camera-2018](https://clawhub.ai/user/camera-2018) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to create, update, and review AstrBot plugins that follow AstrBot APIs, marketplace metadata expectations, and astr-plugin-reviewer checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated AstrBot plugins may introduce dependency, network, API key, proactive messaging, LLM, or platform-access risks. <br>
Mitigation: Review the resulting plugin's dependencies, network calls, API key handling, proactive messaging, LLM use, and platform access before running or publishing it. <br>
Risk: Plugin guidance can be misapplied if generated code is not checked against AstrBot reviewer requirements. <br>
Mitigation: Run the final plugin through the reviewer checklist and confirm metadata, async I/O, hook signatures, logging, and persistence choices before release. <br>


## Reference(s): <br>
- [AstrBot Plugin Development](SKILL.md) <br>
- [AstrBot Plugin Project Structure](references/project-structure.md) <br>
- [astr-plugin-reviewer Checklist](references/reviewer-checklist.md) <br>
- [AstrBot Core API Reference](references/core-api.md) <br>
- [AstrBot Advanced Features](references/advanced-features.md) <br>
- [AstrBot Message Components](references/message-components.md) <br>
- [AstrBot Reviewer-Friendly Patterns](references/patterns.md) <br>
- [AstrBot Project](https://github.com/AstrBotDevs/AstrBot) <br>
- [AstrBot Plugin Marketplace](https://plugins.astrbot.app) <br>
- [ClawHub Skill Page](https://clawhub.ai/camera-2018/astrbot-plugin-dev-skill) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with Python, YAML, JSON, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
