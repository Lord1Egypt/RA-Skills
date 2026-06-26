## Description: <br>
CodeFlicker is a Kuaishou-focused CLI programming assistant skill that helps OpenClaw users install, configure, and invoke flickcli for coding tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[LeeGoDamn](https://clawhub.ai/user/LeeGoDamn) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Kuaishou developers and OpenClaw users use this skill to run CodeFlicker/flickcli for code generation, debugging, refactoring, code review, session continuation, git-worktree workspace management, and natural-language shell command generation. It assumes access to Kuaishou internal network resources, SSO, and the CodeFlicker npm package. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can configure or use auto-execution modes for coding and shell tasks. <br>
Mitigation: Keep approvalMode at default for normal work, review generated shell commands before execution, and reserve yolo-style automation for disposable sandboxes. <br>
Risk: Installation and login depend on an internal npm package, Kuaishou network access, and SSO. <br>
Mitigation: Install only if you are an intended CodeFlicker/Kuaishou user and trust the internal npm registry and SSO flow. <br>
Risk: Workspace commands can merge or delete git-worktree changes. <br>
Mitigation: Check repository status and review pending changes before running workspace complete, delete, or forced delete operations. <br>
Risk: The skill exposes skill and MCP server management paths that can extend tool access. <br>
Mitigation: Add only trusted skills and MCP servers, and review requested capabilities before enabling them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/LeeGoDamn/codeflicker) <br>
- [README](artifact/README.md) <br>
- [Skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown text with bash command examples and CLI wrapper output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke flickcli to edit files, run shell commands, continue sessions, configure global CLI settings, and manage git-worktree workspaces.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata; artifact _meta.json reports 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
