## Description: <br>
支持自定义分支/代码库创建MR、查询MR合并状态、按代码库+环境关键字触发发布流水线，并自动推送通知。支持自然语言输入，由大模型自动识别意图。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[farb](https://clawhub.ai/user/farb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and release engineers use this skill to create and inspect Alibaba Cloud Yunxiao merge requests, trigger deployment pipelines by repository and environment, and send operation notifications to an approved webhook destination. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create merge requests and trigger deployment pipelines from broad natural-language prompts without a built-in confirmation step. <br>
Mitigation: Require human confirmation or allowlists before write actions such as merge request creation and deployment triggers. <br>
Risk: Misconfigured credentials or webhook destinations could expose repository or release activity. <br>
Mitigation: Use a least-privileged Yunxiao token and point the webhook only to an approved internal bot destination. <br>
Risk: Default repository, branch, and pipeline fallbacks may cause actions in unintended targets. <br>
Mitigation: Remove or constrain default write-action fallbacks before production use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/farb/ailiyun-yunxiao-mr-deploy) <br>
- [Publisher profile](https://clawhub.ai/user/farb) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, configuration, guidance] <br>
**Output Format:** [Plain text or Markdown status messages with configuration guidance and operation results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create merge requests, query merge request state, trigger deployment pipelines, and send webhook notifications when configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
