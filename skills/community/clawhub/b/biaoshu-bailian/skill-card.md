## Description:

百炼标书智能写作工具 helps users process tender and bid files through the 百炼标书 cloud service to interpret tender requirements, generate bid documents, review bid compliance, and compare 2-3 bid files for similarity risk.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chichihaixiaojian666](https://clawhub.ai/user/chichihaixiaojian666)

### License/Terms of Use:

MIT-0

## Use Case:

External bidding, procurement, and proposal teams use this skill to analyze tender files, produce draft bid documents, review submission risks, and check similarity across legally held bid files before submission.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tender and bid files may contain confidential commercial, pricing, or personal information and are uploaded to the 百炼标书 service.

Mitigation: Use the skill only when the user is authorized to upload those files and accepts service-side processing and retention.

Risk: The skill uses a full-account API key for 百炼标书 operations.

Mitigation: Keep the key in the local skill config file with restrictive permissions, never paste it into chat, and reset it if exposure is suspected.

Risk: Generated reports or bid documents may be written outside a tightly controlled location when arbitrary output paths or basenames are used.

Mitigation: Prefer a dedicated output folder and avoid user-controlled report basenames or arbitrary save paths.

Risk: Tender and job metadata may persist locally across sessions.

Mitigation: Clear ~/.zcm/projects.json if persistent local tender or job metadata is not desired.

Risk: Bid generation, compliance review, and duplicate checking may consume the user's word balance.

Mitigation: Confirm paid operations before running them and monitor the account balance returned by the service.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chichihaixiaojian666/skills/biaoshu-bailian)
- [百炼标书 service](https://biaoshu.zhiliaobiaoxun.com/?ch=c666)
- [百炼标书开放 API 总调度](references/api.md)
- [鉴权、任务与可用字数接口](references/api-auth.md)
- [智能解读与标书制作 API](references/api-bid-workflow.md)
- [标书审查 API](references/api-compliance.md)
- [标书查重 API](references/api-duplicate.md)
- [执行细节](references/usage.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Text guidance, JSON summaries, HTML or Word reports, short-lived download links, and .docx bid documents.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Paid generation, review, and duplicate-check tasks consume the user's 百炼标书 word balance; generated files and task results may be retained by the service for about 7 days.]

## Skill Version(s):

1.0.17 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
