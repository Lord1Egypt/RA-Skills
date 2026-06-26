## Description: <br>
Use Codex safely for repo-aware coding with explicit approvals, sandbox choices, MCP boundaries, and PR-ready verification workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to operate Codex safely in repository workflows, including setup, bounded execution, review mode, sandbox and approval choices, MCP or cloud boundaries, and handoff-ready verification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Write-capable Codex runs can change real repository files or widen a diff beyond the intended task. <br>
Mitigation: Confirm the target repo, working directory, dirty worktree state, sandbox level, approval policy, and verification plan before write-capable runs. <br>
Risk: Dangerous sandbox bypass, full access, remote MCP, or Codex Cloud apply can expand data exposure and side effects. <br>
Mitigation: Use least privilege by default and enable high-trust modes only after explicit approval, scope review, and a rollback plan. <br>
Risk: Prompts, selected repository context, tool results, and optional MCP or cloud payloads may leave the local machine. <br>
Mitigation: Install and use the skill only when those services are trusted for the selected data, and keep MCP and cloud flows explicitly approved. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ivangdavila/codex) <br>
- [Skill homepage](https://clawic.com/skills/codex) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Focuses on reviewable local agent operation, explicit trust boundaries, and verification-ready handoffs.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
