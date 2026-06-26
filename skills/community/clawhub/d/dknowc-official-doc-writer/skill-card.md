## Description: <br>
Assists agents with drafting, revising, reviewing, and generating Word-format Chinese official documents and formal business or government materials, using DKnowC search when policy, data, standards, or case evidence is needed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dylanzhangzx](https://clawhub.ai/user/dylanzhangzx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers use this skill to produce formal Chinese notices, reports, requests, replies, meeting minutes, announcements, opinions, plans, summaries, management measures, briefing materials, speeches, and related official documents. It supports search-backed materials gathering, document review, and final Word delivery for normal or red-head document workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search-backed tasks may send sensitive policy, personnel, business, or government-related query details to DKnowC as an external search provider. <br>
Mitigation: Use the search feature only when organizational policy permits the query contents to be shared with that provider; avoid confidential details in search terms. <br>
Risk: API keys can be exposed if passed in commands, pasted into prompts, or shared with generated files. <br>
Mitigation: Configure the key locally in config.ini and avoid placing credentials in command-line arguments, generated documents, or shared artifacts. <br>
Risk: Formal documents may contain incorrect policy references, data, conclusions, or commitments if generated without sufficient review. <br>
Mitigation: Apply the bundled review checklist and require human confirmation of policy basis, factual accuracy, organizational authority, and final wording before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dylanzhangzx/skills/dknowc-official-doc-writer) <br>
- [README](artifact/README.md) <br>
- [Search policy](artifact/reference/search_policy.md) <br>
- [Material usage guidance](artifact/reference/material_usage_guidance.md) <br>
- [Output guide](artifact/reference/output_guide.md) <br>
- [Review checklist](artifact/reference/review_checklist.md) <br>
- [Task router](artifact/reference/task_router.md) <br>
- [Document standards index](artifact/reference/standards/00_索引.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Formal Chinese document text or constrained Markdown for Word generation, with .docx files produced by bundled scripts when requested.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require a locally configured DKnowC API key for search-backed policy, data, standard, or case materials.] <br>

## Skill Version(s): <br>
3.0.19 (source: evidence.release.version, _meta.json, CHANGE_log.md, released 2026-06-25) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
