## Description: <br>
Sets Feishu cloud document permissions so external users can view shared documents through an anyone-with-the-link access setting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harrot90-code](https://clawhub.ai/user/harrot90-code) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to verify or change Feishu document sharing settings when a document must be accessible to users outside the organization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes a live-looking Feishu app secret. <br>
Mitigation: Rotate the exposed secret and require users to provide Feishu credentials from secure storage at runtime. <br>
Risk: The skill can make documents public to anyone with the link. <br>
Mitigation: Require explicit confirmation for each document before changing permissions, and restrict use to documents intended for external sharing. <br>
Risk: Document tokens may be exposed through logs. <br>
Mitigation: Avoid logging full document tokens and redact identifiers in audit records where possible. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Feishu API request examples, verification checks, and logging guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
