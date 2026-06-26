## Description: <br>
Auto-selects and applies design systems from awesome-design-md based on project type and task context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[html1602](https://clawhub.ai/user/html1602) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and design-focused agents use this skill to select an appropriate design system for UI work, generate local DESIGN.md guidance, and adapt choices for project types such as dashboards, documentation, marketing sites, developer tools, and AI/ML products. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is always active and broadly triggered, so it may influence UI work when design guidance was not intended. <br>
Mitigation: Install it only when an always-on design assistant is desired, and review its recommendations before applying them. <br>
Risk: The skill can fetch remote design files and write project guidance without a clear confirmation gate. <br>
Mitigation: Use it in a branch or disposable workspace, and require explicit approval before any network download or file creation. <br>


## Reference(s): <br>
- [Auto Design homepage](https://github.com/moyubox/auto-design) <br>
- [ClawHub skill page](https://clawhub.ai/html1602/auto-design-clawhub) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, configuration, shell commands] <br>
**Output Format:** [Markdown guidance with inline commands and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require node and curl; can generate local DESIGN.md references.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
