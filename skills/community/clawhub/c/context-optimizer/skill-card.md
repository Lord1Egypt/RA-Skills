## Description: <br>
Context Optimizer helps agents manage long DeepSeek conversations by compacting, scoring, archiving, retrieving, and logging context to reduce overflow while preserving useful information. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ad2546](https://clawhub.ai/user/ad2546) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent builders use this skill in Clawdbot or JavaScript agent workflows to keep long DeepSeek conversations within context limits while preserving recent or high-priority information. It can compact messages, retrieve relevant archived snippets, and report context health for ongoing conversations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Conversation content can be archived locally and later reused as retrieved context. <br>
Mitigation: Treat the archive as sensitive data, choose an appropriate archive path, restrict file permissions, and disable archive or chat logging for sensitive work. <br>
Risk: Retrieved archive snippets can affect future agent responses, including high-stakes responses. <br>
Mitigation: Review retrieved archive context before using it for important decisions or high-stakes workflows. <br>
Risk: Uninstall instructions include recursive deletion commands for the skill folder and archive data. <br>
Mitigation: Double-check paths before running any rm -rf commands, especially when using a custom archive path. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ad2546/context-optimizer) <br>
- [README.md](README.md) <br>
- [INSTALL.md](INSTALL.md) <br>
- [SKILL.md](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown documentation with JavaScript, YAML, and shell examples; runtime outputs include optimized message arrays, archive snippets, status objects, and chat log text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local token counting and optional embedding-based archive indexing; archive and chat logging behavior are configurable.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
