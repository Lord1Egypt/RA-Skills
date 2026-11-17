## Description:

Aibuy helps agents query Shenzhen Shuibei jewelry wholesale listings, estimate gold product prices from live Shanghai gold quotes, and report current precious-metal and brand gold prices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[plabzzxx](https://clawhub.ai/user/plabzzxx)

### License/Terms of Use:

MIT-0

## Use Case:

External users and shopping assistants use this skill to look up Shuibei jewelry products, compare wholesale listing facts, estimate gold product reference prices, and check current gold or precious-metal quotes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Jewelry search terms are sent to the skill's remote inventory service and quote requests are sent to a live metal-pricing service.

Mitigation: Use product-focused search terms and avoid including personal, confidential, or payment information in queries.

Risk: Product, merchant, and metal-price outputs may be incomplete, stale, or inaccurate.

Mitigation: Present results as reference information and tell users to confirm specifications, availability, and final prices with the merchant before purchase.

## Reference(s):

- [Aibuy ClawHub skill page](https://clawhub.ai/plabzzxx/skills/aibuy)
- [Aibuy publisher profile](https://clawhub.ai/user/plabzzxx)
- [Jewelry inventory query API](https://wjxggrbemnbuhpmbyyws.supabase.co/functions/v1/query-jewelry)
- [Gold quote API](https://api-gold.aibuy.cloud/quoteCenter/realTime.htm)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown product summaries and price guidance, with optional JSON returned by bundled helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Product search defaults to 5 results and should not exceed 10 results per request.]

## Skill Version(s):

1.7.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
