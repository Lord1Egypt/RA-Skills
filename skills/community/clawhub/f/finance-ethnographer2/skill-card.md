## Description: <br>
Privacy-first UX research ethnographer for OpenClaw with a personal-finance lens that observes consented usage, logs structured behavioral events, and compiles sanitized observed-behavior and interpretation reports for participant review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dflam1](https://clawhub.ai/user/dflam1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External OpenClaw users and research participants use this skill to collect consent-based UX research signals about personal-finance workflows. It records abstracted behavioral events, delegates redaction to a sanitizer subagent, and presents sanitized pulse reports for review before any sharing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill persistently records broad OpenClaw usage and creates finance-related scores and hypothesis reports. <br>
Mitigation: Require explicit participant consent before logging, keep retention low, allow pause/stop/delete controls, and review every sanitized report before sharing. <br>
Risk: Reports may contain sensitive personal or financial context if abstraction or redaction fails. <br>
Mitigation: Keep raw reports in memory only, delegate redaction to the sanitizer subagent, enable aggressive redaction by default, and require participant review before export or email. <br>
Risk: Finance-related profiling and general usage logging can create privacy concerns even when raw values are not stored. <br>
Mitigation: Use the configurable general-usage logging control where available, keep the default retention window limited, and use delete controls for unwanted date ranges. <br>
Risk: Email sharing could send sanitized reports to the wrong recipient. <br>
Mitigation: Require a participant-supplied recipient, validate the email format, confirm the recipient, and wait for explicit send approval. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/dflam1/finance-ethnographer2) <br>
- [Publisher Profile](https://clawhub.ai/user/dflam1) <br>
- [Skill Instructions](artifact/SKILL.md) <br>
- [Sanitizer Subagent](artifact/sanitizer/SKILL.md) <br>
- [Settings Schema](artifact/settings.schema.json) <br>
- [Test Plan](artifact/test-plan.md) <br>
- [Example Pulse Output](artifact/example-output.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, files, configuration, guidance] <br>
**Output Format:** [Markdown reports, JSON event and manifest records, local files, and participant-facing guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces scheduled sanitized pulse reports, redaction manifests, settings/state files, and exportable report packages.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and OpenClaw metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
