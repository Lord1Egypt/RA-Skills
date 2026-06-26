## Description: <br>
Extract design tokens from existing code and generate DESIGN.md with awesome-design-md comparison. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[html1602](https://clawhub.ai/user/html1602) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to scan project style files, extract design tokens such as colors, typography, spacing, and effects, and generate design-system documentation for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill scans project style files and may write generated design documentation and analysis files into the workspace. <br>
Mitigation: Run it in a version-controlled working tree and inspect generated files before committing or sharing them. <br>
Risk: Usage may invoke the referenced npm/GitHub extractor with npx. <br>
Mitigation: Review the referenced extractor package or repository before running it in sensitive projects. <br>


## Reference(s): <br>
- [Design Extractor homepage](https://github.com/moyubox/design-extractor) <br>
- [awesome-design-md](https://github.com/VoltAgent/awesome-design-md) <br>
- [ClawHub skill page](https://clawhub.ai/html1602/design-extractor-clawhub) <br>
- [Publisher profile](https://clawhub.ai/user/html1602) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown documentation with generated design-token analysis and optional JSON analysis artifacts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write DESIGN.md or DESIGN-EXTRACTED.md and Docs/Design/extracted-analysis.json into the analyzed workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
