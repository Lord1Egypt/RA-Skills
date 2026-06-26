## Description: <br>
EPAI helps agents administer EPAI knowledge bases, documents, and catalogs through a CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Iamlovingit](https://clawhub.ai/user/Iamlovingit) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use EPAI to manage EPAI platform resources from an agent workflow, including listing, creating, and deleting knowledge bases and catalogs, uploading documents, and listing or deleting documents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change or delete remote EPAI resources. <br>
Mitigation: Use a least-privileged EPAI API key and double-check knowledge base, catalog, and document IDs before running delete commands. <br>
Risk: The skill can upload selected local files to EPAI. <br>
Mitigation: Upload only documents intended for EPAI and confirm file paths before execution. <br>
Risk: Misconfigured service endpoints or TLS settings could send requests to the wrong service or weaken transport security. <br>
Mitigation: Verify EPAI_API_BASE points to the intended service and keep TLS verification enabled. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Iamlovingit/epaiskill) <br>
- [Publisher profile](https://clawhub.ai/user/Iamlovingit) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires EPAI_API_BASE, EPAI_API_KEY, EPAI_ACCOUNT, and EPAI_VERIFY_TLS environment variables.] <br>

## Skill Version(s): <br>
1.0.4 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
