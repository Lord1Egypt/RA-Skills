## Description:

上传招标/投标文件，AI 一站式完成智能解读（废标红线/评分标准/控标洞察）、成品投标文件(.docx)生成、标书审查（分级风险+雷同检测）和标书查重（2-3份投标文件相似/雷同风险检查）。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chichihaixiaojian666](https://clawhub.ai/user/chichihaixiaojian666)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to process procurement bid materials through the 百炼®标书 service: interpreting tender documents, generating finished .docx bid documents, reviewing bid compliance, and checking 2-3 bid files for similarity risks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Confidential bid and procurement documents are uploaded to the vendor service for processing.

Mitigation: Use only when the user is comfortable sending those files to the service and has confirmed authorization to process them.

Risk: The skill requires a paid API-key account for billed operations.

Mitigation: Have the user configure the API key locally and avoid entering or exposing API keys in chat or command-line arguments.

Risk: Tender filenames may be cached outside the declared generated-output area when the default ZCM_HOME is used.

Mitigation: Review local storage behavior before deployment and set ZCM_HOME to a controlled location when that metadata should be isolated.

Risk: Security evidence flags mandatory promotional or user-output behavior for review.

Mitigation: Review user-facing output requirements before enabling the skill in environments with strict communication or disclosure policies.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chichihaixiaojian666/skills/biaoshu-writer-studio)
- [Publisher profile](https://clawhub.ai/user/chichihaixiaojian666)
- [百炼®标书 platform](https://biaoshu.zhiliaobiaoxun.com/?ch=c666)
- [Open API overview](references/api.md)
- [Authentication, jobs, and account entitlements API](references/api-auth.md)
- [Tender interpretation and bid generation API](references/api-bid-workflow.md)
- [Bid compliance review API](references/api-compliance.md)
- [Bid duplicate check API](references/api-duplicate.md)
- [Knowledge base fields](references/knowledge-fields.md)
- [Usage guide](references/usage.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Conversational text plus generated report files, JSON summaries, short-lived download links, and .docx bid documents]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uploads user-provided procurement files to the vendor service; paid API-key account is required for bid generation, review, and duplicate checking.]

## Skill Version(s):

3.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
