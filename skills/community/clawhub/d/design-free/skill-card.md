## Description: <br>
Design LITE learns UI design preferences from user choices and feedback, then records confirmed Aesthetic and Never entries after three consistent signals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and designers use this skill to help an agent remember simple UI aesthetic preferences and design prohibitions across UI design iterations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can build a persistent profile of UI design preferences over time. <br>
Mitigation: Review stored preference entries periodically, keep entries concise and UI-focused, and remove or override entries when the user explicitly changes a preference. <br>
Risk: The skill asks for read, write, and execution authority beyond basic preference learning. <br>
Mitigation: Review before installation and use agent-level controls to limit shell execution and file writes to the minimum needed for the workflow. <br>
Risk: The optional callback URL flow could send data outside the local agent environment. <br>
Mitigation: Avoid callback delivery unless the destination and transmitted data are understood and approved. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/design-free) <br>
- [Publisher profile](https://clawhub.ai/user/thcjp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [JSON responses with Markdown-style preference entries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Preference entries are intended to stay concise, UI-focused, and organized into Aesthetic and Never sections.] <br>

## Skill Version(s): <br>
1.0.2 (source: server evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
