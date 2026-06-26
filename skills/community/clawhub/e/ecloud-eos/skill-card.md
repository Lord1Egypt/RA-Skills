## Description: <br>
ecloud-eos helps an agent configure and manage China Mobile Cloud EOS object storage, including bucket and object operations, ACLs, signed URLs, and image processing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ecloud-eos](https://clawhub.ai/user/ecloud-eos) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to let an agent perform EOS storage administration tasks through bundled Node.js and setup scripts. It is suited for configuring credentials, managing buckets and objects, generating signed access links, and applying supported image-processing operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist long-lived EOS credentials in user-level or shell configuration. <br>
Mitigation: Use a dedicated least-privilege or temporary credential, avoid exposing secrets in chat, and remove persisted EOS_* variables when the work is complete. <br>
Risk: The skill can delete buckets or objects and can empty a bucket. <br>
Mitigation: Review destructive commands before execution, require explicit confirmation for bucket-emptying operations, and back up important data before deletion. <br>
Risk: The skill can change public access controls, referer policy, signed URL behavior, and image save-as writes. <br>
Mitigation: Prefer private ACLs, inspect public-read or public-read-write changes, validate signed URL expiry and referer rules, and confirm image save-as target buckets and keys before running. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ecloud-eos/ecloud-eos) <br>
- [Mobile Cloud EOS operation reference](references/api_reference.md) <br>
- [EOS image processing reference](references/image_process_reference.md) <br>
- [EOS configuration template](references/config_template.properties) <br>
- [China Mobile Cloud EOS product documentation](https://ecloud.10086.cn/op-help-center/doc/category/729) <br>
- [China Mobile Cloud credential creation](https://ecloud.10086.cn/op-help-center/doc/article/24501) <br>
- [China Mobile Cloud regions and endpoints](https://ecloud.10086.cn/op-help-center/doc/article/48082) <br>
- [China Mobile Cloud EOS API documentation](https://ecloud.10086.cn/op-help-center/doc/outline/56247) <br>
- [China Mobile Cloud image processing overview](https://ecloud.10086.cn/op-help-center/doc/article/95187) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, JSON, Files] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses EOS environment variables and can persist configuration through platform-specific setup scripts.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
