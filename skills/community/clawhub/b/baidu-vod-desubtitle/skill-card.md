## Description: <br>
Baidu AI Cloud VOD Subtitle Erasure helps agents guide users through paid Baidu VOD subtitle, logo, and region erasure workflows for local or Baidu Netdisk videos. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lhx121619](https://clawhub.ai/user/lhx121619) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to collect video-processing parameters, confirm planned actions, and run Baidu VOD subtitle or region erasure jobs. It supports local files, Baidu Netdisk inputs, batch processing, task lookup, deletion, local downloads, and optional Netdisk upload. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected videos may be uploaded to Baidu VOD or transferred through Baidu Netdisk. <br>
Mitigation: Confirm that each selected video can be sent to Baidu services before running processing or transfer commands. <br>
Risk: The workflow uses Baidu cloud credentials from environment variables. <br>
Mitigation: Use scoped credentials where possible and review the command before exposing BAIDU_VOD_AK or BAIDU_VOD_SK in the session. <br>
Risk: Baidu VOD subtitle erasure is a paid service and may create usage charges. <br>
Mitigation: Review pricing and expected processing duration before confirming each job, especially batch jobs. <br>
Risk: Batch processing, deletion, and Netdisk upload options can affect multiple files or tasks. <br>
Mitigation: Require explicit user confirmation for the selected files, task IDs, deletion requests, and upload destinations before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lhx121619/skills/baidu-vod-desubtitle) <br>
- [Baidu VOD pricing reference](https://cloud.baidu.com/doc/VOD/s/Zmheig5gv) <br>
- [Baidu VOD product page](https://cloud.baidu.com/product/vod.html) <br>
- [Baidu VOD subtitle erasure API documentation](https://cloud.baidu.com/doc/VOD/s/fmhiy9vqk) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-provided Baidu VOD credentials; processing may upload videos to Baidu services and incur paid VOD charges.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence; artifact _meta.json reports 1.0.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
