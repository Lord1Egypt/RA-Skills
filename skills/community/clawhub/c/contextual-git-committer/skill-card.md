## Description: <br>
AI-powered Git assistant that analyzes staged changes and terminal history to craft meaningful, conventional commit messages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liverock](https://clawhub.ai/user/liverock) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill inside Git repositories to analyze staged changes and receive commit message options in conventional, detailed, and informal styles. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads recent bash or zsh history and may include sensitive commands in AI-facing output. <br>
Mitigation: Review or clear shell history before use, avoid running it after secret-bearing commands, and inspect the generated context before relying on the suggested commit messages. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with structured Git context and commit message guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes staged diff context, changed files, diff stats, recent commits, branch name, and recent shell history when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
