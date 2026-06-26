## Description: <br>
Evidence-first debugging and incident triage for unclear, recurring, production-like, or high-risk software bugs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brasco05](https://clawhub.ai/user/brasco05) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI coding agents use Deep Debugging to investigate unclear, recurring, production-like, or high-risk software failures through evidence collection, one testable hypothesis at a time, minimal reversible fixes, and verified prevention steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Debugging evidence may contain secrets, customer data, cookies, tokens, or raw production payloads. <br>
Mitigation: Review and redact logs or snapshot output before sharing; collect environment key names only and omit secret values. <br>
Risk: Rollback, deploy, migration, credential, external API, or data repair actions can change production state. <br>
Mitigation: Require explicit user approval before any production write or third-party action, and prefer reversible stabilization steps. <br>
Risk: A root cause may be asserted before enough evidence has been collected. <br>
Mitigation: Follow the evidence-first workflow: state one testable hypothesis, prove or disprove it, verify the exact failure path, and report remaining risk. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/brasco05/deep-debugging) <br>
- [Incident-First Debugging Reference](references/incident-first.md) <br>
- [Output Templates](references/output-templates.md) <br>
- [Stack Checklists](references/stack-checklists.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with plain-text report templates and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use an optional local diagnostic snapshot helper that prints environment key names only and omits secret values.] <br>

## Skill Version(s): <br>
2.2.0 (source: server release metadata, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
