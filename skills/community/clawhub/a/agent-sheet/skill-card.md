## Description: <br>
Agent Sheet is a shell-native spreadsheet CLI for workbook inspection, sheet and range reads, precise writes, import/export handoff, review-table construction, formula analysis, and bounded workbook-native scripting with verification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yangluoshen](https://clawhub.ai/user/yangluoshen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use Agent Sheet to inspect and modify local spreadsheets through explicit workbook targets, safe shell roundtrips, import/export handoffs, and verification playbooks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and change local spreadsheets. <br>
Mitigation: Keep workbook IDs, sheets, and ranges explicit, then verify changed ranges and exported files after edits. <br>
Risk: Broad clears, deletes, and sheet lifecycle actions can have destructive effects. <br>
Mitigation: Review those actions before execution and prefer the smallest scoped command that satisfies the task. <br>
Risk: Installing agent-sheet@latest can change behavior over time in sensitive environments. <br>
Mitigation: Pin the npm package version when reproducibility or stronger change control is required. <br>


## Reference(s): <br>
- [Agent Sheet ClawHub page](https://clawhub.ai/yangluoshen/agent-sheet) <br>
- [Agent Sheet repository and documentation](https://github.com/dream-num/skills) <br>
- [Command Selection Matrix](references/command-selection-matrix.md) <br>
- [Shell Patterns](references/shell-patterns.md) <br>
- [Gotchas](references/gotchas.md) <br>
- [JavaScript API Minimal Reference](references/js-api-minimal.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash, Python, and CLI command snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Encourages bounded previews, explicit entry IDs, staged files, and verification after spreadsheet writes.] <br>

## Skill Version(s): <br>
0.1.6 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
