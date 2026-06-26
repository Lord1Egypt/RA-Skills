## Description: <br>
AANA File Operation Guardrail Skill helps agents review risky file operations such as delete, move, rename, overwrite, publish, upload, export, and bulk edit before acting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mindbomber](https://clawhub.ai/user/mindbomber) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this instruction-only skill to make file operations more deliberate by checking target scope, authorization, reversibility, and safer alternatives before modifying, deleting, publishing, or uploading files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A bundled example has an approval-field inconsistency for a destructive bulk operation. <br>
Mitigation: Require explicit approval for destructive or bulk file operations even when an example payload suggests otherwise. <br>
Risk: File operations can accidentally delete, overwrite, publish, upload, or expose unintended user files if scope is unclear. <br>
Mitigation: Confirm exact target paths or a bounded folder, prefer dry-runs, diffs, or backups, and defer when ownership or expected impact is unclear. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/mindbomber/aana-file-operation-guardrail) <br>
- [README](artifact/README.md) <br>
- [Manifest](artifact/manifest.json) <br>
- [File Operation Review Schema](artifact/schemas/file-operation-review.schema.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown guidance with an optional structured file operation review pattern] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only; does not execute commands, call services, write files, or persist memory by itself.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata; artifact manifest lists 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
