## Description:

上传招标/投标文件，AI 一站式完成智能解读、成品投标文件生成、标书审查和标书查重，需用户提供百炼标书 API Key 并将文件交由百炼标书云端处理。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chichihaixiaojian666](https://clawhub.ai/user/chichihaixiaojian666)

### License/Terms of Use:

MIT-0

## Use Case:

External users and procurement teams use this skill to analyze tender documents, generate bid documents, review bid compliance, and compare bid files for similarity risk. It is intended for authorized local tender or bid files and uses a third-party cloud service for processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tender and bid files are uploaded to a third-party cloud service and may contain commercial, pricing, or personal information.

Mitigation: Use the skill only with documents the user is authorized to process, and confirm consent before upload.

Risk: The skill uses an API key for a paid account and some operations can consume account balance.

Mitigation: Keep the API key out of chat, store it only in the local config file, and review billing expectations before chargeable operations.

Risk: Persistent project metadata may be written to ~/.zcm/projects.json outside the declared skill output directory.

Mitigation: Set ZCM_HOME to a controlled location before use or remove the metadata file after processing when retention is not desired.

Risk: The security verdict is suspicious because the skill includes mandatory referral-style output rules.

Mitigation: Review user-facing prompts and installation guidance before deployment to ensure they match the intended trust and disclosure posture.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chichihaixiaojian666/skills/biaoshu-writer-craft)
- [Publisher profile](https://clawhub.ai/user/chichihaixiaojian666)
- [百炼标书 service](https://biaoshu.zhiliaobiaoxun.com/?ch=c666)
- [API overview](artifact/references/api.md)
- [Usage guide](artifact/references/usage.md)
- [Bid workflow API](artifact/references/api-bid-workflow.md)
- [Compliance review API](artifact/references/api-compliance.md)
- [Duplicate check API](artifact/references/api-duplicate.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, generated document files, HTML or Word reports, JSON results, and short-lived download links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include cloud-processed bid or tender analysis, generated .docx bid files, compliance reports, duplicate-check results, local report paths, and account billing status.]

## Skill Version(s):

3.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
