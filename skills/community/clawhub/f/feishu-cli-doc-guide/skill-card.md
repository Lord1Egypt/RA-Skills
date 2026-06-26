## Description: <br>
A reference guide for checking Feishu-compatible Markdown before document import, covering Mermaid and PlantUML limits, table splitting, callouts, formulas, images, API limits, and fallback behavior. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[GISwilson](https://clawhub.ai/user/GISwilson) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill as a preflight guide when generating Markdown that will be imported into Feishu documents, especially content with diagrams, tables, callouts, formulas, and images. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The guide can shape generated Feishu documents, so incorrect or stale compatibility guidance could cause import failures or degraded document output. <br>
Mitigation: Review generated Markdown against the guide's checklist before importing and verify high-risk diagrams, large tables, formulas, and images in Feishu. <br>
Risk: The reviewed package does not include any optional local style-guide file an agent may choose to consult. <br>
Mitigation: Inspect any separate local style-guide reference before relying on it for document generation. <br>


## Reference(s): <br>
- [Feishu Mermaid Board Syntax Reference](references/mermaid-spec.md) <br>
- [ClawHub skill page](https://clawhub.ai/GISwilson/feishu-cli-doc-guide) <br>
- [Publisher profile](https://clawhub.ai/user/GISwilson) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Configuration instructions] <br>
**Output Format:** [Markdown guidance with checklists, compatibility rules, and syntax examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only reference guidance; no executable code or credential handling in the reviewed artifact.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
