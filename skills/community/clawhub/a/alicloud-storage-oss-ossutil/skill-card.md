## Description: <br>
Alibaba Cloud OSS CLI (ossutil 2.0) skill. Install, configure, and operate OSS from the command line based on the official ossutil overview. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud engineers use this skill to install, configure, validate, and operate Alibaba Cloud OSS through ossutil workflows for listing, uploading, downloading, syncing, and storage management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing ossutil from Alibaba-hosted binaries can introduce supply-chain risk if the source or downloaded artifact is not trusted. <br>
Mitigation: Install only when the publisher and upstream source are trusted, prefer user-local installation, and verify official checksums or signatures when available. <br>
Risk: OSS operations can expose or modify cloud storage resources when credentials or command scope are too broad. <br>
Mitigation: Use least-privilege RAM credentials, confirm region and endpoint settings, run a minimal read-only query first, and review upload, sync, and delete commands before execution. <br>
Risk: Passing AccessKey credentials directly on command lines can leak secrets through shell history or process listings. <br>
Mitigation: Prefer environment variables, shared credentials files, or managed credential mechanisms instead of inline secret arguments. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/cinience/alicloud-storage-oss-ossutil) <br>
- [ossutil overview](https://help.aliyun.com/zh/oss/developer-reference/ossutil-overview) <br>
- [Official source list](references/sources.md) <br>
- [Install instructions](references/install.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown] <br>
**Output Format:** [Markdown with inline bash commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce validation reports, object listings, sync logs, and command evidence files under the configured output directory.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
