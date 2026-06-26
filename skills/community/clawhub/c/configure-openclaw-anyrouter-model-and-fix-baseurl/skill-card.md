## Description: <br>
Helps agents configure OpenClaw to use the AnyRouter Claude Opus model, align related ClaudeCode settings, and troubleshoot baseUrl, protocol, authentication, and fallback behavior with logs and live checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[can4hou6joeng4](https://clawhub.ai/user/can4hou6joeng4) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to merge AnyRouter provider settings into OpenClaw, set the main agent model to anyrouter/claude-opus-4-6, and verify whether requests are actually reaching the intended provider. It also helps diagnose 403, 404, 500, protocol endpoint, API key, and fallback issues across OpenClaw and ClaudeCode configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Model routing or local agent configuration changes can break the user's working OpenClaw or ClaudeCode setup. <br>
Mitigation: Ask for a diff before applying changes, back up openclaw.json and ~/.claude/settings.json, and require approval before restarts. <br>
Risk: API keys can be exposed or misconfigured when provider settings are edited or tested. <br>
Mitigation: Prefer environment-variable API keys over plaintext, confirm that variables resolve correctly, and avoid printing secrets in logs or responses. <br>
Risk: Live endpoint checks may send requests to an unintended or incompatible third-party gateway. <br>
Mitigation: Confirm the AnyRouter endpoint with the user, use minimal non-sensitive test payloads, and require approval before live API tests. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/can4hou6joeng4/configure-openclaw-anyrouter-model-and-fix-baseurl) <br>
- [AnyRouter endpoint referenced by the skill](https://anyrouter.top) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, configuration, shell commands] <br>
**Output Format:** [Markdown with JSON configuration snippets, command examples, and troubleshooting steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local file paths, diff recommendations, log interpretation, endpoint test plans, and fallback guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
