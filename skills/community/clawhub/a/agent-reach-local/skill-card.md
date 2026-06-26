## Description: <br>
Agent Reach Local gives an AI agent command guidance for searching, reading, configuring, and interacting with web, social, video, code, RSS, and article platforms. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[larry-at](https://clawhub.ai/user/larry-at) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to route online research, URL reading, platform search, channel setup, and supported account interactions through existing command-line tools and platform connectors. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may require social-platform cookies or authenticated browser state. <br>
Mitigation: Use a dedicated account or browser profile, avoid storing raw cookies where possible, and review account access before installation. <br>
Risk: The skill includes workflows that can post, comment, publish, or otherwise act through live accounts. <br>
Mitigation: Require explicit user confirmation before any post, comment, publish, or other account-changing action. <br>
Risk: The skill describes an anti-bot bypass workflow for reading some content. <br>
Mitigation: Do not use anti-bot bypass steps on services where they violate terms, account rules, or organizational policy. <br>


## Reference(s): <br>
- [Agent Reach homepage](https://github.com/Panniantong/Agent-Reach) <br>
- [Agent Reach install guide](https://raw.githubusercontent.com/Panniantong/agent-reach/main/docs/install.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, Python snippets, and tool-call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce commands that call external services and account-authenticated platform tools.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
