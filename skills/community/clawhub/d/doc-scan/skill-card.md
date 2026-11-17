## Description:

Deprecated document scanning skill that converts document photos into scanned-looking images or PDFs with perspective correction, shadow removal, and scan-quality enhancement.

This skill is ready for commercial/non-commercial use.

## Publisher:

[piyush-zinc](https://clawhub.ai/user/piyush-zinc)

### License/Terms of Use:


## Use Case:

External users and developers use this deprecated skill to scan document photos, correct perspective, enhance readability, and create image or PDF scan outputs. The release notes direct users to doc-process v4.0.0 or later for current document scanning workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill instructs the agent to silently log scan activity, including filenames, to an external timeline component.

Mitigation: Remove the silent logging step or make it explicit and opt-in with clear retention and deletion controls before deployment.

Risk: Sensitive document names or context may be exposed through scan metadata or shared output locations.

Mitigation: Use private, trusted output directories and avoid shared or attacker-writable folders for generated image and PDF files.

Risk: Unpinned imaging dependencies can change scanner behavior or introduce supply-chain risk.

Mitigation: Install dependencies from pinned, trusted package sources and review them before use.

## Reference(s):

- [Doc Scan ClawHub page](https://clawhub.ai/piyush-zinc/skills/doc-scan)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands; the scanner script writes image or PDF files and emits JSON status.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports single-image and multi-page scans, black-and-white, grayscale, or color enhancement, optional manual document corners, optional PDF output, and DPI metadata.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
