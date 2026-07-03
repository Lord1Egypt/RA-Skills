## Description: <br>
Converts Markdown into an ElegantBook LaTeX book project and PDF for Chinese book-style typesetting with diagrams. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samonysh](https://clawhub.ai/user/samonysh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, technical writers, and agents use this skill to turn Markdown or structured content into a Chinese ElegantBook LaTeX project, compile it with local TeX tools, and deliver a PDF with diagrams and polished table formatting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Compiling LaTeX and rendering Mermaid or PlantUML diagrams may process untrusted content through local tools. <br>
Mitigation: Use a sandbox for untrusted Markdown or diagram content, and keep LaTeX shell escape disabled unless the user explicitly approves it for trusted content. <br>
Risk: Network access and package installation can introduce unreviewed code or changing dependencies. <br>
Mitigation: Keep network access and package installation disabled by default; require explicit approval before fetching remote resources or installing missing tools. <br>
Risk: Remote template fetches can drift if an unfixed branch is used. <br>
Mitigation: Prefer local template files or pin approved remote fetches to release tags instead of tracking master or main branches. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/samonysh/skills/elegantbook-latex) <br>
- [Publisher profile](https://clawhub.ai/user/samonysh) <br>
- [ElegantLaTeX ElegantBook](https://github.com/ElegantLaTeX/ElegantBook) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, files, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses with LaTeX source files, project structure, shell commands, and PDF build guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create a standalone LaTeX project directory containing main.tex, chapter files, figures, build scripts, logs, and a compiled PDF when local dependencies are available.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release evidence; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
