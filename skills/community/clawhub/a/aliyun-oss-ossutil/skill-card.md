## Description: <br>
Use when installing, configuring, or operating Alibaba Cloud OSS from the command line with ossutil 2.0, based on the official ossutil overview. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to install, configure, and run Alibaba Cloud OSS ossutil 2.0 workflows for bucket listing, object transfer, sync, and resource management. It helps agents confirm region, endpoint, credentials, and operation scope before executing OSS commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing ossutil from a stale or incorrect download URL can fail or introduce supply-chain risk. <br>
Mitigation: Verify the ossutil download URL and checksum against Alibaba Cloud official documentation before installation. <br>
Risk: Long-lived or over-privileged Alibaba Cloud credentials can expose OSS resources if mishandled. <br>
Mitigation: Use least-privilege RAM credentials or temporary credentials, and prefer environment variables or shared credential files over passing secrets on the command line. <br>
Risk: Mutating commands such as sync --delete or ACL changes can remove data or alter access unintentionally. <br>
Mitigation: Confirm intent, region, endpoint, identifiers, and operation scope before mutating commands, and run a minimal read-only query first. <br>


## Reference(s): <br>
- [ClawHub Release Page](https://clawhub.ai/cinience/aliyun-oss-ossutil) <br>
- [OSSUTIL 2.0 Overview and Configuration](https://help.aliyun.com/zh/oss/developer-reference/ossutil-overview) <br>
- [ossutil 2.2.1 Linux AMD64 Download](https://gosspublic.alicdn.com/ossutil/v2/2.2.1/ossutil-2.2.1-linux-amd64.zip) <br>
- [ossutil 2.2.1 macOS AMD64 Download](https://gosspublic.alicdn.com/ossutil/v2/2.2.1/ossutil-2.2.1-darwin-amd64.zip) <br>
- [Install Reference](references/install.md) <br>
- [Source Reference List](references/sources.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions, Files] <br>
**Output Format:** [Markdown with inline bash code blocks and saved command evidence files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save command outputs, object listings, sync logs, and validation evidence under output/aliyun-oss-ossutil/.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
