## Description:

Analyze why AI assistants recommend competing products and improve public landing pages using Agentzia reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stoyan-stoyanov](https://clawhub.ai/user/stoyan-stoyanov)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and marketing teams use this skill to audit how AI assistants discover, evaluate, and compare a public product page, then make evidence-led page revisions and retest when authorized.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Public marketing material is sent to Agentzia and external providers; the workflow is unsuitable for secrets, private repository content, customer data, or confidential drafts.

Mitigation: Use only public or explicitly authorized marketing content and avoid secrets, private code, personal data, customer data, and confidential drafts.

Risk: Agentzia studies consume credits and may create avoidable spend if started without agreement or retried incorrectly.

Mitigation: Check available credits, obtain an explicit budget before new studies, reuse the same requestId after a lost response, and avoid unattended recurring tests.

Risk: Research outputs, scraped pages, and assistant recommendations can contain untrusted or unresolved claims.

Mitigation: Treat reports and participant output as evidence only, verify cited evidence against the current page, and preserve accurate product claims when editing.

## Reference(s):

- [Agentzia documentation](https://www.agentzia.dev/docs)
- [Agentzia MCP endpoint](https://www.agentzia.dev/mcp)
- [ClawHub skill listing](https://clawhub.ai/stoyan-stoyanov/skills/agentzia-optimize)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown with summaries, code changes, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include report links, supported findings, implemented changes, test coverage, and remaining uncertainty.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
