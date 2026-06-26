## Description: <br>
Web search for AI agents via the Ceramic Search API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ceramicai](https://clawhub.ai/user/ceramicai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use Ceramic Search to retrieve current web results, rewrite search requests into keyword queries, and produce cited answers from Ceramic result descriptions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries and the Ceramic API key are sent to Ceramic-operated services. <br>
Mitigation: Use the skill only when that external data flow is approved, and avoid sending secrets, confidential business data, or sensitive personal information. <br>
Risk: The setup documentation recommends forcing all web searches through this plugin and disabling other search tools. <br>
Mitigation: Treat that configuration as an optional administrative policy, and keep alternative search tools available unless an owner explicitly approves the restriction. <br>
Risk: Search results may be incomplete, stale, or misleading when the query is too broad or result descriptions lack enough context. <br>
Mitigation: Refine weak searches, cite only sources used in the answer, and review source URLs before relying on high-impact results. <br>


## Reference(s): <br>
- [Ceramic](https://ceramic.ai) <br>
- [Ceramic API keys](https://platform.ceramic.ai/keys) <br>
- [ClawHub skill page](https://clawhub.ai/ceramicai/ceramic-search) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Plain text or Markdown with numbered source references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search requests require Ceramic API access; result descriptions default to 3000 characters and may be requested up to 8000.] <br>

## Skill Version(s): <br>
1.0.8 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
