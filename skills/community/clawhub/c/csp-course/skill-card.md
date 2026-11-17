## Description:

Generates complete C++ CSP/NOIP teaching material packages, including game-style PPT courseware, lesson plans, student worksheets, C++ examples, interactive HTML exercises, and optional PDF-to-course batch workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ahao2001](https://clawhub.ai/user/ahao2001)

### License/Terms of Use:

MIT-0

## Use Case:

External educators, curriculum authors, and agents use this skill to create Chinese-language C++/CSP courseware for elementary through junior competition students. It supports single-lesson generation and batch conversion from PDF teaching material into structured lesson assets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bundled generation scripts write to hard-coded local Windows paths and may overwrite files outside the user's intended folder.

Mitigation: Review and replace hard-coded output paths before running the scripts, and execute generators in a dedicated working folder.

Risk: Wildcard file moves can relocate unrelated .pptx, .docx, .cpp, or .html files when used in a mixed working directory.

Mitigation: Run cleanup commands only in an empty or purpose-specific generation directory and inspect destination paths before moving files.

Risk: Processing untrusted PDFs or images through local dependencies can expose the user to parser and dependency risk.

Mitigation: Update dependencies before processing untrusted files and run PDF or image processing in an isolated workspace.

## Reference(s):

- [ClawHub skill release page](https://clawhub.ai/ahao2001/skills/csp-course)
- [references/game_template.html](references/game_template.html)
- [references/素数判断讲解.md](references/素数判断讲解.md)
- [references/代码示例.cpp](references/代码示例.cpp)
- [PptxGenJS documentation](https://gitbrent.github.io/PptxGenJS/)
- [docx documentation](https://docx.js.org/)
- [pdfplumber project](https://github.com/jsvine/pdfplumber)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance with inline shell commands plus generated .pptx, .docx, .cpp, .html, and JSON course-content files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are intended for Chinese C++/CSP course preparation and may require user-selected output directories before script execution.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
