## Description: <br>
豆包WebSearch submits search queries to Redfox's Doubao WebSearch service and polls until a structured JSON result is available. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[redfox-data](https://clawhub.ai/user/redfox-data) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill when an agent needs up-to-date web search results from Doubao through the Redfox API. It is suitable for retrieving current information and presenting summarized answers with source references. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries and the Redfox API key are sent to the Redfox/Doubao service. <br>
Mitigation: Avoid submitting secrets, personal data, or confidential business content as search queries, and configure REDFOX_API_KEY only through the intended environment or agent configuration. <br>
Risk: Routine local questions could be sent to an external search service if the skill is invoked too broadly. <br>
Mitigation: Prefer explicit invocations for web search tasks so external calls are limited to cases where real-time search is needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/redfox-data/skills/doubao-websearch) <br>
- [Redfox API key settings](https://redfox.hk/settings/api-keys?source=clawhub) <br>
- [Redfox Doubao WebSearch API endpoint](https://redfox.hk/story/api/doubaoSearch) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and structured JSON search results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses REDFOX_API_KEY for authentication, emits polling progress to stderr, and writes completed search results or error JSON to stdout.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
