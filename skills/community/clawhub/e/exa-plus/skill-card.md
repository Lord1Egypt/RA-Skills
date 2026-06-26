## Description: <br>
Neural web search via Exa AI for people, companies, news, research, code, domain-filtered search, and date-filtered search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jordyvandomselaar](https://clawhub.ai/user/jordyvandomselaar) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Agents and developers use this skill to run Exa-powered web searches and extract full text from URLs. It supports research, news, company, people, code, and document discovery workflows with optional filters for domains, categories, dates, and location. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries, URLs, and content-extraction requests are sent to Exa as a third-party service. <br>
Mitigation: Use a dedicated Exa API key and avoid submitting secrets, private internal URLs, confidential research targets, or personal data. <br>
Risk: The skill depends on a local Exa API key configured by the user. <br>
Mitigation: Protect the credential file and rotate or revoke the key if it is exposed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jordyvandomselaar/exa-plus) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration guidance, API calls] <br>
**Output Format:** [JSON API responses with command-line usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, and a user-provided Exa API key; search responses may include text snippets, highlights, and summaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
