## Description: <br>
Create, deploy, update, and troubleshoot Coolify applications with the official Coolify CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Heldinhow](https://clawhub.ai/user/Heldinhow) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to create, redeploy, update, and troubleshoot Coolify applications, including GitHub app deployments, environment variables, logs, and fallback Docker/Traefik routing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Token-bearing Coolify context or API commands can expose credentials if copied with an untrusted fixed host or IP. <br>
Mitigation: Replace every host or IP with the user's own Coolify instance, and do not send Coolify tokens to 217.77.2.59 or any endpoint the user does not control. <br>
Risk: Forced redeploys, app deletion, and Docker stop/remove commands can interrupt or remove running services. <br>
Mitigation: Require explicit confirmation and verify the Coolify context, app UUID, and container name before running destructive or force commands. <br>
Risk: Direct Docker and Traefik fallback deployment can bypass Coolify-managed app state and expected UI visibility. <br>
Mitigation: Use the official Coolify CLI first, reserve direct Docker fallback for blocked app creation, and verify both deployment status and HTTP response before treating deployment as complete. <br>


## Reference(s): <br>
- [Coolify Reference](references/coolify-api.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Coolify CLI, HTTP API, curl, Docker, and Traefik commands that require user-provided hosts, tokens, UUIDs, and domains.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
