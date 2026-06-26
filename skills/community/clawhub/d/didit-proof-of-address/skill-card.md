## Description: <br>
Integrate Didit Proof of Address standalone API to verify address documents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rosasalberto](https://clawhub.ai/user/rosasalberto) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to integrate Didit's proof-of-address API, upload supported address documents, and interpret verification results such as approval status, extracted address fields, warnings, and review outcomes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uploads sensitive proof-of-address documents such as utility bills, bank statements, and government documents to Didit. <br>
Mitigation: Confirm the exact document before upload and review Didit's privacy, retention, and billing behavior before submitting sensitive records. <br>
Risk: The workflow uses DIDIT_API_KEY to authenticate API requests. <br>
Mitigation: Use only an API key intended for this workflow and handle it as a secret in the agent environment. <br>
Risk: Optional vendor_data can add unnecessary identifiers to verification requests. <br>
Mitigation: Avoid unnecessary vendor_data and include only identifiers required for the user's workflow. <br>


## Reference(s): <br>
- [Didit Documentation](https://docs.didit.me) <br>
- [Didit Proof of Address API Reference](https://docs.didit.me/standalone-apis/proof-of-address) <br>
- [Didit Proof of Address Feature Guide](https://docs.didit.me/core-technology/proof-of-address/overview) <br>
- [ClawHub Skill Page](https://clawhub.ai/rosasalberto/didit-proof-of-address) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration instructions, API Calls, JSON] <br>
**Output Format:** [Markdown guidance with inline code examples, shell commands, and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires DIDIT_API_KEY and uploads proof-of-address documents to Didit's API.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
