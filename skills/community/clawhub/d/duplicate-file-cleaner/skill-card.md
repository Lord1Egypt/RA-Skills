## Description: <br>
Scans local folders for exact duplicate files, generates structured reports, and helps agents propose safe cleanup actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ludiansheng](https://clawhub.ai/user/ludiansheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to scan user-selected folders such as Downloads, Pictures, or Documents for exact duplicate files, review disk-space impact, and plan safe cleanup. It is suited for duplicate downloads, photo-library cleanup, project backup cleanup, and post-sync file organization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Accidental deletion of important files if cleanup scripts are run without review. <br>
Mitigation: Back up important data, inspect the duplicate report, and require explicit confirmation before any delete, move, or generated cleanup script is run. <br>
Risk: Broad scans of system or sensitive directories can expose file paths, take a long time, or lead to unsafe cleanup recommendations. <br>
Mitigation: Start with limited user folders such as Downloads, Pictures, or Documents, and avoid system directories unless the user deliberately requests and reviews that scope. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ludiansheng/duplicate-file-cleaner) <br>
- [File Organization Best Practices Guide](references/file-organization-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, code, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON scan reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate local file deletion or move scripts only after user review and confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact manifest) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
