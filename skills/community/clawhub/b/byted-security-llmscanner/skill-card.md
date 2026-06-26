## Description: <br>
Manages large model and agent security evaluation workflows, including asset creation, resource discovery, compliance and security task launch, and result analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[volcengine-skills](https://clawhub.ai/user/volcengine-skills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security evaluators use this skill in OpenClaw to register model or agent assets, discover available evaluation resources, launch compliance and security assessment tasks, and analyze returned results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles platform credentials, model API keys, bearer tokens, and evaluation result data. <br>
Mitigation: Review scripts before installation, avoid passing real API keys on the command line where possible, restrict permissions on config.ts and the data cache directory, and clear cached tokens or results when no longer needed. <br>
Risk: The security evidence identifies unsafe transport and local secret practices. <br>
Mitigation: Use the skill only in a controlled environment until TLS validation is fixed and the configured API endpoints are trusted. <br>
Risk: The skill can create or update evaluation assets and launch assessment tasks on an external platform. <br>
Mitigation: Confirm asset IDs, platform IDs, scenario IDs, and account permissions before running commands that mutate resources or start tasks. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/volcengine-skills/byted-security-llmscanner) <br>
- [Publisher profile](https://clawhub.ai/user/volcengine-skills) <br>
- [README](artifact/README.md) <br>
- [Skill instructions](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and console or JSON result summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call local TypeScript scripts that interact with an external security-evaluation platform and cache tokens or results locally.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
