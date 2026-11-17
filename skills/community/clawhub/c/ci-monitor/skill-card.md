## Description:

Monitor and interact with CI/CD pipelines across Jenkins, GitHub Actions, and GitLab CI by checking build status, triggering builds, analyzing failed jobs, and viewing logs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhanghengyi1986-afk](https://clawhub.ai/user/zhanghengyi1986-afk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect CI/CD pipeline status, review failed job output, trigger or retry builds, and summarize failure causes across Jenkins, GitHub Actions, and GitLab CI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credentialed CI access can expose build logs, project metadata, or sensitive operational details.

Mitigation: Use least-privilege CI tokens and limit log retrieval to the lines needed for the requested status or failure analysis.

Risk: Build-triggering or retry commands can consume CI capacity or affect deployment workflows.

Mitigation: Confirm the target job, repository, branch, environment, and parameters before running commands that trigger or retry CI jobs.

Risk: Failure summaries may omit context or misidentify root causes when based on partial logs.

Mitigation: Review the cited CI log output and test reports before applying proposed fixes or escalating incidents.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhanghengyi1986-afk/skills/ci-monitor)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown status reports and failure summaries with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include CI API requests and log excerpts when the user provides authorized access.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
