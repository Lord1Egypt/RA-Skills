## Description: <br>
Adds the Beckmann Knowledge Graph as a user-confirmed deep-reasoning escalation layer on top of the Self-Improving Agent while feeding resulting insights back into the learning log. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[matthiasbeckmann987-spec](https://clawhub.ai/user/matthiasbeckmann987-spec) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to route ordinary work through the Self-Improving Agent while escalating philosophical, paradoxical, strategic, AI-safety, or long-horizon forecast questions to the Beckmann Knowledge Graph after user confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local learning logs may retain summaries of errors, insights, and Beckmann analyses. <br>
Mitigation: Avoid using the skill on sensitive personal, business, or strategic topics unless those logs will be reviewed, protected, or deleted. <br>
Risk: The workflow depends on two required skills, so its reliability and behavior depend on those skills being present and trusted. <br>
Mitigation: Install and review the Self-Improving Agent and Beckmann Knowledge Graph skills before relying on this combination workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/matthiasbeckmann987-spec/beckmann-x-self-improving-agent) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown with structured reasoning sections and learning-log entry templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the Self-Improving Agent and Beckmann Knowledge Graph skills; Beckmann escalation requires user confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
