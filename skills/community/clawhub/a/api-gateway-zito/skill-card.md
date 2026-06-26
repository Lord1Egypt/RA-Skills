## Description: <br>
Gateway universal para APIs. Conecta cualquier API REST/GraphQL con configuracion simple. Gestiona autenticacion, rate limiting y caching. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[miguelguerra200022-sudo](https://clawhub.ai/user/miguelguerra200022-sudo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to configure and call REST or GraphQL APIs through a common gateway that centralizes authentication, caching, rate limits, retries, logs, and tests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send data to external APIs and use service tokens without clearly defined safety boundaries. <br>
Mitigation: Restrict it to approved APIs and credentials, prefer read-only least-privilege tokens, and require explicit approval for POST or other write operations. <br>
Risk: API credentials, cached responses, logs, or proactive multi-agent use could expose secrets or trigger calls without clear permission. <br>
Mitigation: Avoid query-string secrets, enable credential redaction, define logging and cache cleanup rules, and disable proactive or multi-agent use unless authorization is clear. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and YAML configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference external API credentials and endpoint configuration supplied by the user.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
