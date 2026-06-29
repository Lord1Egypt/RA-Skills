## Description: <br>
深知写作助手 helps agents draft, revise, review, and format Chinese official documents and formal workplace materials, with optional 深知 search for policy, data, and case support and Word document delivery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dknownai](https://clawhub.ai/user/dknownai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and document-preparation teams use this skill to produce Chinese official documents, government-style materials, enterprise formal documents, meeting notices, reports, replies, summaries, plans, and Word-formatted deliverables. The skill is especially suited to workflows that require policy, data, or case support from 深知 search followed by review and formatted .docx output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Policy, data, and case searches send queries to the 深知 provider and require a configured API key. <br>
Mitigation: Configure the API key locally, avoid storing it in shared packages, and use the skill only when sending such queries to the provider is acceptable. <br>
Risk: Generated official or policy-sensitive documents may contain incorrect, incomplete, or unsupported claims. <br>
Mitigation: Review official documents before relying on them, use the included review checklist, and verify policy, data, and case support when search was used. <br>
Risk: Explicit output paths can write generated Word files to unintended locations. <br>
Mitigation: Use explicit output paths carefully and confirm generated file locations before sharing or relying on the document. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dknownai/dknownai-official-doc-writer) <br>
- [Artifact README](artifact/README.md) <br>
- [Search policy and material rules](artifact/reference/search_policy.md) <br>
- [Material usage guidance](artifact/reference/material_usage_guidance.md) <br>
- [Output formatting guide](artifact/reference/output_guide.md) <br>
- [Review checklist](artifact/reference/review_checklist.md) <br>
- [Document standards index](artifact/reference/standards/00_索引.md) <br>
- [深知可信搜索 API endpoint](https://open.dknowc.cn/dependable/search/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown or plain text guidance, shell commands, JSON search outputs, and .docx file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can generate ordinary Word documents by default and red-head Word documents only when explicitly requested.] <br>

## Skill Version(s): <br>
3.0.18 (source: server release and artifact changelog, released 2026-06-10) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
