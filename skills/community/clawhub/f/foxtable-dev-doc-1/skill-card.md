## Description:

A Chinese-language Foxtable development documentation skill covering part 1 of the Foxtable help content, including development guidance, project publishing, advanced development notes, and appendices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[golgys0621](https://clawhub.ai/user/golgys0621)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and Foxtable users use this skill to answer questions about Foxtable development workflows, including scripting, data sources, reports, publishing, and advanced development topics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documentation includes legacy examples for silent remote updating.

Mitigation: Before implementing update flows from these examples, require signed update manifests and packages, explicit user or administrator control, logging, and rollback.

Risk: The documentation includes plaintext credential examples for network and updater workflows.

Mitigation: Replace example credentials with placeholders or secret storage, and prefer HTTPS or SFTP over plaintext FTP patterns.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/golgys0621/skills/foxtable-dev-doc-1)
- [关于Foxtable](references/00_关于Foxtable.md)
- [开发指南](references/02_开发指南.md)
- [发布项目](references/08_发布项目.md)
- [高级开发指南](references/09_高级开发指南.md)
- [附录](references/11_附录.md)
- [Foxtable Website](http://www.foxtable.com)
- [Foxtable Help](http://help.foxtable.com/)
- [Foxtable Mobile Help](http://www.foxtable.com/mobilehelp/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text guidance with code, command, and configuration snippets when relevant]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only responses should be reviewed before applying legacy network, credential, or updater examples.]

## Skill Version(s):

2.0.8 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
