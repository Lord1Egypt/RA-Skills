## Description: <br>
完整记忆系统 - 文件系统记忆 + 向量搜索 + 四类记忆分类 + AutoDream 自动整合 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[minmengxhw-cpu](https://clawhub.ai/user/minmengxhw-cpu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to give an agent persistent file-based memory, semantic search, typed memory categories, feedback records, and optional AutoDream memory consolidation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read or write beyond its intended memory folder. <br>
Mitigation: Use a dedicated non-sensitive memory directory and avoid exposing memory_get or memory_write to untrusted prompts until path sandboxing and confirmation for destructive changes are added. <br>
Risk: AutoDream can automatically process stored memory files. <br>
Mitigation: Disable AutoDream unless automatic consolidation is explicitly wanted and the memory directory has been reviewed. <br>
Risk: Memory contents can be sent to MiniMax when an API key is present. <br>
Mitigation: Do not store secrets or sensitive personal data, and only configure the MiniMax API key when external processing of memory contents is acceptable. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/minmengxhw-cpu/enhanced-memory-v3) <br>
- [Publisher profile](https://clawhub.ai/user/minmengxhw-cpu) <br>
- [README](README.md) <br>
- [Product documentation](PRODUCT.md) <br>
- [Changelog](CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Configuration, Guidance] <br>
**Output Format:** [Markdown and JSON tool responses for memory search, read, write, flush, and AutoDream status workflows] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read, write, append, consolidate, and index local memory files according to skill configuration.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release evidence and changelog, released 2026-03-31) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
