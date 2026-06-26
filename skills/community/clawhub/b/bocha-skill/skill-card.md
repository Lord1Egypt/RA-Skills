## Description: <br>
Searches the web with the Bocha AI Search API, with emphasis on Chinese-language web, image, and news results plus generated summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ypw757](https://clawhub.ai/user/ypw757) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw users can add Bocha-powered search to an agent for Chinese-language research, current-events lookup, image discovery, and summarized web results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries are sent to Bocha using the user's BOCHA_API_KEY. <br>
Mitigation: Install only if sending those queries to Bocha is acceptable, and use a user-owned API key with appropriate account controls. <br>
Risk: The bundled publishing documentation includes an API key value that should be treated as exposed. <br>
Mitigation: Do not reuse the shown key; rotate or revoke any real key that matches it before using the skill. <br>
Risk: Publishing helpers can handle ClawdHub credentials or publish the skill when run. <br>
Mitigation: Avoid running publish.sh unless publication is intended, and prefer browser login or a non-echoing token flow for credentials. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ypw757/bocha-skill) <br>
- [Bocha AI Open Platform](https://open.bocha.cn/) <br>
- [Bocha API Documentation](https://bocha-ai.feishu.cn/wiki/RXEOw02rFiwzGSkd9mUcqoeAnNK) <br>
- [OpenClaw Documentation](https://docs.openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, JSON, guidance] <br>
**Output Format:** [Markdown search results with an embedded raw JSON block] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires BOCHA_API_KEY and Node.js; result count is constrained to 1-50.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and scripts/package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
