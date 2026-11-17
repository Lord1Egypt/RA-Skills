## Description:

Batch Image Processing helps agents compress image directories, convert mixed image formats to JPEG, reorganize image folders, and prepare resumable local or remote batch-processing commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liuyunss](https://clawhub.ai/user/liuyunss)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to guide agents through bulk image compression, format conversion, output-directory planning, and metadata-based directory reorganization for large local or remote image collections.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bulk file writes, directory moves, and output-path reuse can overwrite or mix image collections.

Mitigation: Require explicit source and output paths, use a fresh output directory for each task, run reorganization in dry-run mode first, and ask for confirmation before moving directories.

Risk: Remote SSH execution can expose systems to unsafe host validation, excessive privileges, or unintended remote commands.

Mitigation: Use explicit hosts and paths, a restricted non-root account, strict known_hosts verification, and user confirmation before remote execution.

Risk: Large compression jobs can saturate CPU or memory and affect shared services.

Mitigation: Size worker counts to available CPU cores, leave capacity for system services, and monitor progress logs during long-running jobs.

Risk: Lossy JPEG recompression and format conversion can permanently reduce image fidelity or discard animation frames and transparency.

Mitigation: Preserve originals, choose quality settings deliberately, document conversion tradeoffs, and confirm that first-frame-only animation handling is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liuyunss/skills/batch-image-processing)
- [Publisher profile](https://clawhub.ai/user/liuyunss)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include generated Python scripts, compression settings, filesystem paths, SSH commands, and progress-reporting steps.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
