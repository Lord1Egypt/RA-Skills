## Description: <br>
Researches how people are using an AI tool (Claude Desktop, Cursor, OpenAI Codex, Google Gemini, or OpenClaw) and generates a Productivity Playbook plus a Skills Catalog in a consistent, rated, month-over-month format. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nazmul87-wq](https://clawhub.ai/user/nazmul87-wq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, researchers, and productivity-focused users use this skill to run recurring research on Claude Desktop, Cursor, OpenAI Codex, Google Gemini, or OpenClaw and generate dated Markdown playbooks and skill catalogs. It is suited for month-over-month ecosystem tracking, persona-specific workflow discovery, and rated recommendations for skills, extensions, plugins, rules, and MCP servers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill performs web research and can create or update Markdown reports, so generated recommendations may include outdated, incorrect, or low-quality third-party install guidance. <br>
Mitigation: Review generated reports, verify source links, and inspect third-party install recommendations before acting on them. <br>
Risk: Existing reports can be rewritten unless append mode is selected. <br>
Mitigation: Choose a specific output directory, use append-appendix mode when preserving existing report bodies matters, and keep outputs under version control. <br>
Risk: Search rate limits or limited host web access can reduce coverage and confidence. <br>
Mitigation: Require the run output to state missed coverage or downgraded confidence, and rerun with narrower tool scope or additional provided sources when needed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/nazmul87-wq/ai-tool-research) <br>
- [Agent Skills open standard](https://agentskills.io) <br>
- [README](artifact/README.md) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Productivity Playbook template](artifact/playbook-template.md) <br>
- [Skills Catalog template](artifact/catalog-template.md) <br>
- [Rating system](artifact/rating-system.md) <br>
- [Personas](artifact/personas.md) <br>
- [Research queries](artifact/research-queries.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown files with dated headers, rating tables, source links, and a Markdown run-log entry] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates one Productivity Playbook and one Skills Catalog per selected tool; all-tools mode can generate ten Markdown files plus research-log.md.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
