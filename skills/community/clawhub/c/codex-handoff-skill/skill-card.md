## Description: <br>
Offloads finalized coding plans to Codex CLI for automated execution while Claude Code supervises and reviews the loop. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[philipbankier](https://clawhub.ai/user/philipbankier) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to hand a confirmed coding plan to Codex CLI, then have Claude Code supervise execution, review diffs and tests, and request corrections until the plan is complete. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Codex CLI can make automated repository edits when the handoff proceeds. <br>
Mitigation: Use the skill only from an intended clean branch or worktree, and confirm the summarized plan before execution. <br>
Risk: Automated changes may be incomplete or fail tests. <br>
Mitigation: Review the final diff and test results after execution, and use the correction loop for remaining plan items. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/philipbankier/codex-handoff-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown status updates with shell commands and review summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May trigger Codex CLI to make repository edits after user confirmation.] <br>

## Skill Version(s): <br>
1.1.1 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
