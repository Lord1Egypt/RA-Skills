## Description: <br>
Discover which free or low-cost AI APIs are reachable from the current environment, verify them safely, and recommend a task-to-provider routing plan. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xuxuclassmate](https://clawhub.ai/user/xuxuclassmate) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to check which AI API providers are reachable from the current environment, verify credentials only with approval, and choose a practical routing plan for chat, code, speech, or multimodal tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Outbound API probing may be disallowed or monitored in some environments. <br>
Mitigation: Confirm network policy before probing providers and use short, targeted reachability checks. <br>
Risk: Credential verification can expose API keys through notes, logs, or copied terminal output. <br>
Mitigation: Use temporary or low-privilege keys where possible, request credentials only after approval, and mask secrets in notes and logs. <br>
Risk: Provider availability, pricing, and quota information can change after a routing recommendation is made. <br>
Mitigation: Base recommendations on verified results from the current environment and re-check availability and quota before relying on a route. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xuxuclassmate/free-api-discovery) <br>
- [Groq API endpoint](https://api.groq.com) <br>
- [OpenRouter API endpoint](https://openrouter.ai/api/v1) <br>
- [DeepSeek API endpoint](https://api.deepseek.com) <br>
- [Mistral API endpoint](https://api.mistral.ai/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown with provider reachability notes, credential checks, routing recommendations, and optional code or shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include cost or quota notes, providers requiring credentials, and risks or missing coverage.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
