## Description: <br>
Track competitors automatically. Monitor pricing changes, new products, content updates, hiring, and marketing campaigns across competitor websites and social channels. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kennywayn3](https://clawhub.ai/user/kennywayn3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Business teams and market analysts use this skill to monitor named competitors or competitor URLs and receive reports about pricing, product, content, hiring, marketing, and SEO changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Competitor names, URLs, and lookup requests may be sent to an external ngrok API whose operator and retention practices are not documented. <br>
Mitigation: Review who operates the API, what data is retained, and whether the endpoint is approved before using the skill with sensitive business targets. <br>
Risk: API-key, paid-credit, and recurring monitoring expectations are under-disclosed. <br>
Mitigation: Confirm authentication, payment requirements, and how recurring monitoring can be limited or stopped before production use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kennywayn3/competitor-watch-pro) <br>
- [Company lookup API](https://extant-torrie-nonrepealable.ngrok-free.dev) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API calls, Guidance] <br>
**Output Format:** [Markdown reports with change summaries and recommended actions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports may be periodic and depend on competitor names, URLs, and monitoring cadence supplied by the user.] <br>

## Skill Version(s): <br>
1.0.4 (source: server evidence and SKILL.md frontmatter; package.json lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
