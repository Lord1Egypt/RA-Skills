## Description: <br>
Monitor RSS/Atom feeds and send notifications when new content appears, including feeds for YouTube channels, Reddit subreddits, GitHub releases, blogs, and standard RSS/Atom sources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[runawaydevil](https://clawhub.ai/user/runawaydevil) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to configure a local feed watcher that tracks RSS/Atom sources and posts new-item notifications to a configured webhook service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Feed update metadata may be sent to the configured webhook service. <br>
Mitigation: Use trusted HTTPS webhook URLs and avoid routing private or sensitive feeds to third-party services unless intended. <br>
Risk: Cron setup can make the watcher run continuously in the background. <br>
Mitigation: Add the cron job only when continuous monitoring is desired, and review the configured feeds and log destination before enabling it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/runawaydevil/feed-watcher) <br>
- [Publisher profile](https://clawhub.ai/user/runawaydevil) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with shell command and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces setup and command guidance for a Node.js feed watcher; configured runs may send JSON notifications to a user-provided webhook.] <br>

## Skill Version(s): <br>
0.0.1 (source: SKILL.md metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
