## Description: <br>
Transforms AI agents from task-followers into proactive partners that anticipate needs, preserve working memory, perform periodic check-ins, and improve through documented operating patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AlexeyVorobiev](https://clawhub.ai/user/AlexeyVorobiev) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to configure an assistant with proactive workflows, persistent memory files, onboarding, heartbeat checks, and approval-gated external actions. It is best suited for users who intentionally want a highly proactive assistant and are prepared to review its automation boundaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill encourages broad proactive behavior, memory logging, monitoring, cleanup, and automation that can exceed a user's intended consent boundaries. <br>
Mitigation: Install only when this posture is intended, require explicit approval for external, destructive, or background actions, and review memory and automation files regularly. <br>
Risk: Persistent memory and transcript-style logs can capture sensitive personal or project details. <br>
Mitigation: Avoid storing secrets or sensitive personal data, periodically prune memory files, and keep credential storage separate with restrictive permissions. <br>
Risk: Automatic cleanup, BOOTSTRAP.md deletion, spawned agents, cron work, and email or calendar checks can create operational surprise. <br>
Mitigation: Gate or remove these behaviors before use unless specifically needed, and keep human approval in the loop for sends, posts, deletions, purchases, and security changes. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/AlexeyVorobiev/alexey-proactive-agent) <br>
- [Onboarding flow reference](references/onboarding-flow.md) <br>
- [Security patterns reference](references/security-patterns.md) <br>
- [Creator profile referenced by skill](https://x.com/halthelobster) <br>
- [Related Bulletproof Memory skill](https://clawdhub.com/halthelobster/bulletproof-memory) <br>
- [Related PARA Second Brain skill](https://clawdhub.com/halthelobster/para-second-brain) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with file templates and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces operating procedures and starter files for memory, onboarding, heartbeat checks, and security review.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence; artifact frontmatter reports 3.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
