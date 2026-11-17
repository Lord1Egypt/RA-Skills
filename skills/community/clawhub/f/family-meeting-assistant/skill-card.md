## Description:

家语（Jiayu） helps families record daily moments, organize weekly and monthly memory reports, track growth, preserve elder stories, and support calmer family discussions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[perrykono-debug](https://clawhub.ai/user/perrykono-debug)

### License/Terms of Use:

MIT-0

## Use Case:

External families and household coordinators use this skill to capture family memories, prepare periodic summaries, interview elders, track children's growth, and structure family decisions without replacing human consent or judgment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Family records may contain sensitive personal details about adults, children, elders, addresses, finances, schools, or private decisions.

Mitigation: Agree on who may contribute and read records, avoid unnecessary identifiers or child details, and require human approval before recording or sharing sensitive information.

Risk: Configured WeCom or Tencent Docs destinations could expose family records beyond the intended audience.

Mitigation: Review all messaging and document destinations before use, keep external sharing opt-in, and require approval before sending family chronicles or private records outside the workspace.

Risk: The artifact stores records locally and does not define encryption or retention controls.

Mitigation: Protect workspace access, keep only necessary family data, and establish household retention and deletion practices before regular use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/perrykono-debug/skills/family-meeting-assistant)
- [Skill definition](artifact/SKILL.md)
- [Jiayu work specification](artifact/references/agents.md)
- [Jiayu behavior guide](artifact/references/soul.md)
- [Jiayu tool configuration](artifact/references/tools.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown records, JSON configuration examples, and concise conversational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local family memory files and optional messaging or document integration configuration when users provide destinations.]

## Skill Version(s):

2.0.0 (source: server release evidence, artifact/_meta.json, SKILL.md, released 2026-06-07)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
