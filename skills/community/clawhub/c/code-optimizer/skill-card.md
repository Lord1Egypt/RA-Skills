## Description: <br>
Code Optimizer evaluates code quality with feature analysis and machine-learning-assisted strategy selection, then provides optimization-oriented reports and commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clementgu](https://clawhub.ai/user/clementgu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to assess generated or existing code, select a generation strategy, run standard test cases, and produce quality reports. It is intended for code-review and optimization workflows in OpenClaw/Hermes-style environments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The deployment script can persistently change the user's environment, including OpenClaw/Hermes configuration and command links. <br>
Mitigation: Review the deployment script first, back up Hermes configuration, and prefer a dry-run or manual setup before allowing integration changes. <br>
Risk: The skill can store code-derived evaluation results, which may retain sensitive repository details. <br>
Mitigation: Avoid running it on repositories with secrets or sensitive code until retention controls and storage locations are clear. <br>


## Reference(s): <br>
- [Code Optimizer ClawHub page](https://clawhub.ai/clementgu/code-optimizer) <br>
- [Code Optimizer homepage](https://clawhub.ai/skills/code-optimizer) <br>
- [Publisher profile](https://clawhub.ai/user/clementgu) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with CLI examples, configuration snippets, and text reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local CLI, model, configuration, and evaluation-history files when its deployment script is run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
