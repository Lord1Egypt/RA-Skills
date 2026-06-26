## Description: <br>
Generate professional diagrams including cloud architecture, data charts, academic figures, and more from user descriptions or reference images. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CodeHourra](https://clawhub.ai/user/CodeHourra) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users, developers, and technical authors use this skill to plan and generate cloud architecture diagrams, data visualizations, flow diagrams, network topology diagrams, and academic figures. It guides tool selection, asks for confirmation, and can produce diagram code and output files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can contact an external billing service and charge for generation before the user has confirmed the final work. <br>
Mitigation: Require explicit user confirmation before every paid generation and verify the SkillPay account identity before use. <br>
Risk: The documented anonymous_user fallback can obscure which user is being billed or authorized. <br>
Mitigation: Set a deliberate SKILLPAY_USER_ID for each user or session and do not rely on the anonymous fallback. <br>
Risk: Diagram and LaTeX generation can execute code and use large third-party dependencies. <br>
Mitigation: Run generation in an isolated environment with pinned dependencies and review generated code before execution. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/CodeHourra/diagrams-generator-pro) <br>
- [Diagrams API Reference](references/diagrams-api.md) <br>
- [Styling Guide](references/styling-guide.md) <br>
- [SkillPay](https://skillpay.me) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown with Mermaid previews, Python code blocks, shell commands, and generated diagram files such as PNG, SVG, PDF, or HTML.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May contact SkillPay for paid generation and may write generated code plus diagram assets under a local output directory.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
