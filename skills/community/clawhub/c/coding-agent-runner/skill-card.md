## Description: <br>
Run Codex CLI, Claude Code, OpenCode, or Pi Coding Agent via background process for programmatic control. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pratiknarola](https://clawhub.ai/user/pratiknarola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to run coding agents in focused working directories, monitor long-running sessions, and coordinate non-interactive coding, PR review, and issue-fix workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unsandboxed autonomous runs may modify repositories, commit changes, push branches, or open pull requests without an explicit review checkpoint. <br>
Mitigation: Prefer sandboxed modes, review generated diffs before commit or push, and avoid --yolo on untrusted repositories. <br>
Risk: Long-running coding-agent sessions can operate in the wrong repository or branch if launched from a broad or live workspace. <br>
Mitigation: Run sessions in focused working directories, temporary clones, or git worktrees, especially for PR review and issue-fix workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pratiknarola/coding-agent-runner) <br>
- [Publisher profile](https://clawhub.ai/user/pratiknarola) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces agent-running procedures and review workflow guidance; it does not itself execute commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
