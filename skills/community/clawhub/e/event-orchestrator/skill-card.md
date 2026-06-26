## Description: <br>
Event Orchestrator provides event-driven skill orchestration with publish/subscribe events, middleware-chain processing, and task state-machine management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pagoda111king](https://clawhub.ai/user/pagoda111king) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to coordinate multi-skill workflows through event publishing, event subscription, middleware processing, retries, logging, and task status transitions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Event payloads, debug logs, or retained event history may expose secrets, personal data, or confidential task outputs. <br>
Mitigation: Avoid publishing sensitive payloads unless handlers and logs are controlled; limit debug logging in shared environments and clear or bound event history for sensitive workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pagoda111king/event-orchestrator) <br>
- [README](artifact/README.md) <br>
- [Evaluation report](artifact/docs/evaluation-report.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JavaScript examples, shell commands, and configuration details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local orchestration guidance and code-oriented event, middleware, and task-state patterns.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and package metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
