## Description: <br>
APIClaw provides an API platform overview for AI-powered commerce data infrastructure, including programmatic access to Amazon product, market, competitor, realtime ASIN, and review-analysis endpoints. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[christine-srp](https://clawhub.ai/user/christine-srp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to understand APIClaw capabilities, configure APICLAW_API_KEY, choose the right commerce data endpoint, and draft API requests for Amazon product research workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires APICLAW_API_KEY, giving the agent access to a third-party commerce data API. <br>
Mitigation: Install only when APIClaw access is intended, keep the key in an environment variable, and revoke or rotate the key when it is no longer needed. <br>
Risk: API calls consume credits. <br>
Mitigation: Review credit consumption in API responses and monitor account plans or pricing before running repeated or broad queries. <br>
Risk: Commerce data may have scope and freshness limits, including Amazon US coverage, lower-bound monthly sales estimates, and delayed non-realtime datasets. <br>
Mitigation: Label outputs with these data limits and use realtime product data only where current single-ASIN details are needed. <br>


## Reference(s): <br>
- [APIClaw OpenAPI Quick Reference](references/openapi-reference.md) <br>
- [APIClaw API Docs](https://api.apiclaw.io/api-docs) <br>
- [APIClaw Website](https://apiclaw.io) <br>
- [APIClaw API Keys](https://apiclaw.io/api-keys) <br>
- [APIClaw Pricing](https://apiclaw.io/pricing) <br>
- [ClawHub Skill Page](https://clawhub.ai/christine-srp/apiclaw-api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with endpoint descriptions, JSON request examples, and shell configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires APICLAW_API_KEY for live API use; generated guidance may include endpoint selection, request bodies, data caveats, and credit-usage notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
