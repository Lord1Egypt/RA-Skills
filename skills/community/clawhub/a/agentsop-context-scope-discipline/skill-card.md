## Description: <br>
Coder-agent working-file budget discipline for keeping editable context focused, separating read-only reference material from files to edit, and dropping files once they are no longer needed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentsope](https://clawhub.ai/user/agentsope) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use this skill during multi-file code edits to decide which files belong in the editable working set, which files should stay read-only, and when to drop or split context to preserve editing accuracy. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent may omit an important file from editable context during a multi-file edit. <br>
Mitigation: Confirm the target files before edits, keep important non-edit targets as read-only references, and re-run file location when the correct target is uncertain. <br>
Risk: The agent may drop context that is still needed later in a large coding task. <br>
Mitigation: Drop files only after their current edit is complete, preserve needed contracts as read-only context, and split broad tasks into smaller sessions when the context budget remains high. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/agentsope/agentsop-context-scope-discipline) <br>
- [R1 source evidence](references/R1-source-evidence.md) <br>
- [Aider edit errors troubleshooting](https://aider.chat/docs/troubleshooting/edit-errors.html) <br>
- [Aider token limits troubleshooting](https://aider.chat/docs/troubleshooting/token-limits.html) <br>
- [Aider repository map documentation](https://aider.chat/docs/repomap.html) <br>
- [Aider SWE-Bench Lite repository map results](https://aider.chat/2024/05/22/swe-bench-lite.html) <br>
- [Aider edit formats documentation](https://aider.chat/docs/more/edit-formats.html) <br>
- [Aider commands documentation](https://aider.chat/docs/usage/commands.html) <br>
- [Aider conventions documentation](https://aider.chat/docs/usage/conventions.html) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline command examples and decision tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Focuses on working-set classification, context-budget monitoring, file dropping, and task splitting.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata; artifact frontmatter reports 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
