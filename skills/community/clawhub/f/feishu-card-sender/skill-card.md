## Description: <br>
Sends Feishu interactive-card messages through Feishu OpenAPI using JSON templates, variable substitution, and optional poster upload, with callback handling for MoviePilot subscription actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dobbey](https://clawhub.ai/user/dobbey) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to send structured Feishu notifications to users or chats from reusable movie and TV card templates. It can also process Feishu card callbacks that create or update MoviePilot subscriptions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Callback automation can use local credentials and create MoviePilot subscriptions. <br>
Mitigation: Install only for deployments that explicitly need subscription callbacks, verify the MoviePilot base URL and credential mapping, and limit who can trigger subscription actions. <br>
Risk: Feishu callback handling depends on signature and encryption configuration. <br>
Mitigation: Configure and validate Feishu callback signature and encryption settings before accepting callbacks. <br>
Risk: Poster URLs and local callback state may expose sensitive data or pull untrusted content. <br>
Mitigation: Avoid untrusted poster URLs and treat local temporary databases, queues, and token caches as sensitive operational data. <br>


## Reference(s): <br>
- [Feishu callback response contract](references/feishu-callback-response-contract.md) <br>
- [MoviePilot subscription callback](references/subscribe-callback.md) <br>
- [Movie card template parameters](references/template-params.md) <br>
- [TV card template parameters](references/template-params-tv.md) <br>
- [Template variable example](references/vars.example.env) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, API Calls, JSON, Markdown] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON callback payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces Feishu card-send or callback-handling actions that depend on configured Feishu and MoviePilot credentials.] <br>

## Skill Version(s): <br>
1.1.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
