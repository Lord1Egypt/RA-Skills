## Description: <br>
Feishu Ai Coding Assistant helps users plan large coding tasks, select AI coding tools, configure sub-agent runtimes, and produce commands, status text, and task parameters for coding workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rfdiosuao](https://clawhub.ai/user/rfdiosuao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to break down large software tasks, choose a supported AI coding tool, and prepare sub-agent sessions for coding, refactoring, testing, documentation, or research workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence reports exposed credentials in the artifacts. <br>
Mitigation: Do not install the release as-is; remove embedded tokens, rotate affected credentials, and review the source before use. <br>
Risk: The security evidence reports high-impact publishing and git push behavior. <br>
Mitigation: Require explicit user confirmation, dry-run review, and least-privilege credentials before any publish or push operation. <br>
Risk: The security evidence says some command descriptions overstate whether actions are executed or only shown as examples. <br>
Mitigation: Keep command text truthful and distinguish proposed commands from actions that the skill will execute. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rfdiosuao/feishu-ai-coding-assistant) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>
- [Feishu usage tutorial](https://my.feishu.cn/docx/IgkrdJvgxowAuMxAAkAcDaCOntf) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses with JSON snippets and bash command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include proposed install commands and sub-agent or session parameters for the host agent to review or execute.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
