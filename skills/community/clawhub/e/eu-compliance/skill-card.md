## Description: <br>
EU compliance enforcement for AI agents covering NIS2, GDPR, and ISO 27001 by applying organisation profiles to data residency, supplier checks, secret blocking, audit logging, risk appetite, code generation, cloud deployments, data exports, and API integrations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pkerkhofs](https://clawhub.ai/user/pkerkhofs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, security teams, and compliance owners use this skill to add organisation-specific EU compliance checks to agent workflows for code review, cloud deployment, vendor assessment, incident handling, data handling, and NIS2 gap analysis. It reads or creates a compliance profile so guidance can reflect critical assets, supplier status, legal obligations, data residency constraints, and risk appetite. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is designed to apply a persistent organisation-wide compliance layer across prompts, files, memory, and compliance records. <br>
Mitigation: Enable it only for intended compliance, security, incident, vendor, deployment, or code-risk workflows, and document where the compliance profile is allowed to persist. <br>
Risk: Organisation profile data can include sensitive information about critical assets, suppliers, legal obligations, and risk appetite. <br>
Mitigation: Keep profile JSON out of system prompts or memory unless approved, store it only in approved locations, and avoid including unnecessary secrets or sensitive operational details. <br>
Risk: The skill may write .compliance records or export logs as part of audit, vendor, incident, change, or assessment workflows. <br>
Mitigation: Require user confirmation before writing compliance records or exporting logs, and review generated records before relying on them for formal compliance activity. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pkerkhofs/eu-compliance) <br>
- [complisec homepage](https://skills.eye.security/eu-compliance/) <br>
- [Organisation profile example](.compliance/profile.example.json) <br>
- [Audit logging guide](skills/audit-logging/references/logging-guide.md) <br>
- [Data sensitivity pattern index](skills/data-sensitivity/references/pattern-index.md) <br>
- [EU reporting directory](skills/incident-management/references/eu-reporting-directory.md) <br>
- [NIS2 questionnaire details](skills/nis2-gap-analysis/references/questionnaire-details.md) <br>
- [NIS2 Directive](https://eur-lex.europa.eu/eli/dir/2022/2555) <br>
- [General Data Protection Regulation](https://eur-lex.europa.eu/eli/reg/2016/679) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON records, configuration snippets, code snippets, and occasional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local .compliance profile, audit, change, vendor, incident, and assessment records when the user approves the workflow.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
