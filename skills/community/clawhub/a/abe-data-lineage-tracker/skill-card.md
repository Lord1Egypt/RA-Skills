## Description: <br>
Track data origin, transformations, and flow through construction systems. Essential for audit trails, compliance, and debugging data issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alvisdunlop](https://clawhub.ai/user/alvisdunlop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Construction project teams, data engineers, and analytics assistants use this skill to register data sources and entities, record transformations, trace upstream and downstream lineage, validate consistency, and prepare audit-friendly lineage reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional AI analysis can send construction lineage details to SkillBoss API Hub. <br>
Mitigation: Install only where that transfer is permitted, and avoid sending secrets or regulated data in lineage prompts. <br>
Risk: The skill requires a sensitive API credential. <br>
Mitigation: Use a dedicated SKILLBOSS_API_KEY and rotate or revoke it according to organizational policy. <br>
Risk: The skill requests filesystem access for project data processing. <br>
Mitigation: Scope filesystem access to the project files intended for lineage analysis. <br>


## Reference(s): <br>
- [Data Driven Construction homepage](https://datadrivenconstruction.io) <br>
- [SkillBoss API Hub endpoint](https://api.heybossai.com/v1/pilot) <br>
- [ClawHub skill listing](https://clawhub.ai/alvisdunlop/abe-data-lineage-tracker) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance] <br>
**Output Format:** [Markdown summaries with structured tables, JSON-style exports, Mermaid lineage diagrams, and Python code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can present lineage traces, impact analysis, validation findings, audit reports, and export guidance for CSV, Excel, or JSON.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata; artifact/claw.json lists 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
