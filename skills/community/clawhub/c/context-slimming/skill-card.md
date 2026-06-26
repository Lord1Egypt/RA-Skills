## Description: <br>
Diagnose and optimize an OpenClaw agent workspace's injected context files to reduce per-round token consumption. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[scomper](https://clawhub.ai/user/scomper) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to audit and slim OpenClaw workspace context files, move detailed guidance into on-demand references, remove duplicated injected content, and reduce baseline token usage across agent turns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent workspace context edits can change future agent behavior. <br>
Mitigation: Ask for a plan first, keep backups, and review diffs before applying changes. <br>
Risk: Deleting, moving, or committing workspace files can be difficult to undo if approved too broadly. <br>
Mitigation: Manually approve deletions, moves, and commits, and keep the scope limited to context-slimming changes. <br>
Risk: Injected markdown may expose secrets or sensitive operational details in every agent turn. <br>
Mitigation: Avoid storing actual secrets in injected markdown and move sensitive details out of always-loaded context. <br>


## Reference(s): <br>
- [Context Slimming Skill Page](https://clawhub.ai/scomper/context-slimming) <br>
- [Before and After](references/before-after.md) <br>
- [Slimming Checklist](references/checklist.md) <br>
- [Wenyan Patterns](references/wenyan-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and file-organization recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose edits to persistent workspace context files; review diffs before applying changes.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
