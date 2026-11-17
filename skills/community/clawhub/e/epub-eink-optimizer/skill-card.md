## Description:

This skill helps optimize EPUB files for e-ink readers by deduplicating images, removing tiny decorative images, resizing oversized images, and recompressing JPEGs to reduce file size while preserving readability.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangkf](https://clawhub.ai/user/wangkf)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to reduce EPUB size for e-ink reading workflows, especially when books contain duplicated, decorative, oversized, or high-quality images. It provides command-line guidance and scripts for analysis-first or in-place EPUB optimization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optimizer overwrites the selected EPUB when run without --dry-run.

Mitigation: Keep a backup copy and run with --dry-run before allowing the script to write changes.

Risk: Image deletion and lossy recompression can remove decorative images or reduce visual fidelity more than intended.

Mitigation: Review dry-run output and adjust --min-size, --quality, --max-width, or disable individual stages with the --no-* flags.

Risk: Very large or crafted EPUB archives and images can consume significant memory or CPU during extraction and image processing.

Mitigation: Process EPUBs from trusted sources in a normal user or virtual-environment Python setup, avoid sudo, and test suspicious files in an isolated workspace.

## Reference(s):

- [epub manual-fixes.md](references/manual-fixes.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include EPUB optimization commands, parameter recommendations, dry-run instructions, and manual remediation guidance.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
