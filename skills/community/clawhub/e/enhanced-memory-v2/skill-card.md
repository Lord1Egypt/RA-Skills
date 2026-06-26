## Description: <br>
A file-backed long-term memory skill for storing, searching, loading, and consolidating user, feedback, project, and reference memories. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[minmengxhw-cpu](https://clawhub.ai/user/minmengxhw-cpu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to preserve long-term working memory as Markdown files, retrieve relevant memories with keyword or vector search, and consolidate stale or duplicate memory entries over time. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill persists and reuses user, feedback, project, and reference memory, which can include sensitive or outdated information. <br>
Mitigation: Avoid storing secrets or sensitive personal data, review retained memories periodically, and remove stale or inappropriate entries. <br>
Risk: Security evidence reports that this version can read or write outside its memory folder. <br>
Mitigation: Restrict memory paths to an approved memory directory and review configured storage locations before high-trust use. <br>
Risk: Security evidence reports shell-built embedding commands using memory text. <br>
Mitigation: Disable vector search unless needed, prefer shell-free embedding calls, and keep Ollama and embedding model configuration under operator control. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/minmengxhw-cpu/enhanced-memory-v2) <br>
- [README](artifact/README.md) <br>
- [Product documentation](artifact/PRODUCT.md) <br>
- [Changelog](artifact/CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, configuration, guidance] <br>
**Output Format:** [Markdown memory files, JSON tool responses, and configuration values] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May persist memory content locally and return retrieved memory snippets.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release and CHANGELOG, released 2026-03-31) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
