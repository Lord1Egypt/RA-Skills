## Description: <br>
Converts traditional job description documents into structured, deployable Markdown system prompts for AI Agents using Chudaxia's seven-layer digital employee template. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charleschor](https://clawhub.ai/user/charleschor) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, operators, and agent builders use this skill to transform role descriptions into consistent AI Agent system prompts with identity, persona, capability, knowledge, workflow, compliance, and KPI layers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated role prompts may contain inferred responsibilities, permissions, or compliance limits that do not match the source job description. <br>
Mitigation: Review generated prompts before deployment, with special attention to duties, authority boundaries, KPI definitions, and compliance constraints. <br>
Risk: The skill searches a user-selected knowledge base for job descriptions, which may expose or reuse internal information if the source is not approved. <br>
Mitigation: Confirm the permitted knowledge base before use and remove sensitive internal details from reusable prompts. <br>


## Reference(s): <br>
- [Chudaxia Ai Coach Tools Position Agent Prompts Generator on ClawHub](https://clawhub.ai/charleschor/chudaxia-ai-coach-position-prompts-generator) <br>
- [Seven-layer template reference](references/seven-layer-template.md) <br>
- [Quality checklist](references/quality-checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a complete seven-layer prompt document and may include a Markdown quality self-check when needed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
