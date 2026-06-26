## Description: <br>
Datasets provides a local command-line logger for dataset-related activity such as ingest, transform, query, filter, and export notes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ckchzh](https://clawhub.ai/user/ckchzh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and data practitioners can use this skill as a local CLI activity tracker for dataset-related notes, operations, and exports. It is not evidenced as a real dataset browser or loader beyond local logging. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may expect a ready-to-use dataset browser or loader, but the evidenced behavior is a local dataset-activity note tracker. <br>
Mitigation: Install only when local activity logging is desired, and validate behavior before using it in dataset workflows. <br>
Risk: Command inputs may be stored under ~/.local/share/datasets and later exposed through search, recent, status, or export commands. <br>
Mitigation: Do not enter credentials, tokens, proprietary queries, or sensitive dataset details; review and remove local logs when needed. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/ckchzh/datasets) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, files] <br>
**Output Format:** [Plain text CLI output with local JSON, CSV, or TXT export files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local log and export files under ~/.local/share/datasets.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
