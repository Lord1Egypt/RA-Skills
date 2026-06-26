## Description: <br>
Provides read-only Figma design analysis, asset export, accessibility auditing, design-system inspection, and design documentation support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maddiedreese](https://clawhub.ai/user/maddiedreese) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Designers, developers, and design-system maintainers use this skill to inspect Figma files, export assets, audit accessibility and style consistency, and generate implementation-ready design documentation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Figma access tokens can expose design data if committed, logged, or shared. <br>
Mitigation: Store the token as a secret or in an untracked .env file, keep it out of source control, and rotate it if exposed. <br>
Risk: Exported assets and reports may contain proprietary design content and are written to the local workspace. <br>
Mitigation: Install and run the skill only where those files are acceptable, prefer a dedicated output directory, and review outputs before sharing. <br>
Risk: Python dependencies and API-facing scripts require ordinary dependency hygiene. <br>
Mitigation: Install dependencies from trusted sources, keep them updated, and run the skill in an isolated workspace when practical. <br>


## Reference(s): <br>
- [Figma API Reference](references/figma-api-reference.md) <br>
- [Accessibility Guidelines](references/accessibility-guidelines.md) <br>
- [Design Patterns](references/design-patterns.md) <br>
- [Export Formats](references/export-formats.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/maddiedreese/figma) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with shell command examples, JSON summaries, and generated asset or report files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Figma access token and writes exported assets or reports to local output directories.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
