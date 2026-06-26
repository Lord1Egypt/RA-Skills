## Description: <br>
Generate an Arknights operator agent based on gacha probabilities with authentic lore and personality. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hg-hg](https://clawhub.ai/user/hg-hg) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Players and agent users use this skill to randomly create an Arknights-themed OpenClaw character agent, populate it with lore-based identity files, and start an operator arrival interaction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates a persistent OpenClaw character agent and workspace under ~/.openclaw. <br>
Mitigation: Install and run it only when persistent agent creation is desired, and remove the generated agent and workspace afterward if they should not be kept. <br>
Risk: The skill fetches public wiki content and downloads an avatar image from external sources. <br>
Mitigation: Rely on the disclosed domain allowlist, HTTPS requirement, content-type validation, and file-size limit; review fetched/generated lore before reuse. <br>
Risk: The skill runs git commits inside the generated agent workspace. <br>
Mitigation: Review the generated workspace files before sharing or publishing the created agent. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hg-hg/arknights-operator-gacha) <br>
- [Arknights Fandom operator lists](https://arknights.fandom.com/wiki/Operator/{star}-star) <br>
- [PRTS Wiki operator pages](https://prts.wiki/w/{operator}) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [JSON worker output, Markdown agent files, shell commands, and final text summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates a persistent OpenClaw agent workspace, downloads a validated avatar image, commits generated files, and may spawn the new agent for a greeting.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
