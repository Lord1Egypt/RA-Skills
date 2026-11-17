## Description: <br>
Design Toolkit Free helps an agent learn and reuse a user's visual preferences for UI and graphic design through lightweight local Markdown records. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and design-focused developers use this skill to help an agent remember personal UI and graphic design preferences, apply them to later design tasks, and maintain a local preference profile they can review or edit. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist personal visual design preferences in a local Markdown profile. <br>
Mitigation: Install only when local preference memory is desired, and periodically review ~/.design-preferences/profile.md. <br>
Risk: The initialization snippet may create or replace a preference profile file the user already maintains. <br>
Mitigation: Avoid running the initialization snippet until any existing profile file has been backed up or intentionally replaced. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/design-toolkit-free) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, code snippets, configuration examples, and design preference guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update a local Markdown preference profile at ~/.design-preferences/profile.md.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
