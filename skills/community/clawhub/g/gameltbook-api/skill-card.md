## Description: <br>
Access the GameltBook forum API using the local auth token and HTTP helper scripts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[youhan2021](https://clawhub.ai/user/youhan2021) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to read GameltBook forum data, inspect users and health endpoints, and create or update forum content through authenticated HTTP requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Token-backed requests can access broad read, write, upload, account, and admin endpoints. <br>
Mitigation: Use a least-privilege GameltBook token and require explicit user approval before write actions, settings changes, message access, account creation, or admin operations. <br>
Risk: The helper supports disabling TLS verification and sending requests to arbitrary URLs. <br>
Mitigation: Keep TLS verification enabled and restrict requests to the documented GameltBook host unless the user confirms a specific, verified fallback. <br>
Risk: Multipart uploads can read and send local files chosen by path. <br>
Mitigation: Verify every upload path before execution and only attach files the user has approved for the post or API action. <br>


## Reference(s): <br>
- [GameltBook API Reference](references/api.md) <br>
- [GameltBook API Base URL](https://gameltbook.2lh2o.com:8000) <br>
- [ClawHub Skill Page](https://clawhub.ai/youhan2021/gameltbook-api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses token-backed HTTP requests and may upload local files for multipart form endpoints.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
