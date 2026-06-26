## Description: <br>
Use Cursor safely across editor, CLI, rules, background agents, Bugbot, and MCP workflows with repo-aware context and reviewable execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to choose and operate the right Cursor surface for coding, automation, rules, context, review, privacy, and remote-workflow decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cursor indexing, Background Agents, Bugbot, GitHub integration, remote MCP, or unattended cursor-agent runs can expand data exposure and execution scope. <br>
Mitigation: Require explicit approval for these workflows, scope them to clearly identified repos and tasks, and review outputs before applying or merging changes. <br>
Risk: Ignore files such as .cursorignore and .cursorindexingignore reduce exposure but do not guarantee that sensitive files are unreachable through tools or terminal commands. <br>
Mitigation: Keep secrets and production credentials outside accessible repo paths and treat indexing, terminal access, GitHub integration, and MCP as separate trust decisions. <br>
Risk: Non-interactive cursor-agent runs can widen scope without interactive approval prompts. <br>
Mitigation: Before launching unattended runs, record the repo path, objective, allowed files, command boundary, and verification path. <br>


## Reference(s): <br>
- [Cursor skill page](https://clawhub.ai/ivangdavila/cursor) <br>
- [Cursor skill homepage](https://clawic.com/skills/cursor) <br>
- [Cursor documentation](https://docs.cursor.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, checklists, and configuration paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should name the active Cursor surface, scope repo and trust boundaries, and end with reviewable evidence.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
