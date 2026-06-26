## Description: <br>
Guides users through a scored AI operating-system audit covering persistent memory, skill architecture, agent routing, outputs, and integrations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[flynndavid](https://clawhub.ai/user/flynndavid) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, operators, and AI power users use this skill to audit their current AI workflow, identify weak layers, and produce a prioritized rebuild plan for memory, skills, routing, and integrations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill recommends connecting tools and outputs such as Slack, Notion, GitHub, and databases. <br>
Mitigation: Use least-privilege credentials, narrow channel/repository/database scopes, and require confirmation before external writes. <br>
Risk: The memory templates may encourage storing sensitive business context or personal data in persistent files. <br>
Mitigation: Keep secrets, regulated data, and confidential context out of memory files and public repositories. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/flynndavid/ai-os-blueprint) <br>
- [Artifact skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown guidance with scorecards, checklists, tables, and templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a self-assessment and prioritized implementation plan; no executable code is included.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
