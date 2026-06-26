## Description: <br>
Generate polished .docx documents by injecting Markdown content into an existing Word template while preserving the template's cover page, TOC, fonts, headers, and footers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[loki612](https://clawhub.ai/user/loki612) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, technical writers, and enterprise teams use this skill to turn a Word template plus source materials into production-ready .docx deliverables. It guides template analysis, scoped research, chapter drafting, Mermaid rendering, and final document injection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Mermaid diagram rendering runs live npm code through npx. <br>
Mitigation: Use trusted Markdown and Mermaid input, and pin or preinstall Mermaid CLI instead of relying on live npx resolution. <br>
Risk: Chromium sandboxing is disabled for Mermaid rendering in the bundled Puppeteer configuration. <br>
Mitigation: Run rendering in a low-privilege or isolated environment and avoid --no-sandbox where the environment supports sandboxed Chromium. <br>
Risk: Local document-generation scripts modify generated Word outputs in the target workspace. <br>
Mitigation: Review inputs before execution and always write to a new .docx output path. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/loki612/corporate-doc-builder) <br>
- [README](artifact/README.md) <br>
- [Skill Definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with shell commands and generated .docx, Markdown, and PNG files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local Python document-generation scripts and Mermaid rendering; users should write final .docx output to a new path.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
