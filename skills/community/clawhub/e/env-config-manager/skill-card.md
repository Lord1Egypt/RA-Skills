## Description: <br>
Env Config Manager helps agents manage local environment files by loading, switching, setting, validating, and diffing configuration values. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kaiyuelv](https://clawhub.ai/user/kaiyuelv) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to inspect and update project environment configuration files, compare environments, and validate required variables before running local or deployment workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads and modifies local .env files and can expose secret values through terminal output or logs. <br>
Mitigation: Use it only with files you intend to inspect, prefer private terminals, redact output before sharing, and review file changes before relying on them. <br>
Risk: Security evidence warns not to rely on the advertised encryption, key rotation, or team-safe sharing behavior from these artifacts. <br>
Mitigation: Verify any secret-protection implementation before using it with real credentials, and use an established secrets manager for production secrets. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kaiyuelv/env-config-manager) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with shell and Python examples; CLI commands may produce plain text output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Handles local environment configuration values and may display sensitive variables if commands are run without redaction.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence release version and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
