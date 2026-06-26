## Description: <br>
AI模型切换器 helps OpenClaw users route routine work to local models and more complex chat, research, coding, analysis, long-document, and creative tasks to configured cloud models to balance cost and performance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[savidwilbert](https://clawhub.ai/user/savidwilbert) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and developers use this skill to choose between local Ollama and cloud model configurations by task type, while tracking model switches, token use, and estimated cost. It is intended for normal productivity workflows where users want a configurable hybrid local/cloud model strategy. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cloud model modes may send future prompts, code, or documents to third-party providers. <br>
Mitigation: Use local mode for confidential work unless the selected cloud provider is trusted and approved for that data. <br>
Risk: Local switch logs and statistics may reveal model usage history. <br>
Mitigation: Review or delete local switch log and statistics files when usage history is sensitive. <br>


## Reference(s): <br>
- [Skill page](https://clawhub.ai/savidwilbert/ai-model-switcher) <br>
- [Publisher profile](https://clawhub.ai/user/savidwilbert) <br>
- [docs/README.md](docs/README.md) <br>
- [config/config.json](config/config.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with OpenClaw command examples and JSON configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read and update local configuration, switch log, and usage statistics files under the skill configuration directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: OpenClaw metadata and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
