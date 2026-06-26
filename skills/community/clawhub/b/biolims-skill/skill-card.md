## Description: <br>
Call Bio-LIMS APIs to query and manage orders, sample receiving, experiment templates, sequencing QC, reports, and related lab workflows through CLI-style commands and reference guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[biolims](https://clawhub.ai/user/biolims) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and lab operations users use this skill to operate Bio-LIMS workflows from an agent, including order lookup and mutation, sample receipt, barcode scanning, experiment template management, sequencing QC, report workflows, and exports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill grants an agent broad Bio-LIMS authority, including patient and order lookup, lab workflow mutation, QC changes, report operations, and exports. <br>
Mitigation: Install only for agents that need this authority, scope credentials narrowly, and review proposed actions before execution. <br>
Risk: Local server modes can expose Bio-LIMS operations if run without authentication, localhost binding, and CORS restrictions. <br>
Mitigation: Avoid server modes unless authentication is added, the service is bound to localhost, and CORS is restricted. <br>
Risk: Token caches and exported lab data may contain sensitive information. <br>
Mitigation: Treat token, cache, and export files as sensitive data and limit file access to trusted users and processes. <br>
Risk: Delete, complete, recall, import/export, report-send, and bulk-update commands can change lab workflow state or disclose data. <br>
Mitigation: Require explicit human confirmation before running destructive, state-changing, sending, export, or bulk operations. <br>
Risk: Incorrect Bio-LIMS field names can cause order or sample receive data loss. <br>
Mitigation: Use the bundled field-mapping references and validate JSON payload fields before create or update operations. <br>


## Reference(s): <br>
- [BioLIMS SKILL on ClawHub](https://clawhub.ai/biolims/biolims-skill) <br>
- [Bio-LIMS API Reference](artifact/references/api.md) <br>
- [Order Module API Reference](artifact/references/order-api.md) <br>
- [Sample Receive Module API Reference](artifact/references/receive-api.md) <br>
- [Experiment Template Module API Reference](artifact/references/experiment-template-api.md) <br>
- [Experiment Center Module API Reference](artifact/references/experiment-api.md) <br>
- [Sequencing QC Module API Reference](artifact/references/qc-api.md) <br>
- [Report Module API Reference](artifact/references/report-api.md) <br>
- [Bio-LIMS Key Operation Rules](artifact/references/biolims-rules.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON payload examples and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May trigger Bio-LIMS API calls through local scripts and can read or produce JSON request and response data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, created 2026-03-25) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
