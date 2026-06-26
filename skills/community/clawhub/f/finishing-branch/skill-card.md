## Description: <br>
Completes development work by guiding test verification and presenting structured merge, pull request, keep, or discard options. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wpank](https://clawhub.ai/user/wpank) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill after implementation is complete to verify tests and choose a structured branch integration path. It helps an agent guide local merge, pull request creation, branch preservation, or explicit discard workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide local and remote branch deletion. <br>
Mitigation: Confirm the exact branch and worktree path before cleanup, and use dry-run or listing modes before deletion when available. <br>
Risk: Running project tests may execute code from the current repository. <br>
Mitigation: Use the skill only in trusted repositories, or inspect the test commands before allowing the agent to run them. <br>
Risk: The security review notes inconsistent cleanup instructions. <br>
Mitigation: Review the selected option before cleanup and preserve the worktree for workflows that should keep it. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/wpank/finishing-branch) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands] <br>
**Output Format:** [Markdown with inline shell commands and structured options] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prompts for explicit confirmation before destructive discard actions.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
