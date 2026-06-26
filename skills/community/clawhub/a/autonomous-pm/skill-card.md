## Description: <br>
Coordinates autonomous project work by having agents share task state through STATE.yaml and use a Node-based project manager workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sunnyhot](https://clawhub.ai/user/sunnyhot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to coordinate multi-agent project work with shared STATE.yaml files, delegated PM sessions, and git-backed status updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow asks agents to spawn autonomous subagents, modify project files, and commit changes, which can exceed the user's intended scope. <br>
Mitigation: Require explicit user approval before spawning subagents, changing project files, or running git add or commit. <br>
Risk: The documented Node command depends on an unbundled local project-manager.cjs script and a hardcoded local workspace path. <br>
Mitigation: Inspect or supply the referenced script and replace the local path before using the workflow. <br>
Risk: STATE.yaml and git commits may expose sensitive project status or repository context. <br>
Mitigation: Use the skill only in controlled workspaces and keep STATE.yaml contents and commit scope limited, especially in repositories with secrets or sensitive internal state. <br>


## Reference(s): <br>
- [Autonomous coding agents inspiration](https://nicholas.carlini.com/) <br>
- [OpenClaw project](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with YAML, JavaScript, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node; git is optional for audit-log commits.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
