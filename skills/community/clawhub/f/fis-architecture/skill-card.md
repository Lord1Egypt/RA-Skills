## Description: <br>
Orchestrate multi-agent workflows with JSON tickets and A2A coordination for delegation between a main agent and worker agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MuseLinn](https://clawhub.ai/user/MuseLinn) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to coordinate multi-step work across main and worker agents, track JSON task tickets, and generate Discord/OpenClaw handoff commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill generates executable sessions_send and sessions_spawn commands from task and ticket inputs. <br>
Mitigation: Review generated agent commands before execution and prefer versions that validate ticket IDs and safely serialize command arguments. <br>
Risk: Ticket contents and notes can include sensitive task details that are stored in local JSON files and shared through Discord/OpenClaw workflows. <br>
Mitigation: Avoid placing secrets in tickets, notes, summaries, or deliverable names; restrict ticket storage to trusted workspaces. <br>
Risk: Discord bot permissions and thread routing can expose task context beyond the intended forum channel. <br>
Mitigation: Grant bots only the forum permissions and channel access required for the workflow, then verify thread creation and reply behavior before operational use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/MuseLinn/fis-architecture) <br>
- [Declared project homepage](https://github.com/linn/fis-architecture) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON snippets and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates ticket identifiers, status reports, Discord thread templates, and agent handoff commands for review before execution.] <br>

## Skill Version(s): <br>
3.3.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
