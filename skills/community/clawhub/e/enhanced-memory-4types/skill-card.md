## Description: <br>
Provides a filesystem-backed memory system with semantic search, automatic loading, memory flush, and four memory categories for user, feedback, project, and reference knowledge. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[minmengxhw-cpu](https://clawhub.ai/user/minmengxhw-cpu) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use this skill to persist long-running memory as Markdown files, retrieve prior context, and organize memories into user, feedback, project, and reference categories. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Memory file reads and writes may escape the configured memory directory. <br>
Mitigation: Constrain memory_get and memory_write to the configured memoryDir before deployment and review any configured memoryDir value. <br>
Risk: The embedding path uses shell execution with user-controlled text. <br>
Mitigation: Replace shell-based curl invocation with a native HTTP client before using the skill in trusted or automated environments. <br>
Risk: The skill may persist sensitive personal, credential, regulated, or confidential team data. <br>
Mitigation: Avoid sensitive data until review, deletion, retention, and consent controls are defined and tested. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/minmengxhw-cpu/enhanced-memory-4types) <br>
- [Publisher profile](https://clawhub.ai/user/minmengxhw-cpu) <br>
- [README.md](README.md) <br>
- [PRODUCT.md](PRODUCT.md) <br>
- [CHANGELOG.md](CHANGELOG.md) <br>
- [Ollama](https://ollama.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown files and structured tool responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read, write, append, search, and flush memory files under the configured memory directory.] <br>

## Skill Version(s): <br>
1.1.0 (source: release metadata, skill.json, CHANGELOG.md, released 2026-03-31) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
