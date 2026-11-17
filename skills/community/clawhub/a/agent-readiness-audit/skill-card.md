## Description:

Audits whether AI agents can use a product's docs, APIs, onboarding, errors, and discovery surfaces from a non-human user's perspective.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mohitagw15856](https://clawhub.ai/user/mohitagw15856)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, product teams, and documentation teams use this skill to audit whether public product surfaces are usable by AI agents and to prioritize fixes across discovery, docs, API/auth, errors, onboarding, transactions, and guardrails.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An audit may expose sensitive product information if private credentials, internal URLs, or confidential observed failures are supplied as inputs.

Mitigation: Provide only the sites, docs, APIs, and failures intended for assessment; share credentials only when authenticated-flow testing is explicitly in scope.

Risk: Findings can be misleading if the agent audits from memory or incomplete surface evidence instead of current product artifacts.

Mitigation: Fetch the actual public surfaces during the audit and require concrete artifact citations for every score below 3.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mohitagw15856/skills/agent-readiness-audit)
- [Project skill homepage](https://mohitagw15856.github.io/pm-claude-skills/skill/agent-readiness-audit.html)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown report with scores, findings tables, prioritized fixes, and a re-test protocol]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scores six audit surfaces on a 0-4 scale for a total of 24.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
