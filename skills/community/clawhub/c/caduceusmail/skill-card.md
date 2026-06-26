## Description: <br>
☤CaduceusMail lets your OpenClaw automate an enterprise-level communications stack with one domain/mailbox combo. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lmtlssss](https://clawhub.ai/user/lmtlssss) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operations teams use this skill to automate Microsoft 365, Exchange, and Cloudflare mail/DNS setup for controlled mailbox, alias, lane, and deliverability workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The reviewed package is missing the core CaduceusMail tarball that the wrapper expects to verify and run. <br>
Mitigation: Do not provide production Microsoft 365, Exchange, or Cloudflare credentials until the tarball is included and scanned. <br>
Risk: The skill performs high-privilege Microsoft Graph, Exchange, and Cloudflare DNS operations. <br>
Mitigation: Use a dedicated least-privilege Entra service principal and a Cloudflare token scoped only to the target zone's DNS permissions. <br>
Risk: Runtime configuration requires sensitive tenant, mailbox, and DNS credentials. <br>
Mitigation: Inject secrets through the OpenClaw skill environment, keep runtime state owner-readable, and test first on a non-production domain. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lmtlssss/caduceusmail) <br>
- [CaduceusMail homepage](https://github.com/lmtlssss/caduceusmail) <br>
- [OpenClaw configuration example](examples/openclaw.config.json5) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate machine-readable state artifacts through the wrapped CaduceusMail tool.] <br>

## Skill Version(s): <br>
3.6.7 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
