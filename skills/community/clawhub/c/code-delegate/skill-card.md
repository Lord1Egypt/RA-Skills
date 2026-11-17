## Description: <br>
Code Delegate guides agents through enterprise code delegation workflows for parallel task execution, queue management, write protection, team handoff, quality audits, and code review reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to delegate batches of coding, refactoring, testing, and quality-audit tasks to an agent while tracking execution status and generated reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill relies on command execution and remote LLM CLI tooling, which can process workspace content outside the local environment. <br>
Mitigation: Review workspace privacy requirements before use and run delegated tasks only where remote LLM processing is acceptable. <br>
Risk: The documented setup can create .delegate-toolkit configuration, log, and report files in the project workspace. <br>
Mitigation: Install and run the setup only in projects where those generated files are expected, and review them before committing or sharing. <br>
Risk: The skill references API-key based CLI authentication for automated environments. <br>
Mitigation: Provide API keys through the organization's normal secret-management process and avoid embedding secrets in source files or logs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/code-delegate) <br>
- [Publisher profile](https://clawhub.ai/user/thcjp) <br>
- [Homepage](https://skillhub.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash, JSON, and text examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce task status summaries, execution logs, audit reports, configuration snippets, and remediation guidance.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
