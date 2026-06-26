## Description: <br>
Personal deep product research report generator that automates topic research, Markdown report optimization, and Mermaid chart conversion into images. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shinelp100](https://clawhub.ai/user/shinelp100) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and analysts use this skill to generate professional Chinese-language product, industry, company, technology trend, market research, and investment memo reports with supporting Markdown structure and Mermaid-generated PNG charts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may use external research and search tools, so confidential or sensitive topics could be exposed to dependent services. <br>
Mitigation: Use only when the dependent tools' data handling is acceptable, and avoid confidential topics unless that handling has been reviewed. <br>
Risk: Generated research reports can contain incorrect, stale, or misleading claims. <br>
Mitigation: Review generated reports and sources before relying on them, especially for investment, market, or company analysis. <br>
Risk: The chart workflow creates report and image files in the workspace and runs Mermaid CLI through npm/npx. <br>
Mitigation: Run it in a dedicated project folder and review generated files and commands before deployment or sharing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shinelp100/deepresearchwork-forme) <br>
- [README.md](artifact/README.md) <br>
- [EXAMPLES.md](artifact/EXAMPLES.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown reports with Mermaid code blocks, PNG chart files, shell commands, and JSON configuration snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates a topic report Markdown file and a sibling mermaid_charts directory containing generated PNG images.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
