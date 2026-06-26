## Description: <br>
将较长内容拆分为多个飞书文档 Blocks 后逐块写入，以减少长文本、表格或 Mermaid 图表导致空白文档的风险。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[icesumer-lgtm](https://clawhub.ai/user/icesumer-lgtm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users who create Feishu documents from agent conversation content can use this skill to split long Markdown, Mermaid diagrams, tables, and code blocks into smaller document blocks before writing. It is intended for Feishu document creation workflows where avoiding blank documents from oversized writes matters. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad automatic triggers may write conversation content to Feishu without clear per-action approval. <br>
Mitigation: Require explicit user confirmation before every create or append action, and verify the Feishu account, destination folder, assignee, and sharing settings before writing. <br>
Risk: The referenced block-writer.py script is not included in the release artifact reviewed here. <br>
Mitigation: Review the actual script source before relying on it, and keep dry-run or preview checks in place until the write path is verified. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/icesumer-lgtm/feishu-doc-block-writer-safe) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with bash and JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide creation or appending of Feishu document blocks and return a document link when the Feishu tooling is configured.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
