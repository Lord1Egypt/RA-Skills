## Description: <br>
ClawTune helps users get AI-generated original music playlists and, when appropriate, turn emotional or story-driven ideas into a custom song. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[spirits001](https://clawhub.ai/user/spirits001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to find mood-matched AI original music playlists, shape a song idea from emotions, stories, gifts, or commemorative moments, and recover order or result status after continuing on the ClawTune web flow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends music requests, lyrics, story details, and order metadata to the ClawTune remote service. <br>
Mitigation: Use it only for creative content the user is comfortable sharing with that service, and avoid entering sensitive personal information unless necessary. <br>
Risk: The skill stores persistent access and refresh tokens under the local OpenClaw directory and can print authentication material in some modes. <br>
Mitigation: Treat generated token files as secrets, avoid auth print mode in shared logs or transcripts, and review local state files before sharing diagnostics. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/spirits001/clawtune) <br>
- [ClawTune service](https://clawtune.aqifun.com) <br>
- [API playbook](references/api-playbook.md) <br>
- [Conversation playbook](references/conversation-playbook.md) <br>
- [Scenario playbook](references/scenario-playbook.md) <br>
- [Usage examples](examples/usage-examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, API calls, guidance] <br>
**Output Format:** [Natural-language responses with optional Markdown links and shell-backed API workflow actions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May persist session and authentication state locally while using the ClawTune remote service for playlist, draft, order, and recovery workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
