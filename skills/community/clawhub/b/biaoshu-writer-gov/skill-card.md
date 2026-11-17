## Description:

上传招标/投标文件，AI 一站式完成智能解读、成品投标文件生成、标书审查和标书查重。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chichihaixiaojian666](https://clawhub.ai/user/chichihaixiaojian666)

### License/Terms of Use:

MIT-0

## Use Case:

External users and bidding teams use this skill to analyze tender files, generate Word bid documents, review bid compliance risks, and compare bid documents for similarity or duplicate-risk signals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Confidential tender and bid files are uploaded to the vendor server for processing.

Mitigation: Use only files the user is authorized to disclose and confirm consent before upload.

Risk: Paid operations use the user's API-key account and available word balance.

Mitigation: Explain which operations may consume word balance before starting bid generation, review, or duplicate checks.

Risk: The security summary reports local project metadata storage outside the declared write area unless configured otherwise.

Mitigation: Review local storage behavior before installation and configure the output/storage location when needed.

Risk: The security guidance flags channel-tagged platform links and prescriptive assistant-output behavior.

Mitigation: Review the skill prompts and links before deployment, especially in managed or enterprise environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chichihaixiaojian666/skills/biaoshu-writer-gov)
- [百炼标书 platform](https://biaoshu.zhiliaobiaoxun.com/?ch=c666)
- [API dispatcher](references/api.md)
- [Authentication, jobs, and word entitlements](references/api-auth.md)
- [Tender interpretation and bid generation workflow](references/api-bid-workflow.md)
- [Bid compliance review API](references/api-compliance.md)
- [Bid duplicate-check API](references/api-duplicate.md)
- [Knowledge-base fields](references/knowledge-fields.md)
- [Usage guide](references/usage.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown responses plus generated reports, JSON results, and .docx bid-document files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May upload user-provided tender and bid files to the vendor service; generated task results and documents are time-limited on the platform.]

## Skill Version(s):

3.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
