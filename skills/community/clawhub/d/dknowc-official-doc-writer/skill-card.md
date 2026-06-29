## Description: <br>
Helps agents draft, revise, review, and generate Word-formatted Chinese official documents and formal organizational materials, using DeepKnow search for policy, data, standards, or case support when needed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dylanzhangzx](https://clawhub.ai/user/dylanzhangzx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to produce Chinese official-document drafts, reviews, and Word deliverables for notices, reports, requests, replies, meeting minutes, announcements, opinions, plans, summaries, management measures, briefing materials, and speeches. When source support is required, the skill guides agents through DeepKnow search, material classification, source review, and document generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: DeepKnow search requires an API key and may process user-provided task materials through the configured search service. <br>
Mitigation: Configure the API key only in the local config file and avoid confidential government or business materials unless the user's environment permits this processing. <br>
Risk: Drafts, search JSON, and generated Word files are stored locally under the skill workspace. <br>
Mitigation: Review local file-retention expectations before use and remove generated materials according to the user's data-handling policy. <br>
Risk: Official-document drafts can contain incorrect policy interpretation, unsupported data, or overconfident formal language. <br>
Mitigation: Use the included search policy, material usage guidance, and review checklist before final delivery, especially for policy-dependent, high-risk, or Word/red-head document workflows. <br>


## Reference(s): <br>
- [ClawHub skill release page](https://clawhub.ai/dylanzhangzx/skills/dknowc-official-doc-writer) <br>
- [README](README.md) <br>
- [Skill instructions](SKILL.md) <br>
- [Search policy](reference/search_policy.md) <br>
- [Task router](reference/task_router.md) <br>
- [Output guide](reference/output_guide.md) <br>
- [Review checklist](reference/review_checklist.md) <br>
- [Material usage guidance](reference/material_usage_guidance.md) <br>
- [DeepKnow ClawHub API key registration](https://platform.dknowc.cn/auth/#/register?channel=2787E171-B0E5-4328-9946-47AC52434D1F&type=6) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown or plain text drafts, Python shell commands, configuration guidance, search-result JSON, and .docx files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Word outputs are written under the skill workspace; long formal materials default to .docx delivery, with Markdown drafts used only as internal intermediates unless the user explicitly asks for draft text.] <br>

## Skill Version(s): <br>
3.0.20 (source: server release metadata, artifact _meta.json, and CHANGE_log.md released 2026-06-26) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
