## Description: <br>
Build and navigate DSP (Data Structure Protocol), a graph-based long-term structural memory of codebases for LLM agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[k-kolomeitsev](https://clawhub.ai/user/k-kolomeitsev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to create, update, navigate, and diagnose DSP-tracked project structure. It helps agents maintain .dsp metadata for modules, functions, dependencies, public exports, and reasons for relationships while working in a codebase. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled CLI can persist .dsp metadata and source-marker changes in a repository. <br>
Mitigation: Keep .dsp and related source-marker changes under version control and review diffs before committing. <br>
Risk: Delete operations may remove DSP graph entities and relationship metadata without confirmation or dry-run safeguards. <br>
Mitigation: Avoid autonomous use of delete commands until UID validation and confirmation or dry-run safeguards are in place. <br>


## Reference(s): <br>
- [Storage format](references/storage-format.md) <br>
- [Bootstrap procedure](references/bootstrap.md) <br>
- [Operations reference](references/operations.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and code annotations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces guidance for maintaining local .dsp metadata and may direct agents to run the bundled DSP CLI.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
