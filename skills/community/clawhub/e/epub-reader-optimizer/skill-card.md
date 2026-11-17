## Description:

Optimizes EPUB reading experience by rewriting CSS, arranging bilingual Chinese-English paragraphs, applying reader-friendly font handling, improving code blocks and tables, and fixing common text visibility issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samonysh](https://clawhub.ai/user/samonysh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and publishing workflow maintainers use this skill to improve EPUB layout, typography, bilingual paragraph presentation, image-based formula rendering, code block readability, table styling, and EPUB package correctness without intentionally rewriting book text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can edit EPUB working files and generate local output files.

Mitigation: Use a copy of the original EPUB and choose output paths carefully before running helper scripts.

Risk: Helper scripts can overwrite an existing output EPUB or remove source TTF files from the EPUB working directory after font subsetting.

Mitigation: Run in a disposable working directory or keep backups of the unpacked EPUB and font inputs.

Risk: Remote font downloads are part of some workflows.

Mitigation: Confirm any remote font downloads explicitly and pin them to release URLs before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/samonysh/skills/epub-reader-optimizer)
- [LXGW WenKai Lite regular font release](https://github.com/lxgw/LxgwWenKai-Lite/releases/download/v1.522/LXGWWenKaiLite-Regular.ttf)
- [LXGW WenKai Lite mono font release](https://github.com/lxgw/LxgwWenKai-Lite/releases/download/v1.522/LXGWWenKaiMonoLite-Regular.ttf)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with file paths, shell commands, CSS snippets, Python helper usage, and generated or modified EPUB working files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local file edits and EPUB artifacts in a user-selected workspace.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
