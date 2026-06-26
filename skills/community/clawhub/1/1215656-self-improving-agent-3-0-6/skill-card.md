## Description: <br>
Captures learnings, errors, and corrections so agents can log failures, user feedback, feature requests, knowledge gaps, and reusable practices for future improvement. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1215656](https://clawhub.ai/user/1215656) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to capture operational learnings, command failures, user corrections, and recurring best practices in structured markdown logs that can inform future sessions or promoted guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent learning logs can capture secrets, personal data, proprietary code, raw transcripts, or unredacted command and API output. <br>
Mitigation: Keep .learnings private or gitignored unless team sharing is intentional, and redact sensitive details before logging. <br>
Risk: Promoting entries into agent memory or instruction files can make incorrect, stale, or overly broad guidance persistent across future sessions. <br>
Mitigation: Review every promotion, keep promoted rules narrow and evidence-based, and update or remove stale guidance during periodic review. <br>
Risk: Optional hook reminders can inject learning-capture guidance into agent sessions and affect workflow behavior. <br>
Mitigation: Enable hooks only when persistent learning is intended, scope them to the intended workspace, and review hook configuration before deployment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/1215656/1215656-self-improving-agent-3-0-6) <br>
- [OpenClaw Integration](references/openclaw-integration.md) <br>
- [Hook Setup Guide](references/hooks-setup.md) <br>
- [Examples](references/examples.md) <br>
- [Agent Skills specification](https://agentskills.io/specification) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces structured learning, error, and feature-request entries intended for local review and optional promotion into agent memory files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact metadata reports 3.0.6) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
