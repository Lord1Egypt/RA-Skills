## Description: <br>
Uses the Baidu AI Search Engine (BDSE) for web search through a CLI curl request without requiring Python. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zfeng1982](https://clawhub.ai/user/zfeng1982) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to issue Baidu web search requests from a shell environment using a prepared JSON request body and a BAIDU_API_KEY. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends the configured query, result count, date filters, and BAIDU_API_KEY-authenticated request to Baidu. <br>
Mitigation: Review search_request.json before use and confirm that the configured request is intended for the Baidu API. <br>
Risk: Authentication fails if BAIDU_API_KEY is missing or incorrect. <br>
Mitigation: Set BAIDU_API_KEY in the shell environment and verify the key before running the curl command. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zfeng1982/baidu-search-cli) <br>
- [Publisher profile](https://clawhub.ai/user/zfeng1982) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses search_request.json as the request template and requires BAIDU_API_KEY for Baidu API authentication.] <br>

## Skill Version(s): <br>
1.0.5 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
