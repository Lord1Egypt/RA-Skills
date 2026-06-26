## Description: <br>
Token-based context compaction for local models (MLX, llama.cpp, Ollama) that don't report context limits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[emberDesire](https://clawhub.ai/user/emberDesire) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to estimate context size and summarize older conversation messages before local model sessions exceed their practical context limits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Compaction can send prior conversation history to the configured LLM runtime for summarization, which may expose sensitive prompts, code, credentials, or personal data if the runtime is not trusted. <br>
Mitigation: Configure summarization to use only trusted local models, avoid using it with sensitive or high-stakes sessions without review, and check the original conversation before relying on a compacted summary. <br>
Risk: Setup changes local OpenClaw configuration and stores backups that may contain model or provider details. <br>
Mitigation: Review the generated configuration before restarting OpenClaw and keep backup files in a secure local location. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/emberDesire/context-compactor) <br>
- [OpenClaw compaction documentation](https://docs.openclaw.ai/concepts/compaction) <br>
- [npm package](https://www.npmjs.com/package/jasper-context-compactor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces setup guidance, OpenClaw plugin configuration, context usage summaries, and compacted conversation summaries.] <br>

## Skill Version(s): <br>
0.3.8 (source: SKILL.md frontmatter, package.json, server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
