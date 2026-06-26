## Description: <br>
Clawtrial Courtroom monitors AI agent conversations for behavioral violations and initiates local hearings with anonymized case record submission. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Assassin-1234](https://clawhub.ai/user/Assassin-1234) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to add behavioral oversight to ClawDBot or OpenClaw agents, including local violation evaluation, hearings, and management commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent no-confirm monitoring and evaluations can affect a real agent profile without repeated prompts. <br>
Mitigation: Install only on intended profiles, avoid autostart or cron setup unless explicitly desired, and verify uninstall removes symlinks, config entries, cron jobs, queue files, keys, and agent instruction edits. <br>
Risk: Conversation-derived case summaries may be published externally even when raw transcripts are not submitted. <br>
Mitigation: Confirm consent and anonymization settings before enabling public submissions, and disable API submission for sensitive agent profiles. <br>
Risk: Local queue files, signing keys, and behavior modifications can persist after installation. <br>
Mitigation: Protect agent profile storage, rotate keys after suspected compromise, clear queued cases during incident response, and confirm any SOUL.md or AGENTS.md additions are removed when uninstalling. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Assassin-1234/clawtrial) <br>
- [ClawTrial public case record](https://clawtrial.app) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [CLI output, local configuration changes, and agent-facing hearing and verdict text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can run as persistent monitoring automation and may queue or submit anonymized case summaries externally when enabled.] <br>

## Skill Version(s): <br>
1.0.9 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
