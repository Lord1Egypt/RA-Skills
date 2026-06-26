## Description: <br>
Alibaba Cloud Tablestore Agent Storage Skill for building and managing Tablestore-based knowledge bases with the tablestore-agent-storage Python SDK. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to configure Alibaba Cloud Tablestore Agent Storage, create or connect knowledge bases, import local or OSS documents, run retrieval, and set up directory synchronization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide high-impact Alibaba Cloud Tablestore or OSS mutations and scheduled synchronization. <br>
Mitigation: Require explicit user confirmation before instance creation or scheduled sync, and review every cloud mutation before execution. <br>
Risk: Generated configuration may contain sensitive Alibaba Cloud credentials or STS tokens. <br>
Mitigation: Avoid storing raw AK/SK or STS tokens in generated JSON; prefer the default credential chain or temporary credentials. <br>
Risk: Directory sync may upload unintended local files to OSS and import them into a knowledge base. <br>
Mitigation: Review the exact local directory, OSS path, and inclusion filters before enabling sync. <br>
Risk: Installer shortcuts such as curl-to-bash or sudo commands can expand local execution authority. <br>
Mitigation: Prefer verified manual CLI installation paths and inspect installation commands before running them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sdk-team/alibabacloud-tablestore-agent-storage) <br>
- [Credentials Configuration](references/credentials.md) <br>
- [RAM Permissions](references/ram-policies.md) <br>
- [Metadata Reference](references/metadata.md) <br>
- [Tablestore Instance Operations](references/tablestore-instance.md) <br>
- [Tablestore CLI Installation Guide](references/tablestore-cli-installation-guide.md) <br>
- [ossutil Installation Guide](references/ossutil-installation-guide.md) <br>
- [Alibaba Cloud CLI Installation Guide](references/aliyun-cli-installation-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JSON, Python, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create configuration and synchronization files under tablestore_agent_storage/ when used by an agent.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
