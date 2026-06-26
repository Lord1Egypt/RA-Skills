## Description: <br>
This skill guides an agent through researching, planning, writing, building, and versioning 100-page-plus PDF manuals with modular HTML fragments and Playwright PDF rendering. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[RenBigCheng](https://clawhub.ai/user/RenBigCheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, technical writers, and content teams use this skill to produce complete PDF manuals, ebooks, reference guides, and similar long-form documents. It supports a workflow from topic research and outline planning through parallel HTML-fragment drafting, build assembly, PDF rendering, and version updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Helper scripts handle user-controlled titles and update messages unsafely. <br>
Mitigation: Review or patch the scripts before use, especially paths and changelog message handling. <br>
Risk: Untrusted or punctuation-heavy titles can affect generated paths and file names. <br>
Mitigation: Run in an isolated project directory and avoid slashes, '..', and untrusted title strings. <br>
Risk: PDF rendering may download npm, Chromium, or font assets. <br>
Mitigation: Expect dependency downloads and possible Google Fonts network requests during setup or rendering. <br>


## Reference(s): <br>
- [Design System Reference](references/design-system.md) <br>
- [Node.js](https://nodejs.org/) <br>
- [ClawHub Skill Page](https://clawhub.ai/RenBigCheng/book-pdf) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and HTML, JavaScript, CSS, and JSON project files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The workflow can create or update a project scaffold, research notes, PROJECT.md, HTML fragments, version metadata, changelog entries, rendered HTML, archived versions, and PDF outputs when its scripts are executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
