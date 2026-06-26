## Description: <br>
Generate comprehensive data migration plans between cloud vendors for databases, big data platforms, object storage, and data lakes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangbingpeng](https://clawhub.ai/user/wangbingpeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Cloud architects and data engineers use this skill to plan migrations between major cloud providers, including target product selection, migration strategy, tooling, assessment, proof-of-concept planning, risks, and rollback guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated migration steps may affect production data or service availability if applied without validation. <br>
Mitigation: Review the plan with qualified operators and test the steps in a non-production environment before using them on live systems. <br>
Risk: Migration planning prompts may expose credentials or sensitive customer data if users provide unnecessary details. <br>
Mitigation: Provide architecture-level details only and avoid sharing secrets, credentials, or sensitive customer records. <br>


## Reference(s): <br>
- [Cloud Data Migration Examples](examples.md) <br>
- [Cloud Vendor Product Mapping](product-mapping.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration guidance] <br>
**Output Format:** [Markdown migration plan with tables, checklists, and step-by-step guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Advisory output that should be reviewed and tested before production use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
