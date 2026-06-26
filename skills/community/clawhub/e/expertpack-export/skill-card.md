## Description: <br>
Export an OpenClaw instance's accumulated knowledge into a structured ExpertPack composite for backup, migration, or portable knowledge snapshots. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brianhearn](https://clawhub.ai/user/brianhearn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to scan an OpenClaw workspace, propose ExpertPack constituents, scaffold distilled packs, compose a composite manifest, and validate the resulting portable export. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill scans sensitive workspace knowledge, including agent identity, memory, user profile, logs, tools, infrastructure, and integrations. <br>
Mitigation: Review the scan manifest and all generated files before sharing or syncing an export; keep user-specific and infrastructure-specific content private unless explicitly approved. <br>
Risk: Automatic redaction is not guaranteed to catch every secret or sensitive detail. <br>
Mitigation: Run the validation step and manually inspect files derived from tools, infrastructure, integrations, memory, logs, and profiles before distribution. <br>
Risk: Pack classification and distillation can be ambiguous or incomplete. <br>
Mitigation: Review proposed packs, confidence scores, warnings, and generated stubs before composing the final ExpertPack composite. <br>


## Reference(s): <br>
- [ExpertPack homepage](https://expertpack.ai) <br>
- [ExpertPack schema docs](https://expertpack.ai/#schemas) <br>
- [ExpertPack repository](https://github.com/brianhearn/ExpertPack) <br>
- [ExpertPack Schema Summary for Export](references/schemas-summary.md) <br>
- [ClawHub skill page](https://clawhub.ai/brianhearn/expertpack-export) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [JSON scan manifests, Markdown pack files with YAML frontmatter, YAML manifests, shell commands, and validation summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces files under the selected export directory and leaves the live OpenClaw workspace unchanged.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
