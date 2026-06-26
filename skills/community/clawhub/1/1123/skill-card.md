## Description: <br>
Skill to call Cloud API for Tencent Cloud (Tencent Cloud). Used for cloud automation or resource management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[2513483494](https://clawhub.ai/user/2513483494) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operators use this skill to install and authenticate tccli, look up Tencent Cloud API documentation, and prepare tccli commands for Tencent Cloud automation or resource management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Authenticated tccli commands can create, modify, or delete Tencent Cloud resources. <br>
Mitigation: Use a least-privilege Tencent Cloud account and review each tccli command before running it. <br>
Risk: Tencent Cloud SecretId or SecretKey values could be exposed if requested, pasted, or printed. <br>
Mitigation: Do not ask for or paste SecretId or SecretKey values, and avoid commands that print credential configuration. <br>
Risk: The OAuth login command can block while waiting for browser authorization. <br>
Mitigation: Tell the user to open the authorization link in a browser and complete login before continuing. <br>
Risk: Parallel tccli calls can fail due to configuration file contention. <br>
Mitigation: Run tccli commands one at a time unless the underlying CLI behavior is verified safe for concurrent use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/2513483494/1123) <br>
- [Install TCCLI](references/install.md) <br>
- [Configure TCCLI credentials](references/auth.md) <br>
- [Tencent Cloud API reference lookup examples](references/refs.md) <br>
- [Tencent Cloud API service index](https://cloudcache.tencentcs.com/capi/refs/services.md) <br>
- [TencentCloud CLI source repository](https://github.com/TencentCloud/tencentcloud-cli.git) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON parameter examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide authenticated Tencent Cloud CLI commands that create, modify, or delete cloud resources.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
