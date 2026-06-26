## Description: <br>
Flicker is an ASCII pet companion that can be summoned, show pet stats, generate new pets, and occasionally add short snarky comments based on the conversation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jofiction918](https://clawhub.ai/user/jofiction918) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to add a lightweight ASCII pet companion to an agent conversation, including pet generation, status display, direct interaction, and occasional personality-driven commentary. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad trigger words and probability-based interjections may make the pet appear when a user did not intend to summon it. <br>
Mitigation: Use explicit commands such as /buddy and /stats when predictable behavior is preferred, and disable or adjust random interjections in deployments that require quiet operation. <br>
Risk: The skill keeps pet attributes in a local JSON state file. <br>
Mitigation: Keep the state file scoped to non-sensitive pet data and review local file changes before sharing, syncing, or reusing the workspace. <br>
Risk: Generating a new pet runs the bundled local Node script. <br>
Mitigation: Review the included generator script before deployment and run it only from the trusted skill artifact. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jofiction918/flicker) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown text with ASCII art, short pet replies, pet-stat summaries, and local command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May keep a scoped local pet JSON state file and run the included Node generator when creating a pet.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
