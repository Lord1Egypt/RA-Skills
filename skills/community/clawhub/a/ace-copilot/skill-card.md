## Description: <br>
ACE Copilot helps developers work with IBM App Connect Enterprise 12.0 message flows, ESQL, BAR deployments, integration node and server operations, and troubleshooting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shoaibkhan](https://clawhub.ai/user/shoaibkhan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and integration engineers use this skill to implement, debug, deploy, and review IBM ACE 12.0 message flows, ESQL changes, BAR files, and integration server operations. It is especially relevant for ACE project work that starts from tickets and ends with tested changes or pull requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Deployment, undeploy, delete, trace, diagnostic bundle, and credential commands can affect production IBM ACE environments. <br>
Mitigation: Install only for IBM ACE or App Connect Enterprise work, verify node and server targets, and require explicit user confirmation before executing production-impacting commands. <br>
Risk: Credential examples and diagnostic workflows could expose secrets or sensitive message data if copied directly into command lines or shared trace files. <br>
Mitigation: Avoid placing real secrets on command lines, redact trace and support files before sharing, and protect diagnostic artifacts according to the environment's data-handling rules. <br>
Risk: The skill has broad activation language and may offer powerful operational guidance in contexts where the user did not intend to change an ACE runtime. <br>
Mitigation: Confirm the user is working on IBM ACE/App Connect Enterprise and distinguish advisory steps from executable actions before proposing or running commands. <br>


## Reference(s): <br>
- [Architecture](artifact/references/architecture.md) <br>
- [Message Flows](artifact/references/message-flows.md) <br>
- [ESQL](artifact/references/esql.md) <br>
- [CLI Commands](artifact/references/cli-commands.md) <br>
- [Deployment](artifact/references/deployment.md) <br>
- [Troubleshooting](artifact/references/troubleshooting.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/shoaibkhan/ace-copilot) <br>
- [Publisher GitHub Profile](https://github.com/ShoaibKhan) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline code blocks and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include IBM ACE CLI commands, ESQL snippets, configuration examples, diagnostic steps, and deployment guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
