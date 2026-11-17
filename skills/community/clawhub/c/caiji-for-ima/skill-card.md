## Description:

教发老兵实测沉淀的 IMA 知识库补料流水线：按主题检索搜狗微信文章、筛选编码、分批导入 IMA 知识库，并在用户明确要求时为指定知识库文件夹批量补充文章素材。

This skill is ready for commercial/non-commercial use.

## Publisher:

[byrdsongstratakoslb663-ctrl](https://clawhub.ai/user/byrdsongstratakoslb663-ctrl)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to collect public WeChat article candidates for a topic, filter and batch the URLs, and import them into a selected IMA knowledge-base folder. It is intended for deliberate knowledge-base enrichment workflows where the user confirms the target knowledge base, folder, and volume before import.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill imports public article URLs into a chosen IMA knowledge-base folder, so selecting the wrong knowledge base or folder could place content in the wrong location.

Mitigation: Confirm the exact knowledge base and folder before import, and byte-check the folder ID before starting batched imports.

Risk: Search results may include noisy items such as advertisements or Sogou verification pages, and the referenced IMA interface has no delete API.

Mitigation: Review generated batches when practical, use the documented filters, and prepare a manual cleanup list for any imported noise.

Risk: High-frequency use of Sogou WeChat search may trigger rate limiting or verification pages.

Mitigation: Keep keyword volume and page counts within the documented limits, respect cooldown behavior, and stop when verification pages appear.

## Reference(s):

- [IMA MCP 工具签名与 ID 基线](references/ima_kb_api.md)
- [检索与效率复盘](references/pitfalls.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command snippets and generated JSON and Markdown files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces topic-filtered article candidates, encoded URL batches, wave files for parallel import, and import reports; imports are designed to be idempotent.]

## Skill Version(s):

1.0.8 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
