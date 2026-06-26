## Description: <br>
Codegraph Assistant wraps npm codegraph to set up project indexing, query symbols, analyze affected files, and inject generated project context for coding workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huangxianzhan](https://clawhub.ai/user/huangxianzhan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to initialize and query a local code graph, inspect impacted files, and add generated codebase summaries to agent memory during implementation work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads and indexes local project code through a globally installed npm codegraph tool. <br>
Mitigation: Install and run it only in repositories where local indexing by that tool is acceptable. <br>
Risk: The inject command changes MEMORY.md without creating a backup or asking for confirmation. <br>
Mitigation: Review MEMORY.md after running inject and use version control before applying it in sensitive projects. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/huangxianzhan/codegraph-assistant) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration] <br>
**Output Format:** [Command-line text, Markdown context, optional JSON query output, and MEMORY.md updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs depend on the locally installed npm codegraph tool and the indexed repository.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
