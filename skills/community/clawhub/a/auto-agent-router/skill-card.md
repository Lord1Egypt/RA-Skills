## Description: <br>
Routes slash-command-prefixed chat messages to configured specialist sub-agents for coding, writing, analysis, research, review, DevOps, or automatic task selection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiangzhiyu](https://clawhub.ai/user/jiangzhiyu) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agent operators use this skill to delegate chat requests to specialized sub-agents when a supported command appears at the start of a message. It is intended for workflows that benefit from concurrent, isolated sub-agent sessions and configurable routing rules. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can route ordinary chat to sub-agents from inferred keywords or configured commands. <br>
Mitigation: Disable autoRoute when broad automatic routing is not desired and require explicit slash commands for delegation. <br>
Risk: Message content and routing decisions may be written to /tmp/auto-route-handler.log. <br>
Mitigation: Disable logging, restrict log access, rotate logs, or avoid sending sensitive content through this skill. <br>
Risk: Chat input can add new bot-name aliases to the configuration. <br>
Mitigation: Turn off automatic bot-name learning or protect the configuration file from unreviewed updates. <br>
Risk: Generic aliases such as assistant and bot may broaden the set of messages eligible for command handling. <br>
Mitigation: Remove generic aliases from config.json and keep only deliberate, environment-specific bot names. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jiangzhiyu/auto-agent-router) <br>
- [Publisher profile](https://clawhub.ai/user/jiangzhiyu) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and plain text status messages with optional JSON-like routing results and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return sub-agent routing decisions, target agent names, model identifiers, task text, and log-oriented status output.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
