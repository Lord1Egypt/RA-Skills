## Description: <br>
Bold UI helps agents apply professional design templates, polished icons, and framework-specific styling guidance across web, mobile, and desktop AI coding projects. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wh19981224](https://clawhub.ai/user/wh19981224) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI coding agents use this skill to evaluate an application's product context, choose or adapt a design direction, and generate UI code, design tokens, shell commands, or configuration for supported web and app frameworks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can import user-supplied GitHub templates into persistent local agent state. <br>
Mitigation: Use add-temp only with trusted repositories and review imported manifest and description files before installation. <br>
Risk: The skill can fetch remote SVG icons from third-party services. <br>
Mitigation: Prefer local icon fallbacks in restricted or sensitive environments. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/wh19981224/bold-ui) <br>
- [Skill instructions](SKILL.md) <br>
- [Template registry](templates/index.yaml) <br>
- [Tailwind CSS adapter](adapters/tailwindcss.md) <br>
- [CSS Variables adapter](adapters/css-variables.md) <br>
- [Iconify API example](https://api.iconify.design/lucide/arrow-right.svg?height=24) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with code blocks, implementation plans, and framework-specific snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include design tokens, component code, icon recommendations, and file modification guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and SKILL.md metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
