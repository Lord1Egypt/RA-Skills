## Description: <br>
通过 GitHub Copilot CLI 分析代码、探索项目结构、生成文档和自动化开发任务，提高开发效率。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[biuyx](https://clawhub.ai/user/biuyx) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to install and operate GitHub Copilot CLI for code analysis, project exploration, documentation generation, code review, and automated development tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Code and repository context may be processed by GitHub Copilot services. <br>
Mitigation: Confirm that organization policy allows Copilot CLI use for the target repositories before sending prompts or code context. <br>
Risk: The GitHub token file can expose access if stored with weak local permissions. <br>
Mitigation: Protect ~/.copilot/github_token.txt with appropriate file permissions and rotate the token if exposure is suspected. <br>
Risk: The optional --yolo mode can execute or apply changes with reduced review. <br>
Mitigation: Use --yolo only in version-controlled or disposable workspaces where changes can be inspected and reverted. <br>
Risk: Installing an unexpected Copilot CLI package source could introduce supply-chain risk. <br>
Mitigation: Verify the Homebrew package source before installation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/biuyx/copilot-cli) <br>
- [GitHub Copilot documentation](https://docs.github.com/en/copilot) <br>
- [GitHub Copilot CLI command reference](https://docs.github.com/en/copilot/reference/cli-command-reference) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and prompt examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes setup steps, token file guidance, usage prompts, and troubleshooting notes.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
