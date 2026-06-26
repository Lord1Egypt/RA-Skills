## Description: <br>
EvoMap WorkBench v1.0.11 Mini provides AI decision, knowledge graph, predictive maintenance, adaptive learning, and decision-trace utilities for EvoMap workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yesimagine-oss](https://clawhub.ai/user/yesimagine-oss) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to evaluate EvoMap task context, build and search knowledge graphs, generate predictive maintenance recommendations, and record decision outcomes for automation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The server security summary reports under-disclosed local Feishu credential discovery and external message-sending paths, including a hardcoded fallback recipient. <br>
Mitigation: Install only in a sandbox or after source review; remove automatic credential discovery and hardcoded recipients, require explicit notification configuration, and document Feishu, Telegram, DingTalk, and EvoMap data flows before normal use. <br>
Risk: The release requires OAuth-token style credentials and may interact with external services when notification or API modules are used. <br>
Mitigation: Use least-privilege credentials, keep secrets out of shared workspaces, and run with explicit outbound-network and notification settings. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yesimagine-oss/evomap-workbench-min) <br>
- [Publisher profile](https://clawhub.ai/user/yesimagine-oss) <br>
- [EvoMap A2A validation endpoint](https://evomap.ai/a2a/validate) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python code examples, shell commands, and JSON or configuration details.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include external notification and API workflow guidance when explicitly configured.] <br>

## Skill Version(s): <br>
1.0.11 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
