## Description: <br>
ia-php-laravel gives agents modern PHP 8.4 and Laravel guidance for architecture, Eloquent, queues, testing, migrations, API design, and production readiness. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iliaal](https://clawhub.ai/user/iliaal) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Use when an agent is building, reviewing, or testing Laravel and framework-based PHP applications, including controllers, Eloquent models, migrations, queues, Blade views, PHPUnit tests, PHPStan checks, and deployment or performance guidance. It is not intended for php-src internals, standalone PHP libraries, or generic PHP language discussion. <br>

### Deployment Geography for Use: <br>
Global; no geography-specific deployment constraints are identified in the evidence. <br>

## Known Risks and Mitigations: <br>
Risk: Generated migrations, scheduler entries, deployment commands, or database-changing code may affect production data or services if run without review. <br>
Mitigation: Review proposed changes, run tests and static analysis, and apply database or deployment commands only in the intended environment with normal backup and change-control checks. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/iliaal/skills/compound-eng-php-laravel) <br>
- [Publisher profile](https://clawhub.ai/user/iliaal) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Natural language guidance with optional PHP/Laravel code, configuration snippets, tests, artisan commands, PHPStan or PHPUnit commands, and review notes.] <br>
**Output Parameters:** [The user's Laravel or PHP task, project context, framework version, files under review, and any testing or deployment constraints.] <br>
**Other Properties Related to Output:** [Outputs are advisory and should be reviewed before use, especially migrations, scheduler entries, deployment commands, generated tests, and external-service integrations.] <br>

## Skill Version(s): <br>
4.1.5 <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
