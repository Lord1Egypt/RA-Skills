## Description: <br>
Generates production-ready React TSX frontend components from natural-language UI goals for non-programmers, including setup instructions and dependencies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[h4gen](https://clawhub.ai/user/h4gen) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, developers, and non-programmers use this skill to turn natural-language UI requirements into a single React TypeScript component with setup commands, assumptions, and adaptation notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may ask users to install or update upstream ClawHub skills and run npx commands. <br>
Mitigation: Confirm the required upstream skills are intended and review npx commands before running them. <br>
Risk: shadcn setup commands can modify the target frontend project. <br>
Mitigation: Run shadcn setup only inside the intended project and use version control so changes can be reviewed. <br>
Risk: Using clawhub update --all can update more installed skills than this workflow requires. <br>
Mitigation: Avoid update-all unless broad skill updates are intentional. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/h4gen/frontend-builder) <br>
- [Inspected upstream skills](references/inspected-skills.md) <br>
- [ClawHub](https://clawhub.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and a single TypeScript React TSX component] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default output includes setup commands, one self-contained TSX file, assumptions, and adaptation notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
