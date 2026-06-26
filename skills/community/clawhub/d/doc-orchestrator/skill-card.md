## Description: <br>
Orchestrates multi-chapter document generation with sub-agents by using contract-first decomposition, dependency analysis, file isolation, state persistence, and consistency validation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nicolayao](https://clawhub.ai/user/nicolayao) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and document authors use this skill to coordinate long structured documents such as PRDs, technical specs, research reports, design docs, and worldbuilding bibles that exceed a single agent's context window. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: High-impact maintenance workflows may propose actions that affect moderation, GitHub activity, artifact publishing, or nested reviews. <br>
Mitigation: Review proposed commands and workflow steps before execution, and configure nested review or autoreview behavior deliberately. <br>
Risk: Parallel sub-agents may overwrite work, repeat the document title, produce the wrong chapter, or introduce inconsistent shared definitions. <br>
Mitigation: Use one output file per chapter, keep shared definitions in the contract, strip duplicate titles during merge, and validate the final document for known conflicts. <br>
Risk: Long-running orchestration can lose state after context compaction or interruption. <br>
Mitigation: Persist orchestration state to the JSON state file after every status change and restore from that file before continuing. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON state-file examples and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces orchestration plans, sub-agent prompt templates, JSON state-file structure, merge steps, and validation checks.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
