## Description:

Helps agents guide business-security and anti-cheating analysis from workflow clarification through risk modeling and solution guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jshdcn](https://clawhub.ai/user/jshdcn)

### License/Terms of Use:

MIT-0

## Use Case:

Business, fraud-risk, and trust-and-safety teams use this skill to clarify a business workflow, model it with a three-flow method, identify cheating and fraud risks, and draft mitigation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive business workflow details may be sent to or embedded in external hdconsultatio.com services.

Mitigation: Use redacted or generic workflow descriptions unless the publisher provides clear consent, retention, and data-handling guarantees.

Risk: The skill describes an API-key flow for an external RAG service.

Mitigation: Avoid entering secrets directly in chat and confirm API-key handling, scoping, and rotation practices before use.

Risk: Risk-control recommendations may be incomplete or unsuitable for a specific business without review.

Mitigation: Have qualified business-security or fraud-risk reviewers validate the model, assumptions, and mitigations before operational use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jshdcn/skills/anti-cheating-assistant)
- [Risk Problems Table](artifact/references/risk-problems-table.md)
- [Solution List](artifact/references/solution-list.md)
- [Three Flow Graph Analysis Script](artifact/scripts/three_flow_graph_analysis.py)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and structured text with optional code, shell command, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include business workflow summaries, three-flow tables, risk lists, mitigation recommendations, and external-service setup guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
