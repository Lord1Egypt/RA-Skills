## Description: <br>
Structure an OpenClaw agent's memory like a computer, using a cache hierarchy, a YAML fact store for directly addressable data, a lookup index for fast retrieval, and prose files only for narrative and behavioral context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kimmi2ue](https://clawhub.ai/user/kimmi2ue) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to restructure OpenClaw long-term memory, migrate prose-only memory into structured storage, reduce token usage, and improve retrieval of facts and project context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Migration can overwrite or misplace existing long-term memory content. <br>
Mitigation: Back up current memory files before migration and review proposed MEMORY.md, facts.yaml, and lookup-index.md changes before accepting them. <br>
Risk: Structured memory can retain secrets or sensitive personal details if they are copied into facts.yaml. <br>
Mitigation: Avoid storing secrets or sensitive personal data unless intentional, and review facts.yaml before committing or sharing memory files. <br>


## Reference(s): <br>
- [facts-yaml-template.md](references/facts-yaml-template.md) <br>
- [lookup-index-template.md](references/lookup-index-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, configuration] <br>
**Output Format:** [Markdown guidance with YAML and Markdown templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces proposed memory structure, migration steps, and template content for local memory files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
