## Description: <br>
Provides guidance and shell helpers for using the DeepMiner dm-cli to start, monitor, stop, and retrieve results from DM tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dmpm-mininglamp](https://clawhub.ai/user/dmpm-mininglamp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to configure dm-cli, submit DeepMiner tasks, poll task state, manage asynchronous task lifecycle actions, and return DM results and generated files to the user. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles DeepMiner AccessKeys and endpoint configuration. <br>
Mitigation: Install only from a trusted publisher, use least-privilege AccessKeys, and avoid placing real secrets in shell history, logs, or shared transcripts. <br>
Risk: Polling helpers can forward full DeepMiner results or file links between sessions with weak destination controls. <br>
Mitigation: Verify the destination session before enabling notification helpers, avoid shared sessions for sensitive prompts or results, and review persistent status files before sharing. <br>
Risk: DeepMiner prompts, outputs, task IDs, and generated file URLs may contain sensitive business data. <br>
Mitigation: Avoid sending highly sensitive prompts or results through shared sessions, and restrict access to generated files and status artifacts. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/dmpm-mininglamp/deepminer-skill) <br>
- [thread.result response structure](references/response-structure.md) <br>
- [DeepMiner agent session page pattern](https://deepminer.com.cn/agents/${thread_id}) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include DeepMiner thread IDs, task IDs, task state, result text, generated file URLs, and polling status.] <br>

## Skill Version(s): <br>
1.7.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
