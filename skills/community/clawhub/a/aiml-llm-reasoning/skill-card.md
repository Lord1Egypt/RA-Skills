## Description: <br>
Run AIMLAPI LLM and reasoning workflows through chat completions with retries, structured outputs, and explicit User-Agent headers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aimlapihello](https://clawhub.ai/user/aimlapihello) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to make AIMLAPI chat completion calls from an agent workflow, including reasoning options, structured JSON responses, retry behavior, and optional response file output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, system messages, and allowed extra JSON fields are sent to AIMLAPI. <br>
Mitigation: Avoid sending sensitive content unless AIMLAPI handling is acceptable for the use case. <br>
Risk: The skill requires an AIMLAPI API key and can read it from a file when --apikey-file is used. <br>
Mitigation: Prefer AIMLAPI_API_KEY and keep any API key file path intentional and access-controlled. <br>
Risk: The --output option can save full API responses to a chosen file. <br>
Mitigation: Use --output only for intended response files and review saved content before sharing or committing it. <br>


## Reference(s): <br>
- [AIMLAPI LLM notes](references/aimlapi-llm.md) <br>
- [AIMLAPI API base endpoint](https://api.aimlapi.com/v1) <br>
- [ClawHub skill page](https://clawhub.ai/aimlapihello/aiml-llm-reasoning) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Plain text or JSON, with optional full JSON response files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AIMLAPI_API_KEY; requests are sent to AIMLAPI chat completions with configurable retry, timeout, User-Agent, and whitelisted extra JSON fields.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
