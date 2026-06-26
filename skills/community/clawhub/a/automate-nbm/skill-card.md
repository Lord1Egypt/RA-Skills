## Description: <br>
Automate Nbm routes tasks to specialized AI agent personas and orchestration workflows for software, product, marketing, testing, support, and automation work. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ironiclawdoctor-design](https://clawhub.ai/user/ironiclawdoctor-design) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and teams use this skill to choose single agents, departments, or an orchestrator for task planning, implementation guidance, QA review, growth work, and issue-driven automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist SSH private key material when AUTOMATE_SSH_KEY is configured. <br>
Mitigation: Review before installation, use low-privilege credentials, avoid setting AUTOMATE_SSH_KEY unless required, and rotate credentials if exposure is suspected. <br>
Risk: GitHub issue comments or webhook notifications can receive task content. <br>
Mitigation: Treat configured notification targets as recipients of task data and restrict webhook URLs, GitHub tokens, and repository issue access. <br>
Risk: Issue labels can trigger task or orchestration workflows. <br>
Mitigation: Restrict who can apply task and orchestrate labels, and review generated outputs before using them in production work. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ironiclawdoctor-design/automate-nbm) <br>
- [Publisher profile](https://clawhub.ai/user/ironiclawdoctor-design) <br>
- [README](README.md) <br>
- [Quick Start Guide](docs/QUICKSTART.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports and plans with optional code snippets, shell commands, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write task result files or post notifications when installed with appropriate GitHub or webhook credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
