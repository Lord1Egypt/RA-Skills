## Description:

Uses the ClawEC API to run Amazon keyword research, compare monthly searches, purchase rate, supply-demand ratio, and blue-ocean index, and optionally return AI interpretation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anyunzhong](https://clawhub.ai/user/anyunzhong)

### License/Terms of Use:

MIT-0

## Use Case:

External users, Amazon sellers, and ecommerce operators use this skill to submit keyword research criteria to ClawEC and receive keyword opportunity data and optional AI analysis for product and market selection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends Amazon keyword research parameters to the ClawEC API using the user's CLAWEC_API_KEY.

Mitigation: Install only when ClawEC is trusted for the intended data, keep API keys out of source files, and provide the key through the CLAWEC_API_KEY environment variable.

Risk: Recent keyword-search logs are account-scoped, so sharing one API key among mutually untrusted users could expose prior searches.

Mitigation: Use separate ClawEC API keys for separate users or trust boundaries.

Risk: The polling helper may select the wrong similar record during concurrent searches with matching region, month, keyword, and AI settings.

Mitigation: Avoid concurrent identical searches under the same account or verify the returned log identifier and parameters before relying on the result.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/anyunzhong/skills/clawec-amazon-keyword-selection)
- [ClawEC API base](https://www.clawec.com/api)
- [ClawEC API key page](https://www.clawec.com/api-key?source=q-clawhub)
- [ClawEC keyword research search endpoint](https://www.clawec.com/api/aigc/ec/amazon/keyword_research/search)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown summaries with JSON API responses and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include keyword opportunity tables, search criteria, AI interpretation text, log identifiers, and API status messages.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
