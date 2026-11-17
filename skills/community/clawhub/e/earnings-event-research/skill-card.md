## Description:

Builds sourced pre- and post-earnings briefs by combining event, estimate, result, price, and SEC filing data through Crawlora.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

Analysts and researchers use this skill to prepare earnings previews or recaps with cited estimates, reported results, SEC filings, comparable periods, and bounded price changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Ticker and company queries, filing identifiers, and the API key are sent to Crawlora.

Mitigation: Use only when this data sharing is acceptable; avoid non-public or sensitive research topics and keep the API key in the environment.

Risk: Revised estimates, restated figures, and ambiguous earnings timing can make comparisons or price reactions misleading.

Mitigation: Record source dates and fiscal periods, verify comparable metrics and filing evidence, disclose gaps, and avoid attributing daily price changes to earnings without support.

## Reference(s):

- [Earnings event research endpoint reference](reference/endpoints.md)
- [ClawHub skill release](https://clawhub.ai/crawlora-org/skills/earnings-event-research)

## Skill Output:

**Output Type(s):** [Text, Markdown, Analysis]

**Output Format:** [Dated Markdown earnings brief with citations and an evidence ledger]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Separates estimates from reported figures and states fiscal periods, retrieval times, price windows, and material gaps.]

## Skill Version(s):

1.0.2 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
