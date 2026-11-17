## Description:

Helps agents configure credentials and upload, download, manage, delete, share, and process files in China Mobile Cloud EOS object storage using bundled Node.js scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ecloud-eos](https://clawhub.ai/user/ecloud-eos)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and external users can use this skill through an agent to configure China Mobile Cloud EOS access, manage buckets and objects, generate signed sharing URLs, and perform supported image-processing operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for EOS credentials and can persist them in the user environment.

Mitigation: Use least-privilege, short-lived credentials when possible, avoid sharing secrets in conversation, and review shell profile or user environment changes after setup.

Risk: The skill includes powerful bucket, object deletion, ACL, policy, and public-access operations.

Mitigation: Review target bucket and object keys before execution, keep destructive actions behind explicit confirmation, and avoid public-read-write ACLs.

Risk: Incorrect or untrusted endpoints could expose credentials or send operations to the wrong service.

Mitigation: Verify that the endpoint is the official EOS HTTPS endpoint for the selected region before configuring or running operations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ecloud-eos/skills/ecloud-eos)
- [Publisher profile](https://clawhub.ai/user/ecloud-eos)
- [EOS API operation reference](references/api_reference.md)
- [EOS image processing reference](references/image_process_reference.md)
- [EOS configuration template](references/config_template.properties)
- [China Mobile Cloud EOS product documentation](https://ecloud.10086.cn/op-help-center/doc/outline/56247)
- [China Mobile Cloud credential setup](https://ecloud.10086.cn/op-help-center/doc/article/24501)
- [China Mobile Cloud EOS regions and endpoints](https://ecloud.10086.cn/op-help-center/doc/article/48082)
- [China Mobile Cloud EOS image processing overview](https://ecloud.10086.cn/op-help-center/doc/article/95187)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands; invoked scripts return JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires EOS credentials and region, bucket, and endpoint configuration; setup scripts may persist environment variables for future sessions.]

## Skill Version(s):

1.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
