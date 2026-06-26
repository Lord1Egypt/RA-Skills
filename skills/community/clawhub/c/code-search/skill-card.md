## Description: <br>
Search codebase contents, filenames, and directory structures using ripgrep, fd, and tree with filters for file types, context, depth, and result limits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Yanxingang](https://clawhub.ai/user/Yanxingang) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to inspect unfamiliar codebases, find definitions and usages, locate files by pattern, and summarize project directory structure without modifying files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search results may reveal any readable files under the selected path. <br>
Mitigation: Run searches only against the intended project directory and review the requested --path before execution. <br>
Risk: Dependency installation can introduce supply-chain or privilege risk if tools are fetched manually or copied into privileged locations. <br>
Mitigation: Check for existing rg, fd, and tree installations first; prefer trusted OS package managers or verified releases, and use privileged installation only when explicitly intended. <br>
Risk: Missing rg, fd, or tree dependencies can cause commands to fail. <br>
Mitigation: Run the check command before use and install only the missing dependencies from trusted sources. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Yanxingang/code-search) <br>
- [Publisher profile](https://clawhub.ai/user/Yanxingang) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Structured text with labeled result sections and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only local search output; results may be truncated according to command limits.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
