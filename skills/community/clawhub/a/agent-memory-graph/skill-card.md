## Description: <br>
Memory Graph provides an agent-agnostic personal knowledge graph stored as Markdown files with YAML frontmatter for persistent context about people, projects, tools, concepts, decisions, and activity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[afgonullu](https://clawhub.ai/user/afgonullu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, external users, and agents use this skill to create, query, maintain, and visualize a persistent local memory graph across agent sessions or tools. It is suited for durable personal context, activity logging, relation discovery, and setup guidance for a file-based knowledge store. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives agents broad durable access to a persistent personal memory folder that may contain sensitive context. <br>
Mitigation: Install only when that access is acceptable, avoid storing secrets or highly sensitive personal data, and add local rules for what agents may read or write. <br>
Risk: Server security guidance flags unsafe command and HTML handling around QMD, auto-commit, and graph visualization when memory content is untrusted. <br>
Mitigation: Review or patch those paths before use with untrusted content, and be cautious when opening generated graph HTML. <br>


## Reference(s): <br>
- [Memory Graph README](artifact/README.md) <br>
- [Memory Graph Setup Guide](artifact/references/setup.md) <br>
- [ClawHub release page](https://clawhub.ai/afgonullu/agent-memory-graph) <br>
- [QMD semantic search](https://github.com/tobi/qmd) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown files, CLI text, shell commands, and generated local index files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a persistent local ~/memory directory, requires Node.js 22+, and can optionally use QMD for semantic search.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
