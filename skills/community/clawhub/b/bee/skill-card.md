## Description: <br>
Bee automates a Douyin video workflow by downloading watermark-free videos, uploading them to Alibaba Cloud OSS, and writing metadata to Feishu Bitable. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jerryxn](https://clawhub.ai/user/jerryxn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content operations teams use Bee to process Douyin links into downloaded video files, Alibaba OSS objects, and Feishu Bitable records for follow-up production workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow sends Douyin video content and metadata to a configured Alibaba OSS bucket and Feishu Bitable. <br>
Mitigation: Confirm bucket, table, visibility, and retention settings before use, and test with --dry-run or skip flags. <br>
Risk: The workflow requires cloud and Feishu credentials. <br>
Mitigation: Use dedicated least-privilege credentials and provide them through environment variables rather than committing secrets. <br>
Risk: The workflow depends on separate download and upload skills plus local node, python3, and curl tools. <br>
Mitigation: Install and review the dependent skills and verify required tools before running the full workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jerryxn/bee) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with bash command examples and a shell script workflow] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Douyin URL and configured Alibaba OSS and Feishu credentials; supports dry-run and skip flags.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
