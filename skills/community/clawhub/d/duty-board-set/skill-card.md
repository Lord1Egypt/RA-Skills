## Description:

Turn user-supplied classroom duty roster slots and duty lines into a four-to-eight still duty board set.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beatra-ai](https://clawhub.ai/user/beatra-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External educators and classroom content creators use this skill to turn approved duty roster slots and duty lines into a consistent set of classroom duty board stills, with one generated image per named slot.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The shared Beatra Device Token grants broad account authority beyond this single classroom-board workflow.

Mitigation: Install only if that authorization is acceptable, keep the token private, and review the Beatra approval page and account console before use.

Risk: The bundled client checks for and applies package updates silently by default.

Mitigation: Use the documented `python3 scripts/mcp_client.py update --auto off` control before use if silent updates are not acceptable.

Risk: Paid image-generation tasks consume Beatra credits and final charges may differ from prepaid estimates.

Mitigation: Require the documented approval card before paid calls, use one request identity per still, and report `billing.net_charged_credits` from terminal task data.

Risk: Generated classroom-board text may be unreadable, inaccurate, or look like an official policy notice if not reviewed.

Mitigation: Review visible printed text against the confirmed pack list and avoid invented student names, school stamps, punishment rules, or official notices.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/beatra-ai/skills/duty-board-set)
- [Beatra skill homepage](https://beatra.ai/skills/duty-board-set)
- [Duty board pack workflow](references/workflow.md)
- [Installation and authentication](references/installation-and-auth.md)
- [Installation registration](references/installation-registration.md)
- [MCP connection](references/mcp-connection.md)
- [Tasks and results](references/tasks-and-results.md)
- [Billing, errors, and recovery](references/billing-errors-and-recovery.md)
- [Automatic updates and safety](references/automatic-updates-and-safety.md)
- [Uninstall and disconnect](references/uninstall-and-disconnect.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown prose with inline shell commands and JSON payloads; approved Beatra tasks return generated still-image artifacts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Plans four to eight stills by default, caps packs at eight, and uses one paid image generation request per approved duty slot.]

## Skill Version(s):

0.1.2 (source: server evidence release and artifact manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
