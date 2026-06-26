## Description: <br>
Transform a workflow description into affordance tables showing UI and Code affordances with their wiring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[morpheis](https://clawhub.ai/user/morpheis) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, designers, and product teams use this skill to map how a workflow moves through UI and code affordances, or to design a new system from shaped parts. It produces tables that make places, controls, calls, data returns, and optional visualizations explicit. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Workflow descriptions, code, or architecture details shared for analysis may contain sensitive information. <br>
Mitigation: Share only code, workflows, and architecture details you are comfortable having the agent analyze. <br>
Risk: Generated affordance tables may be incomplete or misleading if they are not checked against the actual workflow or code. <br>
Mitigation: Review the tables against the source workflow or implementation before using them for design or implementation decisions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/morpheis/breadboarding) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown tables with optional Mermaid diagrams] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces Places, UI Affordances, Code Affordances, and Data Stores tables for the described workflow.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
