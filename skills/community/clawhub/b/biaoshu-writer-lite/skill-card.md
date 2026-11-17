## Description:

Helps users analyze tender documents, generate bid documents, review bid compliance, and compare bid files for similarity using the 百炼®标书 cloud service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chichihaixiaojian666](https://clawhub.ai/user/chichihaixiaojian666)

### License/Terms of Use:

MIT-0

## Use Case:

External bidding teams and proposal writers use this skill to process tender and bid documents for bid/no-bid analysis, bid document drafting, compliance review, and similarity checking. It is intended for users who can authorize upload of those documents to the 百炼®标书 service and manage the associated account billing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tender and bid documents may contain sensitive commercial, pricing, or personal information and are uploaded to biaoshu.zhiliaobiaoxun.com for processing.

Mitigation: Confirm the user is comfortable sending the documents to that service before upload, and avoid using the skill for files that cannot be shared with the service.

Risk: The skill stores an account API key in the skill directory.

Mitigation: Have the user create the local config file with restrictive permissions, never ask for or echo the API key in chat, and rotate the key if exposure is suspected.

Risk: Bid generation, review, and duplicate checking can consume paid platform word credits.

Mitigation: Confirm paid actions, package selections, and page counts before submission, and present cost estimates as non-binding because final billing is determined by the platform.

Risk: Security evidence flags channel-tagged platform links and weak API-key redirect safeguards.

Mitigation: Treat ?ch=c666 links as channel-tagged platform links, do not forward credential-bearing bind or recharge redirects, and use ordinary platform account pages for billing actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chichihaixiaojian666/skills/biaoshu-writer-lite)
- [百炼®标书开放 API 总调度](references/api.md)
- [鉴权、任务与可用字数接口](references/api-auth.md)
- [智能解读与标书制作 API](references/api-bid-workflow.md)
- [标书审查 API](references/api-compliance.md)
- [标书查重 API](references/api-duplicate.md)
- [执行细节](references/usage.md)
- [知识库字段说明](references/knowledge-fields.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown/plain text guidance, JSON summaries, HTML or DOCX reports, and DOCX bid documents]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-provided local files and a skill-local API key; paid generation, review, and duplicate-check actions consume platform word credits.]

## Skill Version(s):

3.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
