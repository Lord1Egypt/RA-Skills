## Description: <br>
Generates offline Chinese interactive HTML courses from a codebase, with a product-manager mode focused on business flow and architecture and a developer mode focused on technical architecture, data flow, and implementation decisions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhouchang1988](https://clawhub.ai/user/zhouchang1988) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, engineers, product managers, and business stakeholders use this skill to turn a repository into a local, browser-readable course that explains system behavior, module responsibilities, architecture, and data flow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads source repositories that may contain sensitive code or credentials. <br>
Mitigation: Use it on trusted repositories or disposable workspaces, and review generated course content before sharing it. <br>
Risk: Generated HTML may expose private implementation details from sensitive codebases. <br>
Mitigation: Review the generated HTML and derived output directory before opening, publishing, or distributing the course. <br>
Risk: Course generation creates a derived output directory and performs a local build step. <br>
Mitigation: Check the resolved output path and generated files before relying on the build output. <br>


## Reference(s): <br>
- [README](README.md) <br>
- [Design System](references/design-system.md) <br>
- [Interactive Elements](references/interactive-elements.md) <br>
- [Product Content Philosophy](references/content-philosophy.md) <br>
- [Developer Content Philosophy](references/content-philosophy-pro.md) <br>
- [Implementation Gotchas](references/gotchas.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [A local HTML course directory with Markdown briefs, HTML modules, CSS and JavaScript assets, an assembled index.html file, and build commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated courses are intended to run offline with localized assets and no external CDN dependency.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
