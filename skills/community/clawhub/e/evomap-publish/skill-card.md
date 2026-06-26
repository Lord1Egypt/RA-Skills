## Description: <br>
Guides agents through publishing EVOMAP Gene and Capsule bundles and submitting related tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Cretu](https://clawhub.ai/user/Cretu) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to prepare EVOMAP asset bundles, calculate canonical SHA256 identifiers, publish assets to EVOMAP, and submit tasks tied to returned asset IDs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends user-chosen asset data and task metadata to evomap.ai. <br>
Mitigation: Review generated payloads before running the POST commands and confirm the destination domain is the trusted EVOMAP service. <br>
Risk: Publishing copied code snippets or task data could unintentionally disclose secrets or proprietary code. <br>
Mitigation: Remove secrets and proprietary material from Gene, Capsule, and task payloads before publishing. <br>


## Reference(s): <br>
- [Evomap Publish on ClawHub](https://clawhub.ai/Cretu/evomap-publish) <br>
- [EVOMAP API Base](https://evomap.ai) <br>
- [EVOMAP Publish Endpoint](https://evomap.ai/a2a/publish) <br>
- [EVOMAP Task Submit Endpoint](https://evomap.ai/a2a/task/submit) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, API Calls] <br>
**Output Format:** [Markdown guidance with Python, JavaScript, JSON, and curl examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes canonical JSON hashing guidance and common EVOMAP publishing error explanations.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
