## Description: <br>
Run Django management commands (migrate, showmigrations, makemigrations, check, version, logs, readonly) or Django ORM queries on any configured Django project. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[manojrammurthy](https://clawhub.ai/user/manojrammurthy) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and administrators use this skill to inspect and operate configured Django projects from OpenClaw, including migrations, model and user listings, settings checks, logs, and ORM queries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives OpenClaw broad administrator-level access to the configured Django project, including write-capable management commands and ORM execution. <br>
Mitigation: Install only for trusted Django projects, enable read-only mode by default for production or sensitive databases, and require explicit review before disabling read-only mode. <br>
Risk: The shell command can execute arbitrary Django-context Python and may expose or modify application data if enabled. <br>
Mitigation: Keep shell disabled through read-only mode except for trusted maintenance windows, and review requested code before execution. <br>
Risk: Setup persists Django project path, virtual environment path, settings module, and read-only state in the local OpenClaw configuration. <br>
Mitigation: Inspect the saved OpenClaw configuration after setup and remove or correct stale DJANGO-related settings when project access should change. <br>


## Reference(s): <br>
- [ClawHub Django Claw Skill Page](https://clawhub.ai/manojrammurthy/django-claw-skill) <br>
- [OpenClaw](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with raw command output in code blocks and a one-line summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires bash and python3 on macOS or Linux; command behavior depends on the configured Django project and read-only mode.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
