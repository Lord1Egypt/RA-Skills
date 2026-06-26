## Description: <br>
ClawBoss turns an OpenClaw agent into a productivity coach that uses the GROW model, adaptive accountability, progress check-ins, and reflection prompts to support goal execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Paitesanshi](https://clawhub.ai/user/Paitesanshi) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External OpenClaw users use this skill to structure goals, break work into action plans, receive progress check-ins, and reflect on blockers and success patterns. It is suited to personal productivity workflows where local goal memory and recurring coaching prompts are acceptable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill keeps a local persistent record of goals, blockers, reflections, progress, and check-ins. <br>
Mitigation: Install only when local productivity memory is acceptable, and periodically review or remove stored memory files if they contain sensitive personal information. <br>
Risk: The documented installer uses an unpinned `npx clawboss@latest` command. <br>
Mitigation: Review or pin the npm package version before installation when reproducibility or supply-chain review is required. <br>
Risk: One optional coaching persona can use emotionally intimate language that may be uncomfortable or distracting. <br>
Mitigation: Choose a non-romantic coaching persona for professional or emotionally sensitive contexts. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Paitesanshi/clawboss) <br>
- [Publisher Profile](https://clawhub.ai/user/Paitesanshi) <br>
- [Artifact Skill Documentation](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Conversational coaching text with Markdown task files, JSON state, and inline shell or configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local goal, progress, check-in, and reflection records under the OpenClaw workspace memory directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
