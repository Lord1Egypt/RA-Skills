## Description: <br>
Discovers GCP-hosted AI agent and MCP-relevant assets from the operator's environment, emits canonical agent-bom inventory JSON, and can scan it without giving agent-bom long-lived GCP credentials. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[msaad00](https://clawhub.ai/user/msaad00) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud security engineers use this skill to inventory Vertex AI, Cloud Run, Cloud Functions, GKE, and related GCP agent infrastructure with local read-only credentials. It helps produce schema-valid agent-bom inventory and optional findings while keeping credential material out of generated outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use the operator's local GCP authentication context for cloud inventory. <br>
Mitigation: Use least-privilege read-only credentials such as a scoped service account or workload identity, and confirm the target project before running discovery. <br>
Risk: Generated inventory may contain sensitive details about cloud resources, permissions, or agent infrastructure. <br>
Mitigation: Review the inventory JSON and confirm credential-like values are redacted before sharing or scanning it further. <br>
Risk: Discovery contacts authenticated Google Cloud APIs and writes output to a local path. <br>
Mitigation: Run only for operator-approved projects and confirm the output path before execution. <br>


## Reference(s): <br>
- [agent-bom repository](https://github.com/msaad00/agent-bom) <br>
- [agent-bom on PyPI](https://pypi.org/project/agent-bom/) <br>
- [Cloud Resource Manager API endpoint](https://cloudresourcemanager.googleapis.com) <br>
- [Vertex AI API endpoint](https://aiplatform.googleapis.com) <br>
- [Cloud Run API endpoint](https://run.googleapis.com) <br>
- [Cloud Functions API endpoint](https://cloudfunctions.googleapis.com) <br>
- [Google Kubernetes Engine API endpoint](https://container.googleapis.com) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance, JSON files] <br>
**Output Format:** [Markdown guidance with shell commands and JSON inventory output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes operator-selected inventory JSON locally and can produce optional agent-bom findings JSON.] <br>

## Skill Version(s): <br>
0.89.2 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
