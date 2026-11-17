## Description: <br>
Chart Gen Free helps an agent generate lightweight command-line charts as terminal ASCII output or saved HTML/SVG chart files from user-provided data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and other external users can use this skill to ask an agent for quick bar, line, pie, sparkline, heatmap, progress, table, HTML, or SVG chart outputs for reports, monitoring summaries, and command-line workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: HTML or SVG output paths may overwrite existing files because overwrite behavior is not clearly specified. <br>
Mitigation: Use explicit output paths in a scratch or project-generated directory and avoid pointing outputs at important existing files. <br>
Risk: The artifact describes a chart script, but the evidence package contains only SKILL.md, which may prevent direct execution if the script is not supplied at install time. <br>
Mitigation: Confirm the required chart script is present in the installed skill package before relying on command examples. <br>


## Reference(s): <br>
- [ClawHub listing for Chart Gen Free](https://clawhub.ai/thcjp/skills/chart-gen-free) <br>
- [SkillHub homepage](https://skillhub.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, files, guidance] <br>
**Output Format:** [Markdown guidance with bash command examples; generated chart outputs may be terminal text, HTML files, or SVG files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Free edition scope; local Bash-oriented chart generation with no external API key requirement.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
