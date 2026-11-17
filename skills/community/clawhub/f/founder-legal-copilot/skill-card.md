## Description:

Legal copilot that guides founders from incorporation to exit with 27 legal deliverables across 5 startup phases.

This skill is ready for commercial/non-commercial use.

## Publisher:

[danillo7](https://clawhub.ai/user/danillo7)

### License/Terms of Use:

MIT-0

## Use Case:

Startup founders and their advisors use this skill to draft founder legal documents, review contracts, run legal readiness checks, and prepare lightweight due diligence reports before fundraising or transactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Legal documents, diligence queries, and optional voice narration content may be sent to third-party services.

Mitigation: Use only with data approved for those services, scrub sensitive personal information where possible, and confirm service terms before deployment.

Risk: Deal history and legal reports may be persisted in Redis across sessions.

Mitigation: Confirm retention, deletion, and access controls before storing confidential deal data.

Risk: The documented local Redis command can expose an unauthenticated service if used as written.

Mitigation: Bind Redis to localhost or a private network, require authentication, and avoid exposing the port publicly.

Risk: Generated legal analysis and documents may be incomplete, non-standard, or incorrect.

Mitigation: Treat outputs as drafts and have a licensed attorney review documents before execution.

## Reference(s):

- [Founder Legal Copilot on ClawHub](https://clawhub.ai/danillo7/skills/founder-legal-copilot)
- [LegalKit](https://legalkit.legal)
- [YC SAFE Documents](https://ycombinator.com/documents)
- [NVCA Model Legal Documents](https://nvca.org/model-legal-documents)
- [Cooley GO](https://cooleygo.com)
- [Orrick Start-Up Forms Library](https://orrick.com/practices/startups)
- [Series Seed](https://seriesseed.com)
- [SEC EDGAR](https://sec.gov/edgar)
- [Apify MCP](https://mcp.apify.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON risk reports, document drafts, checklists, and command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include legal disclaimers, prioritized risk flags, remediation steps, and optional multilingual or voice-ready report content.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
