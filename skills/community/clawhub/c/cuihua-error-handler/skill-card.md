## Description: <br>
Cuihua Error Handler helps agents analyze JavaScript and TypeScript projects for weak or missing error handling and draft try/catch, retry, circuit breaker, fallback, logging, and rollback patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[supermario11](https://clawhub.ai/user/supermario11) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to find missing or weak error handling in code and draft resilient recovery patterns for application functions, API routes, database operations, and external service calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated logging or error responses may expose sensitive request bodies, arguments, tokens, payment details, stack traces, or raw internal errors. <br>
Mitigation: Review generated changes before applying them and redact sensitive data from logs, responses, and error payloads. <br>
Risk: Generated retries, fallbacks, circuit breakers, or rollbacks may change production behavior in unsafe ways if applied without domain review. <br>
Mitigation: Validate recovery behavior for auth, payment, database, and API-route code before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/supermario11/cuihua-error-handler) <br>
- [README](README.md) <br>
- [Skill definition](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JavaScript code snippets, CLI commands, configuration examples, and coverage reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js; generated code and reports should be reviewed before use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
