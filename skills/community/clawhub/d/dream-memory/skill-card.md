## Description: <br>
Dream Memory guides agents in setting up and operating a workspace memory system using Markdown files, OpenViking vector search, Ollama bge-m3 embeddings, and session lifecycle checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shoukuan](https://clawhub.ai/user/shoukuan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to configure cross-session memory for OpenClaw agents, including memory file layout, vector indexing, session flush checks, and troubleshooting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist and index cross-session memory, including private project details or sensitive personal data. <br>
Mitigation: Define what may be stored before use, avoid writing secrets or sensitive personal data, and periodically review retained memory files. <br>
Risk: Memory search may expose information outside the intended workspace or agent if scoping is too broad. <br>
Mitigation: Restrict memory search sources and paths to the intended workspace or agent configuration. <br>
Risk: The setup reference includes a curl-to-shell Ollama installer command. <br>
Mitigation: Verify the installer source and contents before execution, or install Ollama through an approved package workflow. <br>


## Reference(s): <br>
- [Ollama + OpenViking setup](references/ollama-setup.md) <br>
- [Dream Memory release page](https://clawhub.ai/shoukuan/dream-memory) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes a shell self-check script for local workspace memory setup.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
