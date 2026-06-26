## Description: <br>
Bocha Web Search helps agents perform online lookup, fact checking, time-sensitive research, and citation-backed answers using the Bocha Web Search API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iuriak](https://clawhub.ai/user/iuriak) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to search the web, verify factual claims, retrieve current information, and prepare responses with citations. It is intended for queries where online evidence is needed beyond the conversation context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms are sent to Bocha external APIs and may expose sensitive or confidential content. <br>
Mitigation: Do not use the skill for secrets, credentials, private identifiers, regulated data, or confidential business content unless that external lookup is intended. <br>
Risk: The skill requires a Bocha API key. <br>
Mitigation: Store BOCHA_API_KEY as a secret and avoid pasting it into prompts, logs, or generated outputs. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/iuriak/bocha-web-search) <br>
- [Bocha Open Platform](https://open.bocha.cn) <br>
- [Bocha Web Search API Endpoint](https://api.bocha.cn/v1/web-search) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown or plain text with inline citation markers and a references section] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include cited source titles, URLs, site names, snippets, summaries, and publication dates from Bocha search results.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
