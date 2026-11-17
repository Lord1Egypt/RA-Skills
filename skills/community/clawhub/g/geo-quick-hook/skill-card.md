## Description:

GEO Quickhook helps sales and marketing users compare a target brand against competitors across configured AI engines and produce a visibility comparison report for pre-sales conversations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hanwenyolo-dot](https://clawhub.ai/user/hanwenyolo-dot)

### License/Terms of Use:

MIT-0

## Use Case:

Sales teams, marketing consultants, and brand managers use this skill to gather brand, competitor, and keyword inputs, query a configured OpenAI-compatible LLM endpoint, and generate a competitive AI visibility report for pre-sales outreach.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Brand, competitor, and keyword inputs may be sent to the configured external LLM provider.

Mitigation: Use a vetted endpoint and avoid confidential customer data unless the data sharing path is approved.

Risk: Generated reports may be shared externally through Feishu.

Mitigation: Review the generated HTML report before sending it outside the organization.

Risk: The report can overstate five-engine coverage or present misleading competitive rankings.

Mitigation: Treat results as directional sales material and configure separate engine credentials and provenance when independent engine evidence is required.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/hanwenyolo-dot/skills/geo-quick-hook)
- [Publisher Profile](https://clawhub.ai/user/hanwenyolo-dot)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [Analysis, HTML, Files, Shell commands, Configuration guidance]

**Output Format:** [HTML report file with console summaries and setup/run commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes a dated GEO_QuickHook report to the user's Desktop and may be paired with screenshot delivery through Feishu.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
