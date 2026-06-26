## Description: <br>
A language list retrieval skill based on the "Bee Website Builder" Open API. It is used to obtain the list of enabled site languages and provide the dependency data source for the `language` parameter used by other skills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mouxiaming](https://clawhub.ai/user/mouxiaming) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external agents use this skill to fetch enabled Bee Website Builder site languages for language filtering, selectable parameters, and workflow dependency data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Bee API key and sends it to the Bee Website Builder API. <br>
Mitigation: Install only if you trust the Bee Website Builder endpoint, supply the key through an environment variable or secret store, avoid exposing it in chats or logs, and rotate it if exposed. <br>


## Reference(s): <br>
- [Bee Website Builder Open API](https://open.tradew.com) <br>
- [Bee Languages API Endpoint](https://platform.tradew.com/openapis/languages) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON] <br>
**Output Format:** [JSON object with status, msg, and optional data.list language records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Bee API key supplied as api_key or via BEE_API_KEY.] <br>

## Skill Version(s): <br>
2.0.4 (source: server release evidence and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
