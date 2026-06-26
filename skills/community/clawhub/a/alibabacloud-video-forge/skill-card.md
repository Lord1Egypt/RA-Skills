## Description: <br>
Alibabacloud Video Forge helps agents run Alibaba Cloud MPS workflows for video upload, media probing, snapshots, transcoding, content moderation, and downloads. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and media operations teams use this skill to standardize video assets on Alibaba Cloud by uploading source media, generating covers, transcoding to multiple resolutions, running content moderation, and collecting output links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use Alibaba Cloud credentials to process media, create or select MPS pipelines, and access OSS objects. <br>
Mitigation: Use least-privilege RAM policies, configure credentials through the Alibaba Cloud default credential chain, and avoid running the skill against sensitive media unless the environment is approved. <br>
Risk: OSS cleanup commands can delete objects recursively or with force options. <br>
Mitigation: Prefer dry-run cleanup first, review every delete target, and grant OSS delete permissions only when cleanup is required. <br>
Risk: Automatic pipeline selection can create or choose cloud resources without an explicitly reviewed pipeline ID. <br>
Mitigation: Prefer explicit pipeline IDs for controlled environments and review pipeline permissions before running production workflows. <br>
Risk: Environment loading can import cloud-related variables from local shell profiles. <br>
Mitigation: Use a dedicated shell profile or execution environment with only the variables required for this skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sdk-team/alibabacloud-video-forge) <br>
- [Capability Overview](references/capability-overview.md) <br>
- [Security Guidelines](references/security-guidelines.md) <br>
- [RAM Permission Policies](references/ram-policies.md) <br>
- [Script Parameters](references/params.md) <br>
- [Verification Method](references/verification-method.md) <br>
- [Aliyun CLI Installation Guide](references/cli-installation-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, configuration steps, and script output summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce cloud job identifiers, media metadata, moderation results, and OSS object links depending on the selected workflow.] <br>

## Skill Version(s): <br>
0.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
