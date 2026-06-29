## Description: <br>
Extract structured fields from documents with the EasyLink async extraction API, including universal extraction, flash extraction with bounding boxes, business license extraction, org-code certificate extraction, custom schemas, custom prompts, and polling until completion. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sycamore792](https://clawhub.ai/user/sycamore792) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to submit supported document files to EasyLink, poll asynchronous extraction tasks, and receive normalized structured field data. It supports open extraction, schema-constrained extraction, prompt-driven extraction, business license extraction, and org-code certificate extraction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected documents and extracted contents are sent to EasyLink for remote processing. <br>
Mitigation: Use the skill only with documents you are authorized to process, and avoid regulated, confidential, customer, financial, or identity documents unless EasyLink privacy, retention, and regional handling terms have been reviewed. <br>
Risk: Saved extraction results can contain sensitive document content. <br>
Mitigation: Save results only to secure locations with appropriate access controls. <br>
Risk: The helper supports a custom --base-url option that can redirect document uploads. <br>
Mitigation: Use --base-url only for destinations you fully trust. <br>


## Reference(s): <br>
- [EasyLink EasyDoc Extract API Reference](references/easydoc-extract-api.md) <br>
- [EasyLink API Platform](https://platform.easylink-ai.com) <br>
- [EasyLink EasyDoc Extract Endpoint](https://api.easylink-ai.com/v1/easydoc/extract) <br>
- [ClawHub Skill Page](https://clawhub.ai/sycamore792/easydoc-extract) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Markdown, Code, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and normalized JSON results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Normalized results include task_id, status, results, and raw API response; raw output is also supported.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
