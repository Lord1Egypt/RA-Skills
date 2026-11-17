## Description:

Converts Markdown into an ElegantBook LaTeX book project and PDF.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samonysh](https://clawhub.ai/user/samonysh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, technical writers, and educators use this skill to turn Markdown source material into a Chinese ElegantBook LaTeX project and PDF with professionally formatted tables and diagrams.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote template or URL fetching can introduce unreviewed content.

Mitigation: Keep network access off by default and fetch remote resources only with explicit approval from pinned release tags.

Risk: LaTeX compilation and diagram rendering run local tools and may become unsafe if shell escape or package installation is enabled casually.

Mitigation: Keep package installation and LaTeX shell escape disabled by default; enable them only for trusted input in an approved sandboxed environment.

Risk: The workflow may rewrite source material into Chinese when that is not the user's intent.

Mitigation: Ask for or honor the desired output language before rewriting long-form source material.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/samonysh/skills/elegantbook-latex)
- [ElegantLaTeX ElegantBook](https://github.com/ElegantLaTeX/ElegantBook)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance and generated LaTeX project files with build commands and PDF status summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce a local project directory containing LaTeX source, chapter files, image assets, diagram outputs, build logs, and a final PDF when dependencies are available.]

## Skill Version(s):

1.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
