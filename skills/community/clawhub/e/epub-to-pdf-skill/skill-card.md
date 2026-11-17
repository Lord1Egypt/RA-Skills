## Description:

Convert EPUB e-books to PDF using ebooklib + WeasyPrint with proper CJK font support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hellobigbean](https://clawhub.ai/user/hellobigbean)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to convert EPUB e-books, including Chinese, Japanese, and Korean text, into PDF files by running the bundled Python conversion script.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A crafted EPUB could cause the converter to access local files or internal network resources during rendering.

Mitigation: Run the skill in an isolated, low-privilege environment without sensitive local files or internal network access, and prefer a version that restricts WeasyPrint resource fetching.

Risk: The installation guidance uses broad system-level package installation.

Mitigation: Avoid system-wide pip installation where possible and install dependencies in a constrained container or virtual environment.

Risk: The converter writes combined intermediate HTML to a shared temporary path.

Mitigation: Use per-run temporary files or isolate each conversion run to prevent collisions and unintended reuse of intermediate content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hellobigbean/skills/epub-to-pdf-skill)

## Skill Output:

**Output Type(s):** [Shell commands, Code, Files, Guidance]

**Output Format:** [Markdown with inline bash commands and generated PDF file output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a PDF at the caller-provided output path when dependencies, fonts, and input EPUB content are available.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
