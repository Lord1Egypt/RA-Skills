## Description: <br>
Validate, diff, and export DESIGN.md files to ensure consistent design tokens, WCAG compliance, and design system integrity across projects. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[flexrox](https://clawhub.ai/user/flexrox) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and UI engineers use this skill to validate DESIGN.md files, compare design-token revisions, export tokens for implementation, and keep UI component work aligned with documented design systems. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Security review flagged helper behavior that can run nested review commands with broad local repository access. <br>
Mitigation: Review command lines before execution, prefer no-yolo style operation when available, and run only in repositories where broad local review access is acceptable. <br>
Risk: The workflow asks agents to install or run @google/design.md through npm or npx in the local project. <br>
Mitigation: Use a trusted package version, review package behavior before first use, and run commands in a workspace where generated lint, diff, and export outputs can be inspected before adoption. <br>


## Reference(s): <br>
- [DESIGN.md specification](https://github.com/google-labs-code/design.md) <br>
- [Stitch Tool](https://stitch.withgoogle.com/) <br>
- [Design Tokens Format](https://www.designtokens.org/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown] <br>
**Output Format:** [Markdown with inline shell commands and references to JSON or configuration outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct agents to produce lint findings, diffs, Tailwind theme JSON, or DTCG token JSON using @google/design.md commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
