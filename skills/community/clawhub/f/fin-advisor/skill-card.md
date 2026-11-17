## Description:

Fin Advisor helps personal investors analyze, compare, and evaluate funds using external fund-data services and compliance-oriented response rules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lovelcp](https://clawhub.ai/user/lovelcp)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to answer fund-analysis, fund-comparison, fee, market-news, recommendation, and trading-decision questions for personal investors. It is designed for fund-related topics and includes compliance prompts for investment-advice scenarios.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports that the skill may store financial preferences or profile details in USER.md without enough consent or scoping.

Mitigation: Require explicit user consent before saving financial preferences, keep stored profile data minimal, and provide a clear way to update or remove saved preferences.

Risk: The security review reports shell and external-service patterns, including a slot-filling service URL and token path, without enough transport or host restrictions.

Mitigation: Restrict external calls to trusted HTTPS hosts, remove or tightly scope slot-filling service configuration before deployment, and prefer structured MCP invocation over shell command strings for user-provided fund names or search text.

Risk: The skill provides fund recommendations and trading-decision support, which can create misleading or unsuitable financial guidance if data is stale, incomplete, or over-interpreted.

Mitigation: Use only authoritative fund-data service results, preserve required data context, avoid independent calculations or future-performance predictions, and include the required investment-risk disclaimer.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lovelcp/skills/fin-advisor)
- [Compliance rules](references/compliance.md)
- [Fund advisory domain knowledge](references/domain-knowledge.md)
- [Output guide](references/output-guide.md)
- [Tool guide](references/tool-guide.md)
- [Professional persona](references/personas/professional.md)
- [Friendly persona](references/personas/friendly.md)
- [Data-driven persona](references/personas/data-driven.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown responses with tables, citations, fund-analysis prose, and risk disclosures]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Financial data should include timestamp, metric name, value, and subject; advice-oriented responses should include risk disclaimers.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
