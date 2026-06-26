## Description: <br>
Analyzes Git commit frequency, categories, and timing to assess autonomous operation health and detect idle or breakthrough periods. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bobrenze-bot](https://clawhub.ai/user/bobrenze-bot) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill in Git repositories to inspect commit cadence, category mix, and idle gaps so they can monitor autonomous operation health and spot potential blockers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local Git commit history and can surface repository activity patterns that may be sensitive. <br>
Mitigation: Run it only in repositories whose commit history you intend to analyze. <br>
Risk: Heartbeat logging can store commit-health summaries in local agent memory. <br>
Mitigation: Enable heartbeat logging only when those summaries are appropriate to retain locally. <br>
Risk: Health labels are based on commit-pattern thresholds and can be misleading for teams with different workflows. <br>
Mitigation: Treat recommendations as diagnostic signals and review the underlying commit history before taking action. <br>


## Reference(s): <br>
- [Commit Analyzer ClawHub listing](https://clawhub.ai/bobrenze-bot/commit-analyzer) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Terminal text reports or JSON health-check output, with Markdown guidance for agent use.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads local Git history in the current repository; optional --json output is available for health checks.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
