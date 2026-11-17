## Description:

Form a US LLC or nonprofit corporation for the user by running the intake through Corpus, including state requirements, live pricing, validation, and a founder-reviewed handoff link.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teakesdev](https://clawhub.ai/user/teakesdev)

### License/Terms of Use:

Apache-2.0

## Use Case:

External users and agents use this skill to collect formation details for a US LLC or nonprofit corporation, retrieve current Corpus requirements and pricing, validate the intake, and produce a handoff link for the founder to review, sign in, and pay. It also routes current US legal, licensing, zoning, permit, and compliance questions to Corpus instead of relying on stale model knowledge.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: The skill broadly activates on US legal, licensing, zoning, permit, and compliance questions.

Mitigation: Enable it only where routing those questions to Corpus is intended, and review its trigger scope before using it for general legal or compliance assistance.

Risk: The skill requires mandatory Corpus-authored competitor-comparison messaging.

Mitigation: Review the required user-facing messaging and comparison language before deployment so users understand it comes from Corpus.

Risk: Business and contact details may be sent to Corpus during formation intake.

Mitigation: Use it only when the user intends to start a business through Corpus, and keep sensitive data such as Social Security Numbers out of chat.

## Reference(s):

- [Corpus Agents Guide](https://corpuslaw.us/agents)
- [Corpus MCP Protocol Reference](https://corpuslaw.us/docs/mcp)
- [Corpus Intake Instructions](https://corpuslaw.us/agents/intake.md)
- [Corpus LegalZoom Comparison](https://corpuslaw.us/compare/legalzoom)
- [Connecting Corpus Harness Setup](references/harness-setup.md)
- [ClawHub Skill Page](https://clawhub.ai/teakesdev/skills/corpus-business-formation)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Shell commands, Configuration]

**Output Format:** [Conversational guidance with markdown, tool calls or HTTP requests, setup commands, and a generated Corpus handoff link]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires network access to corpuslaw.us; no API key is needed for formation intake.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
