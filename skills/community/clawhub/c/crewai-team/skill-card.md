## Description: <br>
Uses a CrewAI multi-agent team to analyze product ideas and generate product requirements documents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[namechenxinyu](https://clawhub.ai/user/namechenxinyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Product managers, founders, and developers use this skill to turn a product idea into a structured PRD with market research, product design, architecture, development, and QA sections. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Runnable scripts include a hard-coded external LLM API key and forced provider endpoint. <br>
Mitigation: Remove embedded credentials, rotate the key if it was real, and configure provider credentials through environment variables before running. <br>
Risk: Product ideas and generated PRD content may be sent to the configured external LLM service. <br>
Mitigation: Avoid submitting confidential product details unless the selected provider and account are approved for that data. <br>
Risk: Dependency installation and generated logs or PRD files may expose operational details. <br>
Mitigation: Install dependencies in an isolated environment and review generated files before sharing them externally. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/namechenxinyu/crewai-team) <br>
- [Publisher Profile](https://clawhub.ai/user/namechenxinyu) <br>
- [Skill Definition](artifact/SKILL.md) <br>
- [Usage Guide](artifact/USAGE.md) <br>
- [DashScope Console](https://dashscope.console.aliyun.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown PRD documents and terminal text, with optional Python and shell snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save PRD and supporting analysis files; requires Python 3.10 and external LLM credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
