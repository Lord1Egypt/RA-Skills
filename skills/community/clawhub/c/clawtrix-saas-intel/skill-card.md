## Description: <br>
Surfaces up to three ClawHub skill recommendations for SaaS-focused agents across auth, billing, onboarding, customer lifecycle, SaaS product patterns, and n8n workflow conversion. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nicope](https://clawhub.ai/user/nicope) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and SaaS teams use this skill to discover a short, product-specific set of ClawHub skills for billing, authentication, onboarding, customer lifecycle, product analytics, and n8n workflow conversion. It reads the agent mission, searches ClawHub, scores candidates, and writes a top-three recommendation report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads the agent mission and can write a local report containing context about the product domain, stack, business model, and installed skills. <br>
Mitigation: Review SOUL.md for sensitive content before use and inspect the generated memory report before sharing or retaining it. <br>
Risk: Recommended downstream skills for billing, auth, or customer-data workflows may carry higher risk than this discovery skill. <br>
Mitigation: Review each recommended skill separately and run a security audit before installing skills that touch payment, identity, or customer data. <br>
Risk: The skill queries ClawHub search endpoints, which can disclose the SaaS capability areas being investigated. <br>
Mitigation: Use only with search terms that are acceptable to send to ClawHub and avoid including secrets or customer-specific identifiers in queries. <br>


## Reference(s): <br>
- [Clawtrix Saas Intel on ClawHub](https://clawhub.ai/nicope/clawtrix-saas-intel) <br>
- [ClawHub billing skill search](https://clawhub.ai/api/v1/search?q=stripe+billing&limit=10) <br>
- [ClawHub auth skill search](https://clawhub.ai/api/v1/search?q=auth+identity+saas&limit=10) <br>
- [ClawHub onboarding skill search](https://clawhub.ai/api/v1/search?q=onboarding+activation&limit=10) <br>
- [ClawHub n8n workflow skill search](https://clawhub.ai/api/v1/search?q=n8n+workflow&limit=10) <br>
- [ClawHub product analytics skill search](https://clawhub.ai/api/v1/search?q=product+analytics+retention&limit=10) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, API Calls] <br>
**Output Format:** [Markdown report with inline shell commands and JSON API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Limits recommendations to a top-three report saved under memory/reports/saas-intel-YYYY-MM-DD.md.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
