## Description: <br>
Manual productivity assistant for morning briefs and daily summaries. Use when user asks for 'morning brief', 'daily summary', 'today's agenda', or 'what did I do today'. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kneijenhuijs](https://clawhub.ai/user/kneijenhuijs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Knowledge workers and OpenClaw users use this skill to request morning briefs, agenda and task summaries, and end-of-day summaries. It can combine local profile, intention, workspace activity, and optional Todoist or calendar information into concise productivity updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read personal OpenClaw profile files, workspace activity, chat context, and optional Todoist or calendar data. <br>
Mitigation: Install only when that local productivity context is acceptable for the assistant to use, and enable only the optional integrations the user wants exposed. <br>
Risk: Daily summaries are saved under ~/.openclaw/workspace/memory and may contain sensitive personal or work information. <br>
Mitigation: Review or delete memory files that should not persist, and avoid adding sensitive details to end-of-day check-ins. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kneijenhuijs/clawflow-free) <br>
- [README](artifact/README.md) <br>
- [Installation guide](artifact/INSTALL.md) <br>
- [Changelog](artifact/CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown messages, local Markdown summary files, and optional shell command invocations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads local OpenClaw workspace files; optional Todoist and calendar CLI integrations are skipped when unavailable.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and CHANGELOG, released 2026-04-24) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
