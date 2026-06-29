## Description: <br>
An enterprise procurement assistant that helps agents search tender, procurement, bid-award, company, supplier, competitor, market, brand, and pricing data through the Zhiliao Biaoxun/Bilianwang APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhiliaobiaoxun](https://clawhub.ai/user/zhiliaobiaoxun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Procurement, sales, and business-development teams use this skill to find tenders and awards, assess suppliers, identify potential bidders, analyze company relationships, and review procurement market trends. Agents may also use it to produce procurement research summaries backed by API results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review says the skill can silently register a device account and transmit device and user metadata to the provider when no API key is configured. <br>
Mitigation: Install only when this provider data sharing is acceptable; prefer setting ZLBX_API_KEY manually to avoid the automatic registration path. <br>
Risk: The security review says the skill can persist an API key under ~/.zlbx. <br>
Mitigation: Review local ~/.zlbx/config.json handling, protect the file as a credential, and remove it when the account should no longer be used. <br>
Risk: The security guidance highlights contact-data and recharge-link workflows that may affect privacy or account billing. <br>
Mitigation: Review contact-data responses and any recharge or auto-login links before acting on them or sharing them with users. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhiliaobiaoxun/skills/enterprise-tender-search-bilianwang) <br>
- [Tender search API reference](references/api-search.md) <br>
- [Company analysis API reference](references/api-company.md) <br>
- [Market analysis API reference](references/api-market.md) <br>
- [Automatic registration flow](references/auto-register.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, configuration, guidance] <br>
**Output Format:** [Markdown summaries with JSON API request and response details when useful] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read ZLBX_API_KEY or ~/.zlbx/config.json, call provider APIs, and persist an API key under ~/.zlbx when auto-registration is used.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
