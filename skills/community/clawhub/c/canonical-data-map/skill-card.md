## Description: <br>
Single source of truth for all paths, naming conventions, and data formats across the OpenClaw Greek Accounting system. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[satoshistackalotto](https://clawhub.ai/user/satoshistackalotto) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators of OpenClaw Greek Accounting use this reference skill to keep agents aligned on canonical data directories, naming conventions, schemas, audit records, encryption expectations, and ownership boundaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent memory, chat, audit, and proposal workflows may store sensitive accounting or identity data longer or more broadly than intended. <br>
Mitigation: Define and enforce redaction, encryption, access control, retention, deletion, and user-notice rules before using the skill with real client, payroll, banking, tax, or auth data. <br>
Risk: Memory-feedback proposals could carry sensitive operational details into GitHub pull requests. <br>
Mitigation: Require human review and scanning of every memory-feedback proposal before merge, and prevent proposals from including secrets, client identifiers, or regulated records. <br>


## Reference(s): <br>
- [Canonical Data Map on ClawHub](https://clawhub.ai/satoshistackalotto/canonical-data-map) <br>
- [OpenClaw Greek Accounting homepage](https://github.com/satoshistackalotto/openclaw-greek-accounting) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown reference document with directory maps, JSON examples, YAML examples, and inline bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires OPENCLAW_DATA_DIR for the documented setup commands; the skill itself is reference-only and does not require binaries or credentials.] <br>

## Skill Version(s): <br>
0.1.1 (source: ClawHub release metadata; artifact frontmatter lists document version 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
