## Description:

Alibaba International Station weekly business report analysis skill. Retrieves store weekly report data via browser session, validates, and presents structured diagnostics with on-demand deep report access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[simoncai519](https://clawhub.ai/user/simoncai519)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers and e-commerce operators use this skill to retrieve Alibaba International Station weekly store reports, review store metrics, diagnostics, and merchant tasks, and ask follow-up questions about detailed report data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose private Alibaba store analytics, report tokens, merchant tasks, and business diagnostics in the agent conversation.

Mitigation: Run it only with Alibaba accounts whose business metrics may be shown to the agent, and avoid using it on sensitive accounts unless that disclosure is acceptable.

Risk: The workflow depends on the user's logged-in Alibaba browser session to retrieve report data.

Mitigation: Confirm the active Alibaba account before running the skill and stop if the browser is logged in to the wrong account.

Risk: Missing or unavailable Alibaba report data can lead to incomplete analysis.

Mitigation: Use the skill's validation and fallback behavior; provide screenshots or key metrics manually when the weekly report system has no data.

## Reference(s):

- [Workflow details](references/workflow.md)
- [ClawHub skill page](https://clawhub.ai/simoncai519/skills/alibaba-store-analysis)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown with metric tables, diagnostic summaries, task bullet lists, report links, and concise answers to follow-up questions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the user's authenticated Alibaba browser session and avoids proactively dumping the full report JSON after retrieval.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
