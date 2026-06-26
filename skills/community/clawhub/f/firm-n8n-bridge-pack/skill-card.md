## Description: <br>
n8n workflow bridge pack for exporting OpenClaw pipelines to n8n format and importing n8n workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[romainsantoli-web](https://clawhub.ai/user/romainsantoli-web) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to bridge OpenClaw workflows with n8n by exporting OpenClaw pipelines to n8n JSON and importing n8n workflows with validation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Imported n8n workflow JSON can contain secrets, unexpected automation steps, or changes that affect OpenClaw workflows. <br>
Mitigation: Review workflow JSON before import and confirm the workflow content matches the intended automation. <br>
Risk: The skill depends on mcp-openclaw-extensions >= 3.0.0. <br>
Mitigation: Review and approve the referenced dependency before installing or running the bridge tools. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/romainsantoli-web/firm-n8n-bridge-pack) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Configuration, Guidance] <br>
**Output Format:** [n8n workflow JSON, OpenClaw configuration references, and concise import/export status or validation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May operate on local OpenClaw configuration paths and n8n workflow JSON files.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
