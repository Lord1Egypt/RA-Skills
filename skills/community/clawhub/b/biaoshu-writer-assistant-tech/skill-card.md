## Description:

上传招标/投标文件，AI 一站式完成智能解读、成品投标文件 .docx 生成、标书审查和标书查重，并通过百炼标书云端服务处理相关任务。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chichihaixiaojian666](https://clawhub.ai/user/chichihaixiaojian666)

### License/Terms of Use:

MIT-0

## Use Case:

External users and bidding teams use this skill to interpret tender documents, generate technical bid documents, review bid compliance risks, and compare bid files for similarity or duplicate-risk signals. It is intended for users who have authorization to upload the relevant tender and bid files to the vendor cloud service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tender and bid documents may contain commercial, pricing, or personal information and are sent to the vendor cloud service.

Mitigation: Use only files the user is authorized to upload, disclose cloud processing before first upload, and review retention expectations before use.

Risk: The API key is tied to billing and can authorize paid bid-generation, review, or duplicate-checking tasks.

Mitigation: Keep the API key out of chat and logs, store it only in the local skill configuration file, and reset it from the vendor platform if exposed.

Risk: Local output paths and unusual basenames can broaden where generated artifacts are written.

Mitigation: Prefer the default output directory and avoid user-supplied absolute output paths or unusual file basenames unless explicitly required.

Risk: Local project metadata may persist after use.

Mitigation: Periodically review and remove ~/.zcm/projects.json if the skill is installed and project history should not remain on the machine.

Risk: Generated bid documents, compliance findings, and duplicate-risk results may be incomplete or require professional judgment.

Mitigation: Manually review all generated documents, risk findings, and reports before bid submission or business decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chichihaixiaojian666/skills/biaoshu-writer-assistant-tech)
- [Publisher profile](https://clawhub.ai/user/chichihaixiaojian666)
- [百炼标书 platform](https://biaoshu.zhiliaobiaoxun.com/?ch=c666)
- [API overview](references/api.md)
- [Authentication, jobs, and word entitlement API](references/api-auth.md)
- [Interpretation and bid-document workflow API](references/api-bid-workflow.md)
- [Compliance review API](references/api-compliance.md)
- [Duplicate-risk API](references/api-duplicate.md)
- [Usage guide](references/usage.md)
- [Knowledge fields](references/knowledge-fields.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Plain text or Markdown guidance, JSON summaries, HTML or Word reports, and generated .docx bid documents]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated bid documents and reports may rely on cloud task status, short-lived download links, and user account word entitlements.]

## Skill Version(s):

3.1.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
