## Description: <br>
Convert EPUB books into an AI-ready Markdown library with a first-read META.md navigation index, per-chapter Markdown files, and extracted images. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yueeli](https://clawhub.ai/user/yueeli) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and agents use this skill to convert user-selected EPUB books into navigable Markdown workspaces for reading, summarization, retrieval, analysis, and downstream text processing without loading an entire book at once. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: First use may download Python package dependencies through uv. <br>
Mitigation: Install and run in an environment where dependency downloads are allowed and review the declared dependencies before first execution. <br>
Risk: Conversion writes generated Markdown and image files beside the EPUB or in the selected output directory. <br>
Mitigation: Choose an output directory intended for generated exports and review the destination path before running the converter. <br>
Risk: Using --overwrite can replace an existing generated export directory. <br>
Mitigation: Use --overwrite only when the selected output directory is safe to replace. <br>
Risk: DRM-protected or complex EPUB3 books may not convert completely. <br>
Mitigation: Check META.md and chapter files after conversion, especially when the EPUB has sparse table-of-contents data, DRM, JavaScript-heavy content, or SVG assets. <br>


## Reference(s): <br>
- [Overview](references/overview.md) <br>
- [EPUB to Markdown Reference](references/reference.md) <br>
- [Examples](references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, shell commands, guidance] <br>
**Output Format:** [Markdown files, extracted image files, META.md index, and a concise text conversion summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates META.md, chapters/, and images/ in the chosen output directory; conversion stops on an existing output directory unless --overwrite is explicitly used.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata and claw.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
