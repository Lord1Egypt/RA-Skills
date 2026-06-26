## Description: <br>
Claw Multi Agent helps OpenClaw users orchestrate multiple agents in parallel for research, model comparison, writing, and code workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zcyynl](https://clawhub.ai/user/zcyynl) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to split complex research, comparison, writing, and code-review work across coordinated sub-agents, then consolidate the results into reports or recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Spawned agents can receive broad tool access and may perform web search, file operations, or command execution. <br>
Mitigation: Ask for an explicit plan or dry run before spawning agents that can write files, run code, or use external tools. <br>
Risk: Prompts and outputs may be sent to configured model providers or forwarded into Feishu documents. <br>
Mitigation: Avoid sensitive prompts unless the configured providers and delivery channel are trusted. <br>
Risk: Aggregated multi-agent reports can include incorrect or misleading recommendations from sub-agent output. <br>
Mitigation: Review consolidated reports before using them for decisions, deployments, or published documentation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zcyynl/claw-multi-agent) <br>
- [Publisher profile](https://clawhub.ai/user/zcyynl) <br>
- [README](artifact/README.md) <br>
- [Skill instructions](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, plain text, shell command examples, and JSON configuration.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce saved Markdown reports or document-delivery instructions depending on the user channel.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence; package.json lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
