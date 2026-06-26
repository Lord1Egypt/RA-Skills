## Description: <br>
Automatically adjust OpenClaw's thinking level based on message complexity and persist low, medium, or high thinking modes across a session. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zpy0726](https://clawhub.ai/user/zpy0726) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to choose or persist an OpenClaw thinking level for a message or session, reducing repeated manual mode selection during multi-turn work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill launches the local OpenClaw CLI through a shell with user-provided text. <br>
Mitigation: Install only from a trusted publisher, review the command path before use, and prefer a corrected release that removes shell: true. <br>
Risk: Documentation is inconsistent about whether the skill uses v1 automatic analysis or v2 persistent mode switching. <br>
Mitigation: Confirm expected behavior in a test session before production use and prefer a release with aligned documentation and implementation. <br>
Risk: Broad trigger phrases and unvalidated session IDs may cause unexpected mode changes or session-state confusion. <br>
Mitigation: Use explicit commands, review session-id handling, and prefer a release that narrows triggers and validates session IDs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zpy0726/autothink) <br>
- [Project homepage](https://github.com/openclaw/openclaw-autothink) <br>
- [Publisher profile](https://clawhub.ai/user/zpy0726) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [CLI text and forwarded OpenClaw agent output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke the local openclaw command and persist thinking mode in process memory for the current session.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
