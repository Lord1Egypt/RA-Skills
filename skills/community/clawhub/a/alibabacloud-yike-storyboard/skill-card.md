## Description: <br>
Creates Yike storyboards from novels or scripts through a guided Alibaba Cloud CLI workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and creators use this skill to turn a novel or script into a Yike storyboard by confirming parameters, uploading the source file to Alibaba Cloud OSS, submitting a storyboard job, and tracking status until the storyboard editing link is available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow uploads the selected novel or script to Alibaba Cloud services and uses cloud credentials. <br>
Mitigation: Confirm the exact file path, Alibaba account, region, and storyboard settings before upload; use least-privileged RAM or short-lived STS credentials. <br>
Risk: Sensitive access keys may be exposed through command history, logs, or chat if handled carelessly. <br>
Mitigation: Do not print or paste AK/SK values; verify credential status with approved CLI checks and avoid sharing credentials in logs or conversation. <br>
Risk: Installer and CLI commands can affect the local environment or cloud resources. <br>
Mitigation: Review installer commands before running them and confirm that Alibaba Cloud ICE/Yike access and required RAM permissions are intended for the account. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/sdk-team/alibabacloud-yike-storyboard) <br>
- [Aliyun CLI installation guide](references/cli-installation-guide.md) <br>
- [RAM permission policies](references/ram-policies.md) <br>
- [Related CLI commands](references/related-commands.md) <br>
- [Verification method](references/verification-method.md) <br>
- [Acceptance criteria](references/acceptance-criteria.md) <br>
- [Alibaba Cloud ICE activation](https://ice.console.aliyun.com/guide/default) <br>
- [Yike platform](https://www.yikeai.com/#/home) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated service links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce Alibaba Cloud CLI commands, upload status, job status summaries, and Yike storyboard editing URLs.] <br>

## Skill Version(s): <br>
0.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
