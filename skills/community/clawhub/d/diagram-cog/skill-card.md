## Description: <br>
Diagram Cog uses CellCog to generate flowcharts, architecture diagrams, mind maps, org charts, ER diagrams, sequence diagrams, Gantt charts, and network diagrams from plain-English prompts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nitishgargiitd](https://clawhub.ai/user/nitishgargiitd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, product teams, and business users use this skill to turn plain-English descriptions of systems, processes, data models, organizations, timelines, and user journeys into interactive diagrams or print-ready PDFs through CellCog. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Diagram prompts and generated diagram content are sent to CellCog and may include sensitive architecture, customer, or business information. <br>
Mitigation: Do not include secrets, credentials, regulated data, confidential internal architecture, or customer data unless the organization has approved CellCog for that use. <br>
Risk: Generated diagrams may be shared through interactive URLs or PDFs with privacy implications. <br>
Mitigation: Review sharing settings and treat generated URLs and exported files according to the organization's data-handling requirements. <br>


## Reference(s): <br>
- [Diagram Cog on ClawHub](https://clawhub.ai/nitishgargiitd/diagram-cog) <br>
- [CellCog Homepage](https://cellcog.ai) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, configuration, markdown] <br>
**Output Format:** [Markdown guidance with Python SDK examples and setup commands; generated diagram work is returned through CellCog as interactive HTML URLs or PDFs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, the cellcog dependency, and CELLCOG_API_KEY; supports OpenClaw fire-and-forget usage and blocking usage for other agents.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
