## Description: <br>
Collects AI skills relevant to an agent business type from SkillHub in real time and exports them as an Excel inventory, with interactive data-source selection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shmiss](https://clawhub.ai/user/shmiss) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to discover public skills relevant to business agent categories such as HR, sales, customer service, data analysis, finance, IT, marketing, legal, content, and travel. It exports a deduplicated Excel inventory with descriptions, relevance labels, categories, install guidance or URLs, tags, stars, downloads, and versions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The script performs live network searches and results can change or be rate limited. <br>
Mitigation: Run it against public catalog data, allow for retry or review time, and validate exported rows before relying on them. <br>
Risk: Public skill description snippets may be sent to MyMemory for translation. <br>
Mitigation: Avoid private or proprietary catalog data, or disable or replace translation before use. <br>
Risk: Python dependencies are listed without pinned versions. <br>
Mitigation: Pin dependencies to known patched versions before production or controlled-environment use. <br>


## Reference(s): <br>
- [Agent Skills Collector on ClawHub](https://clawhub.ai/shmiss/agent-skills-collector) <br>
- [ClawHub mirror API](https://cn.clawhub-mirror.com/api/v1) <br>
- [SkillHub skill pages](https://skillhub.tencent.com/skill/{slug}) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Text, Shell commands] <br>
**Output Format:** [Excel workbook (.xlsx) plus terminal status text and install guidance or skill URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Rows include skill name, relevance, category, description, install command or URL, tags, stars, downloads, and version.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
