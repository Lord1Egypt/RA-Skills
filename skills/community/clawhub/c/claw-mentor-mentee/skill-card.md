## Description: <br>
Claw Mentor Mentee connects an OpenClaw agent to ClawMentor so it can receive mentor configuration updates and operational guidance, analyze compatibility locally, and apply only user-approved changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clawmentorai](https://clawhub.ai/user/clawmentorai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and developers use this skill to subscribe to ClawMentor mentors, review mentor-proposed setup changes, and integrate technical guidance and operating practices with explicit approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Remote mentor content and local persistent files can influence core agent behavior. <br>
Mitigation: Install only if you trust ClawMentor and subscribed mentors, and review every proposed change before approving it. <br>
Risk: Changes to HEARTBEAT.md, AGENTS.md, SOUL.md, IDENTITY.md, installed skills, cron behavior, or security posture could alter how the agent operates. <br>
Mitigation: Inspect these categories carefully during approval and reject changes that do not match the desired agent behavior. <br>
Risk: Stored mentor state and guidance may continue shaping future agent behavior. <br>
Mitigation: Periodically inspect or delete ~/.openclaw/claw-mentor/state.json, stored mentor files, and mentor-guidance.md when they no longer reflect user intent. <br>


## Reference(s): <br>
- [ClawMentor homepage](https://clawmentor.ai) <br>
- [ClawHub skill page](https://clawhub.ai/clawmentorai/claw-mentor-mentee) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/clawmentorai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and API-call instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CLAW_MENTOR_API_KEY; stores local state and proposes workspace guidance changes for user approval.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
