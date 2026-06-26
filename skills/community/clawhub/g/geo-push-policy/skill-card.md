## Description: <br>
Manages event notification push decisions with cooldowns, watch-pool promotion, push-count limits, retry handling, and local state persistence. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liweijie0709-cmyk](https://clawhub.ai/user/liweijie0709-cmyk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to control when event notifications should be sent, suppressed, retried, or moved through a watch pool. It is suited for workflows that need local notification state management and duplicate-notification protection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local state files may retain event messages, errors, or dead-letter queue entries that include sensitive notification content. <br>
Mitigation: Store the JSON state file in a dedicated protected location and avoid placing secrets in event messages or error text. <br>
Risk: Dead-letter retry behavior can resend stale or duplicate notifications if queued entries are no longer relevant. <br>
Mitigation: Review and clear the dead-letter queue when duplicate or outdated notifications would be harmful. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/liweijie0709-cmyk/geo-push-policy) <br>
- [Artifact documentation](artifact/SKILL.md) <br>
- [Python policy module](artifact/geo_push_policy.py) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Configuration, Guidance] <br>
**Output Format:** [Python API guidance with JSON state structure examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local push decisions, state updates, watch-pool changes, and retry guidance; no hidden network, credential, or install behavior was found by the security scan.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
