## Description: <br>
Helps an agent use BizyAir to search AI apps and ModelZoo endpoints, prepare image, video, and audio generation tasks, run confirmed jobs, and check account assets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ezra-y](https://clawhub.ai/user/ezra-y) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to operate BizyAir media-generation workflows through an agent, including selecting models, preparing parameters, uploading approved inputs, confirming paid executions, and retrieving generated outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a BizyAir API key and can spend BizyAir balance for confirmed generation tasks. <br>
Mitigation: Require an explicit execution confirmation before paid runs and verify account status before starting task workflows. <br>
Risk: Selected local image, audio, or video inputs may be uploaded to BizyAir or OSS storage. <br>
Mitigation: Use only media that is acceptable to share with BizyAir services and avoid private source material unless that exposure is approved. <br>
Risk: Prompts, file paths, and batch details may remain in local runtime or batch files. <br>
Mitigation: Avoid sensitive prompts and clear local runtime state after sensitive work. <br>
Risk: Tool output can include hidden instructions intended for the agent. <br>
Mitigation: Review tool-returned guidance before acting on it and keep user-facing output separate from agent-only instructions. <br>


## Reference(s): <br>
- [BizyAir homepage](https://bizyair.cn) <br>
- [ClawHub skill page](https://clawhub.ai/ezra-y/bizyair-skill) <br>
- [01 Query Search](artifact/references/01-query-search.md) <br>
- [02 Account Assets](artifact/references/02-account-assets.md) <br>
- [03 AI App Tasks](artifact/references/03-ai-app-tasks.md) <br>
- [04 ModelZoo Tasks](artifact/references/04-modelzoo-tasks.md) <br>
- [05 Common Reference](artifact/references/05-common-reference.md) <br>
- [06 Batch Rules](artifact/references/06-batch-rules.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and shell command guidance, with generated media URLs returned as Markdown image embeds or plain video links.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local runtime state, batch files, and configuration guidance for BizyAir API key setup.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
