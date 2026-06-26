## Description: <br>
Context Manager helps agents collect, tag, connect, review, and recall personal context for thought trees, cognitive maps, daily reflection logs, and decision history. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lj22503](https://clawhub.ai/user/lj22503) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to organize personal knowledge, record important cognition, build links between internal reflections and external information, and revisit context before decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The package may persist or modify personal notes, indexes, reports, rules, and belief files in local knowledge stores. <br>
Mitigation: Use backups, review the configured storage paths, and inspect changes before running auto-fix or belief-update workflows on sensitive notes. <br>
Risk: The release mixes Context Manager materials with broader knowledge-workflow artifacts, which can make expected behavior unclear. <br>
Mitigation: Review the included modules and documentation before installation and use only the workflows that match the intended context-management task. <br>
Risk: Optional AI-enhanced analysis can involve sensitive personal context. <br>
Mitigation: Avoid processing sensitive notes until credentials, model configuration, and data-handling expectations have been reviewed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lj22503/context-manager-v1) <br>
- [Subfunction details](artifact/references/子功能详解.md) <br>
- [Usage examples](artifact/使用示例.md) <br>
- [Design document](artifact/设计文档.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Configuration, Guidance] <br>
**Output Format:** [Markdown and JSON-like structured records, with configuration and code snippets in examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local knowledge-base files under configured context or knowledge directories.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and clawhub.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
