## Description: <br>
Diagnose and mitigate ClawHub/ClawDHUB publish failures (auth, browser-login, missing dependencies, pending security-scan visibility errors, and wrong profile/skill URLs). Use when publishing skills to ClawHub fails, inspect reports temporary errors, or you need a safer publish+verify workflow with retries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[BlueBirdBack](https://clawhub.ai/user/BlueBirdBack) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and release maintainers use this skill to diagnose ClawHub publishing failures, run preflight checks, prefer token-based login in headless environments, and publish with retry-aware verification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The publish wrapper can publish under the user's logged-in ClawHub account. <br>
Mitigation: Confirm `clawhub whoami`, the target skill path, slug, version, changelog, and `latest` tag before running the publish wrapper. <br>
Risk: Authentication and account output may be written to temporary files during diagnostics. <br>
Mitigation: Avoid running the helper in shared temporary directories when account details are sensitive. <br>
Risk: A newly published skill can appear hidden or unavailable while security scan visibility catches up. <br>
Mitigation: Treat immediate inspect failures as potentially transient, retry with backoff, and verify with both the CLI and the skill web URL before escalating. <br>


## Reference(s): <br>
- [ClawHub Publish Error Map](references/error-map.md) <br>
- [ClawHub skill page](https://clawhub.ai/BlueBirdBack/clawhub-publish-doctor) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash commands and shell script references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes preflight, login, publish, inspect, and retry guidance for ClawHub workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
