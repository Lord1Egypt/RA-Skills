## Description: <br>
Use when users need command-line operations on Alibaba Cloud resources, credential and profile setup, region or endpoint selection, or API discovery from the aliyun CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operators use this skill to manage Alibaba Cloud resources through the official aliyun CLI, including read-only discovery and bounded create, update, or delete operations. It also guides credential configuration, profile selection, regional endpoints, and troubleshooting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled version guard can download and replace the local aliyun executable from the latest official package. <br>
Mitigation: Prefer installing the Alibaba Cloud CLI from verified official instructions, or review the installer behavior and target path before allowing automatic updates. <br>
Risk: The skill can use powerful Alibaba Cloud credentials for create, update, or delete operations, and saved outputs may include cloud resource details. <br>
Mitigation: Use a dedicated least-privilege profile, verify connectivity with read-only queries first, review mutating commands before execution, and protect or clean generated output files. <br>


## Reference(s): <br>
- [Alibaba Cloud CLI documentation hub](https://help.aliyun.com/zh/cli) <br>
- [Install Alibaba Cloud CLI on Linux](https://help.aliyun.com/zh/cli/install-cli-on-linux) <br>
- [Configure credentials for Alibaba Cloud CLI](https://help.aliyun.com/zh/cli/configure-credentials) <br>
- [Alibaba Cloud OpenAPI Explorer](https://api.aliyun.com) <br>
- [Release page](https://clawhub.ai/cinience/aliyun-cli-manage) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and CLI output summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save CLI version checks, API outputs, and error logs under output/aliyun-cli-manage.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
