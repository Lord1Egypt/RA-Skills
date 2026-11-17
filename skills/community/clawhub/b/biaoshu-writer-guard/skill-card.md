## Description:

上传招标/投标文件，AI 一站式完成智能解读（废标红线/评分标准/控标洞察）、成品投标文件(.docx)生成、标书审查（分级风险+雷同检测）和标书查重（2-3份投标文件相似/雷同风险检查）。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chichihaixiaojian666](https://clawhub.ai/user/chichihaixiaojian666)

### License/Terms of Use:

MIT-0

## Use Case:

External procurement and bid teams use this skill to interpret tender documents, generate bid document drafts, review bid compliance risks, and compare bid files for similarity signals before submission.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tender and bid documents are sent to the 百炼标书 service and results are tied to the user's account.

Mitigation: Use only with documents the user is authorized to process, confirm upload consent before sensitive workflows, and disclose the service dependency before installation or use.

Risk: API-key handling can expose a full account credential if the key is pasted into chat or command arguments.

Mitigation: Have the user write the key directly into the skill-local config.json file, avoid echoing or requesting the key in conversation, and keep the config file permission-restricted.

Risk: Local metadata such as tender filenames and job identifiers may persist in the default project store.

Mitigation: Set a dedicated ZCM_HOME for sensitive workspaces when needed and review or remove local project metadata according to the user's retention requirements.

Risk: The skill includes strong response-control instructions and fixed referral/channel messaging that may be unsuitable for neutral or enterprise deployments.

Mitigation: Review the public-facing wording, referral links, and paid-operation prompts before adopting the skill in a managed environment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/chichihaixiaojian666/skills/biaoshu-writer-guard)
- [Publisher Profile](https://clawhub.ai/user/chichihaixiaojian666)
- [百炼标书 Platform](https://biaoshu.zhiliaobiaoxun.com/?ch=c666)
- [Open API Dispatch Reference](references/api.md)
- [Authentication, Jobs, and Entitlements Reference](references/api-auth.md)
- [Bid Interpretation and Generation Reference](references/api-bid-workflow.md)
- [Bid Compliance Review Reference](references/api-compliance.md)
- [Bid Similarity Check Reference](references/api-duplicate.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Chinese-language assistant responses, local report files, JSON results, and generated .docx bid documents from the connected service.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce HTML or Word reports for interpretation and compliance review; bid generation produces short-lived download links or local .docx files when requested.]

## Skill Version(s):

3.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
