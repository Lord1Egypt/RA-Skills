## Description: <br>
Analyzes Celery task configurations for reliability, performance, debugging, and production readiness across tasks, routing, serialization, result backends, workers, and beat schedules. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to audit Celery applications for reliability, performance, security-sensitive configuration, scheduling, and worker tuning issues before deployment or during troubleshooting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may inspect Celery configuration files that contain broker passwords, backend credentials, tokens, or production connection strings. <br>
Mitigation: Point the agent at the smallest relevant repository or subdirectory and redact or exclude secret-bearing configuration before analysis. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown report with findings, scores, remediation guidance, and code snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include health scores, category scores, critical issues, per-task analysis, routing maps, beat schedule timelines, worker tuning recommendations, remediation code, and a priority matrix.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
