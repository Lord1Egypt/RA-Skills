## Description:

Check image DPI and intelligently upscale low-resolution images using super-resolution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and print-preparation teams use this skill to inspect image DPI, estimate print readiness, and upscale low-resolution image files when higher-resolution outputs are needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The dependency manifest contains ambiguous and unpinned Python packages.

Mitigation: Review and replace the manifest before installation by removing cv2 and pil, keeping canonical packages, and pinning reviewed versions or using a lockfile in an isolated nonprivileged environment.

Risk: Batch processing can read many image files and create many new output files.

Mitigation: Run the tool only on intended image folders and choose an output directory where creating multiple files is acceptable.

Risk: Super-resolution output can be limited for extremely blurry inputs and large files can require substantial memory.

Mitigation: Review restored images before relying on them for print or publication, and test large batches in a controlled workspace before broad use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aipoch-ai/skills/dpi-upscaler-checker)

## Skill Output:

**Output Type(s):** [text, JSON, image files, shell commands]

**Output Format:** [Console text, JSON DPI reports, and upscaled image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can process a single image or a folder and may create multiple output files.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
