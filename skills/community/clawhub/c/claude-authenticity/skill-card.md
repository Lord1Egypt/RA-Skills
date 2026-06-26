## Description: <br>
Detect whether an API endpoint is backed by genuine Claude using weighted rule-based checks, and optionally extract provider-injected system prompts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[helloml0326](https://clawhub.ai/user/helloml0326) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to test Claude-compatible API endpoints, verify whether a provider appears to serve genuine Claude, compare model results, and inspect possible provider-injected prompts when authorized. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Endpoint testing sends API keys and prompts to the configured provider, which can expose credentials or sensitive tenant data if used carelessly. <br>
Mitigation: Use only authorized endpoints with disposable or least-privilege API keys, and avoid production tenants unless testing has been approved. <br>
Risk: The optional prompt-extraction workflow can reveal provider-injected prompts, thinking traces, and responses that may be confidential or sensitive. <br>
Mitigation: Enable prompt extraction only with explicit permission from the provider or owner, and handle extracted prompts and responses as sensitive data. <br>


## Reference(s): <br>
- [claude-verify](https://github.com/molloryn/claude-verify) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces endpoint test configuration, an httpx-based Python script, authenticity scores, verdicts, check details, and optional prompt-extraction results.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
