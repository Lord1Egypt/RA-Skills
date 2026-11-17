## Description: <br>
SSL certificate toolkit for Alibaba Cloud CAS covering identity configuration, domain verification, certificate download and upload, CSR generation, format conversion, and certificate matching. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operations engineers use this skill to manage Alibaba Cloud CAS SSL certificate workflows, including credential and profile setup, domain validation, certificate upload and download, CSR generation, format conversion, and key/certificate matching. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cloud certificate, DNS, IAM, and remote-server commands can make high-impact state changes. <br>
Mitigation: Require explicit user confirmation for all customizable parameters and review each DNS, IAM, SSH, and CAS command before execution. <br>
Risk: Broad quick-trial RAM policies can grant more CAS and DNS access than production workflows need. <br>
Mitigation: Use the documented fine-grained RAM policy for production and reserve broad system policies for short-lived trials only. <br>
Risk: Private keys, certificate passwords, and credential material can leak through logs, shell history, or shared terminals. <br>
Mitigation: Keep secrets out of chat, command echoes, logs, and shell history; use secure credential configuration and local protected files. <br>
Risk: Automatic CLI plugin updates can change tool behavior in sensitive environments. <br>
Mitigation: Disable or gate automatic plugin updates in controlled environments and review tool updates before use. <br>


## Reference(s): <br>
- [Aliyun CLI Installation & Configuration Guide](references/cli-installation-guide.md) <br>
- [Identity Resolver Commands](references/identity-resolver-commands.md) <br>
- [Domain Verify Commands](references/domain-verify-commands.md) <br>
- [Certificate Download Commands](references/cert-download-commands.md) <br>
- [Certificate Upload Commands](references/cert-upload-commands.md) <br>
- [RAM Policies](references/ram-policies.md) <br>
- [Related CLI Commands](references/related-commands.md) <br>
- [Verification Method](references/verification-method.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON policy snippets, and bundled shell-script outputs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate local certificate artifacts such as PEM, PFX, JKS, DER, chain, CSR, key, and verification output files when scripts are run.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
