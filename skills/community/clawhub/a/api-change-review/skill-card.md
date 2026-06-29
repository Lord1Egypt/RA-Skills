## Description: <br>
Review an API change for compatibility, validation, auth, error shape, idempotency, and observability, and classify it as additive, behavior-changing, or breaking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ritual](https://clawhub.ai/user/ritual) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to review API contract changes, classify compatibility impact, and produce a verdict with required fixes, tests, migration notes, and rollout checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optional knowledge-capture workflow can write a reusable note into the repository. <br>
Mitigation: Only write the note after explicit user approval and keep it small with cited evidence. <br>
Risk: The optional Ritual Cloud path requires installing and initializing an external CLI. <br>
Mitigation: Review what the external CLI does before enabling it and use the skill locally when cloud context is unnecessary. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ritual/api-change-review) <br>
- [Ritual homepage](https://ritual.work) <br>
- [Open Knowledge Format overview](https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, shell commands, configuration] <br>
**Output Format:** [Markdown or plain text review notes with optional shell commands and OKF markdown when approved] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local-first checklist output; optional knowledge-note file writes require user approval.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
