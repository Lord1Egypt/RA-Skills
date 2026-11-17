## Description: <br>
Canvas Json Handler helps agents generate, batch-update, merge, lay out, validate, repair, snapshot, and roll back JSON Canvas files for knowledge maps, workflows, boards, and related canvas structures. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, knowledge engineers, project managers, and operations teams use this skill to automate JSON Canvas creation, batch edits, layout, cross-canvas merge, repair, audit, and rollback workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may read and write .canvas or JSON files and run local layout or processing commands. <br>
Mitigation: Install only for workspaces where those file operations and local commands are intended, and ask the agent to list affected files and preview diffs before changes are applied. <br>
Risk: Merge, rollback, aggressive repair, or deletion behavior can change or remove canvas data. <br>
Mitigation: Require explicit confirmation before merge, rollback, aggressive repair, or deletion operations, and keep snapshots or backups available before mutating files. <br>
Risk: The API and network boundary is unclear in the release evidence. <br>
Mitigation: Avoid generic API or network integrations unless they are explicitly configured for the task, and keep credentials scoped to the minimum required access. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/canvas-json-handler) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, JSON files] <br>
**Output Format:** [Markdown guidance with JSON examples, command suggestions, and generated or modified .canvas/JSON files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose file reads, writes, local layout commands, merge operations, repair actions, snapshots, and rollback steps.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact frontmatter says 1.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
