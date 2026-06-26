## Description: <br>
Primary skill for applying confirmed Calibre metadata edits to an existing Content server while avoiding read-only lookup workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nextaltair](https://clawhub.ai/user/nextaltair) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and library operators use this skill to update existing Calibre book metadata after confirming target IDs, dry-running changes, and approving writes. It supports single-book fixes and library-wide metadata maintenance where low-confidence candidates remain pending for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can modify metadata on a target Calibre Content server. <br>
Mitigation: Use confirmed IDs, run dry-runs first, require explicit approval before writes, and re-read final values after applying changes. <br>
Risk: Credentials or book metadata may be exposed if handled carelessly during execution. <br>
Mitigation: Prefer CALIBRE_PASSWORD over plaintext passwords and skip subagent processing when book metadata should remain local. <br>
Risk: Generated comments_html or analysis content may introduce incorrect metadata notes. <br>
Mitigation: Review comments_html and analysis content before approving any write operation. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/nextaltair/calibre-metadata-apply) <br>
- [README](artifact/README.md) <br>
- [Skill Definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, JSONL] <br>
**Output Format:** [Markdown guidance with shell commands and JSONL change payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default workflow requires confirmed book IDs, dry-run before apply, and explicit approval for writes.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata and release changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
