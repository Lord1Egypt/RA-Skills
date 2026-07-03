## Description: <br>
深知写作助手 helps agents draft, revise, review, and generate Word-format official Chinese documents such as notices, reports, requests, replies, meeting minutes, announcements, opinions, plans, summaries, management measures, briefing materials, and speeches. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dknownai](https://clawhub.ai/user/dknownai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and agent operators use this skill to prepare formal Chinese government, public-sector, and enterprise documents. It can plan searches for policy, data, standards, or case material, review document quality, and generate ordinary or red-header Word files when a formal deliverable is needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries and search parameters may be sent to the disclosed DKAG endpoint. <br>
Mitigation: Confirm the user is comfortable with the external search call before use, avoid confidential draft text or sensitive internal details in queries, and use the documented config.ini API-key setup. <br>
Risk: Generated official documents may contain incorrect, incomplete, or unsuitable policy, data, or formatting content. <br>
Mitigation: Apply the skill's review checklist and require user review before relying on generated Word files for formal use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dknownai/skills/dknownai-official-doc-writer) <br>
- [Artifact README](artifact/README.md) <br>
- [Search policy](artifact/reference/search_policy.md) <br>
- [Material usage guidance](artifact/reference/material_usage_guidance.md) <br>
- [Output guide](artifact/reference/output_guide.md) <br>
- [Review checklist](artifact/reference/review_checklist.md) <br>
- [DKAG search endpoint](https://open.dknowc.cn/dependable/search/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration guidance] <br>
**Output Format:** [Chinese prose, Markdown-formatted source text, generated .docx files, shell commands, and concise review or configuration guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use an external DKAG search endpoint for policy, data, standards, or case material when the user confirms the search plan and configures an API key.] <br>

## Skill Version(s): <br>
3.0.20 (source: server release metadata, artifact/_meta.json, artifact/README.md, and artifact/CHANGE_log.md released 2026-06-26) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
