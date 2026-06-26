## Description: <br>
Real-time monitoring dashboard for API uptime, response times, error rates, custom health checks, and alert notifications via email or Slack. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Sunshine-del-ux](https://clawhub.ai/user/Sunshine-del-ux) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to start a lightweight local monitor, add trusted API health endpoints, and inspect recent uptime and response checks in a browser dashboard. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The monitor performs network checks against configured endpoints and could be misused to reach internal or sensitive services. <br>
Mitigation: Run it in a dedicated directory, only add endpoints you trust, avoid URLs containing secrets, and do not allow untrusted users to add endpoints. <br>
Risk: Advertised alerting and historical reporting may not be fully implemented in the artifact. <br>
Mitigation: Do not rely on email, Slack, or historical reporting behavior until those features are verified in the deployed environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Sunshine-del-ux/api-monitor-dashboard) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with shell command examples and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The artifact includes a shell script that creates local runtime files and serves a browser dashboard on localhost:3000.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
