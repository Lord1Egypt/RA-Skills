## Description:

Use mcporter to call cpc-mcp-server AutoJS Agent tools for cloud Android task execution and result retrieval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sav7ng](https://clawhub.ai/user/sav7ng)

### License/Terms of Use:


## Use Case:

Developers and QA engineers use this skill to run AutoJS-based tasks on cloud Android devices, including app smoke tests, scripted remote operations, and result retrieval through screenshots, logs, or text output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLOUDPHONE_API_KEY can authorize cloud-phone automation beyond the immediate task.

Mitigation: Use a least-privileged API key, prefer test devices and test accounts, and avoid committing or logging real credentials.

Risk: mcporter supports broader MCP, auth, config, daemon, stdio, URL, and code-generation operations than this skill's stated cloud-phone workflow requires.

Mitigation: Restrict use to the intended cpc-mcp-server calls unless broader mcporter capabilities are explicitly reviewed and approved.

Risk: Screenshots and logs from remote Android tasks may capture sensitive app or account data.

Mitigation: Collect screenshots and logs only when needed, use non-production accounts where possible, and redact sensitive output before sharing.

Risk: The skill depends on the external mcporter package.

Mitigation: Verify and pin the mcporter package source and version before deployment.

## Reference(s):

- [Cloud Phone Agent on ClawHub](https://clawhub.ai/sav7ng/skills/cloudphone)
- [mcporter](http://mcporter.dev)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON argument examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include cloud-phone screenshots, logs, or text results when requested by the user.]

## Skill Version(s):

0.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
