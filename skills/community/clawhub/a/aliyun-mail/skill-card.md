## Description: <br>
A skill to send emails via Aliyun enterprise email service with support for markdown, HTML text, attachments, and syntax highlighting for code blocks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jixsonwang](https://clawhub.ai/user/jixsonwang) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to send plain text, Markdown, or HTML email through Aliyun Enterprise Mail, including messages built from files and messages with attachments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Email bodies, recipient addresses, and attachments leave the local machine through Aliyun SMTP infrastructure. <br>
Mitigation: Double-check recipients and attachments before sending, and avoid sending sensitive material unless that transfer is intended. <br>
Risk: SMTP credentials are loaded from a local JSON configuration file. <br>
Mitigation: Use a dedicated SMTP account or app password, keep the configuration file private, and restrict file permissions such as chmod 600. <br>
Risk: Body files and attachment paths cause local files to be read and included in outgoing email. <br>
Mitigation: Review requested file paths before execution and attach only files meant for the recipient. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jixsonwang/aliyun-mail) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [package.json](artifact/package.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON configuration examples, and Python command-line usage] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can invoke SMTP sending behavior that transmits email bodies and attachments through the configured mail server.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence.release.version, artifact/_meta.json, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
