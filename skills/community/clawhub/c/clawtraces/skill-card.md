## Description: <br>
Collects local OpenClaw conversation records, converts eligible sessions into trajectory data, and submits them to a data collection service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[miracle](https://clawhub.ai/user/miracle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and data collection operators use this skill to scan local conversations, review eligible sessions, submit conversation traces, and optionally submit scrubbed workspace harness context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill submits full conversation traces and related OpenClaw context, which may include sensitive prompt or workspace information. <br>
Mitigation: Install and run only when the user is comfortable submitting those traces; review the listed sessions and submission confirmation prompts before upload. <br>
Risk: Harness submission can include SOUL.md, USER.md, memory, cron, and session metadata. <br>
Mitigation: Use the bundle-only review step and inspect the reported redactions before confirming upload. <br>
Risk: The environment check can change OpenClaw logging and reasoning settings and restart OpenClaw. <br>
Mitigation: Review the environment check output, especially reported fixes to OpenClaw configuration, before continuing collection. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/miracle/clawtraces) <br>
- [Publisher profile](https://clawhub.ai/user/miracle) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON result summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local trajectory, stats, prompt hint, session bundle, manifest, and workspace zip files before submission.] <br>

## Skill Version(s): <br>
2.0.8 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
