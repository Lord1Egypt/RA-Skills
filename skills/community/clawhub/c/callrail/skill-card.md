## Description: <br>
CallRail API integration with managed OAuth for tracking and analyzing phone calls, managing tracking numbers, companies, and tags. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agents use this skill to work with CallRail accounts through Maton's managed OAuth proxy, including reading call, account, company, tracker, and tag data. They can also manage tags and call metadata when the user explicitly approves the target resource and intended effect. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires MATON_API_KEY and routes CallRail data through Maton, which can expose sensitive CallRail records if the key or connection is mishandled. <br>
Mitigation: Install only if Maton is trusted, protect MATON_API_KEY, and scope requests to the intended CallRail account. <br>
Risk: Write operations can modify CallRail calls, tags, or account resources. <br>
Mitigation: Require explicit user approval and verify the exact account, resource, connection ID, and intended effect before create, update, or delete requests. <br>
Risk: Multiple active CallRail connections can cause requests to target the wrong account. <br>
Mitigation: Use the Maton-Connection header with a specific connection ID when more than one CallRail connection is active. <br>


## Reference(s): <br>
- [CallRail Skill on ClawHub](https://clawhub.ai/byungkyu/callrail) <br>
- [Publisher Profile](https://clawhub.ai/user/byungkyu) <br>
- [CallRail API Documentation](https://apidocs.callrail.com/) <br>
- [CallRail Help Center API](https://support.callrail.com/hc/en-us/sections/4426797289229-API) <br>
- [CallRail API Rate Limits](https://apidocs.callrail.com/#rate-limiting) <br>
- [Maton](https://maton.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python, JavaScript, shell/API endpoint examples, and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access and MATON_API_KEY; write operations require explicit user approval before execution.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
