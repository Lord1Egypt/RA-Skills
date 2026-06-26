## Description: <br>
EvoAgentX Workflow helps agents install, check, scaffold, and use EvoAgentX patterns for self-evolving OpenClaw workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[KyleChen26](https://clawhub.ai/user/KyleChen26) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent builders use this skill to scaffold EvoAgentX workflow templates, inspect installation status, and get examples for evolving multi-agent workflows in OpenClaw. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs or depends on the external EvoAgentX package without pinning a version. <br>
Mitigation: Install EvoAgentX in a virtual environment and pin or review the package version for important projects. <br>
Risk: Generated workflow templates may contain incomplete or unsuitable logic for the user's project. <br>
Mitigation: Review generated Python files before running them or integrating them into an agent workflow. <br>
Risk: The skill is a lightweight installer and scaffolder, not a complete production workflow optimization layer. <br>
Mitigation: Treat its output as setup guidance and examples, then validate EvoAgentX behavior and OpenClaw integration in the target environment. <br>


## Reference(s): <br>
- [EvoAgentX GitHub](https://github.com/EvoAgentX/EvoAgentX) <br>
- [EvoAgentX Documentation](https://evoagentx.github.io/EvoAgentX/) <br>
- [EvoAgentX arXiv Paper](https://arxiv.org/abs/2507.03616) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown-style guidance, inline shell commands, and generated Python files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The create-workflow command can write a Python workflow template in the current directory.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
