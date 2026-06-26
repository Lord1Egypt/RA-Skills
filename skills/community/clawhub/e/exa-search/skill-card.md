## Description: <br>
Use Exa (exa.ai) Search API to search the web and return structured results (title/url/snippet/text) via a local Node script. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xinhai-ai](https://clawhub.ai/user/xinhai-ai) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external users use this skill to run Exa-backed web searches from an agent workflow, returning structured result JSON and optional page text or highlights for user-requested searches. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries are sent to Exa using the configured API key, so secrets, credentials, private business data, or regulated personal information could be exposed if included in queries. <br>
Mitigation: Use the skill only for intended Exa searches, keep EXA_API_KEY in the environment, and avoid sending secrets, credentials, private business data, or regulated personal information in search queries. <br>


## Reference(s): <br>
- [Exa documentation](https://exa.ai/docs) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [JSON responses from a Node script, with Markdown command guidance in the skill instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and EXA_API_KEY; the script limits count to 1..25 results and can optionally request page text or highlights.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
