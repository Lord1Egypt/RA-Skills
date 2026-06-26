## Description: <br>
Chat Vitals monitors AI conversation health with real-time metrics for first-try success, promise fulfillment, token efficiency, rework, plan inflation, dashboards, and reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[carolava](https://clawhub.ai/user/carolava) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and agent users use Chat Vitals to monitor local AI chat sessions, inspect conversation quality metrics, view real-time health status, and generate Markdown reports for optimization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill inspects chat messages and keeps local session telemetry to calculate health metrics. <br>
Mitigation: Use it only for conversations where local inspection and metadata retention are acceptable, and periodically delete the skill data directory when historical metrics are no longer needed. <br>
Risk: Metric outputs are heuristic and may misclassify rework, promises, token efficiency, or health status. <br>
Mitigation: Treat dashboard alerts and reports as review aids, not authoritative quality judgments, and confirm findings before changing workflows. <br>


## Reference(s): <br>
- [Chat Vitals ClawHub page](https://clawhub.ai/carolava/chat-vitals) <br>
- [carolava publisher profile](https://clawhub.ai/user/carolava) <br>
- [README](artifact/README.md) <br>
- [Skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration] <br>
**Output Format:** [Terminal text, JSON summaries, and Markdown reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local session metrics, dashboard views, and report files for the monitored chat session.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
