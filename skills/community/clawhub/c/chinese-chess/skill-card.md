## Description: <br>
Use when the user wants to generate a Chinese chess game from scratch, or wants to improve/enhance an existing Chinese chess game for better experience. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tianzhenjiu](https://clawhub.ai/user/tianzhenjiu) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to generate a new Chinese chess (Xiangqi) game or improve an existing Chinese chess game by reusing pre-built source code patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill instructs the agent to read and reuse hard-coded local directories outside the skill package. <br>
Mitigation: Install only if those directories are trusted and controlled; prefer changing the skill to use bundled or user-provided template paths. <br>
Risk: The skill tells the agent to inspect and copy source folders before asking the user. <br>
Mitigation: Require explicit user confirmation before reading or copying external source directories. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tianzhenjiu/chinese-chess) <br>


## Skill Output: <br>
**Output Type(s):** [code, shell commands, markdown, guidance] <br>
**Output Format:** [Markdown with code changes and command suggestions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or modify project files when applying source code patterns.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
