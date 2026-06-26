## Description: <br>
Use when the user wants to review auto-memory, promote durable instructions into CLAUDE.md or local memory, and clean up duplicates or conflicts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wimi321](https://clawhub.ai/user/wimi321) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and teams use this skill to audit agent memory layers, identify durable memory candidates, and surface duplicates, conflicts, or stale instructions before any approved cleanup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Durable memory updates could preserve personal, temporary, duplicate, or stale instructions. <br>
Mitigation: Classify memory entries by scope, present a grouped report first, and require explicit approval before applying cleanup or promotion. <br>
Risk: Proposed edits could affect unrelated or sensitive local repository state. <br>
Mitigation: Review scoped diffs or files before committing, especially in repositories with sensitive or unrelated local work. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wimi321/claude-code-memory-landscape-review) <br>
- [Publisher profile](https://clawhub.ai/user/wimi321) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown report with grouped proposals, conflict cleanup notes, and no-change recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill may propose memory-file changes, but edits require explicit user approval.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
