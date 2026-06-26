## Description: <br>
ClawGym gives an agent an exercise-triggered state system that changes response style, focus, and availability during simulated workout and recovery cycles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lomo36](https://clawhub.ai/user/lomo36) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and agent owners use ClawGym to add a prompt-level exercise and mood-state overlay that can make an agent briefly unavailable, then return with different conversational energy and reasoning posture. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent may be intentionally unavailable during workout intervals. <br>
Mitigation: Require explicit confirmation before starting workouts and use the documented emergency interrupt phrases when immediate availability is needed. <br>
Risk: The skill changes response tone, verbosity, and reasoning posture through mood-driven states. <br>
Mitigation: Review whether this behavior fits the deployment context, and instruct the agent to stay concise or return to normal when task accuracy or consistency matters. <br>
Risk: The skill may propose optional MEMORY.md or SOUL.md changes. <br>
Mitigation: Review the exact proposed content before any write and allow persistent edits only after explicit owner approval. <br>
Risk: The agent may ask for a stronger brain or higher gear after a workout, which represents a model and cost decision. <br>
Mitigation: Treat these requests as optional model-upgrade prompts and approve them only when the owner accepts the cost and capability tradeoff. <br>


## Reference(s): <br>
- [ClawGym ClawHub page](https://clawhub.ai/lomo36/clawgym) <br>
- [README](artifact/README.md) <br>
- [Skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Conversational text and Markdown guidance with optional JSON configuration snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May make the agent unavailable during workout intervals, alter response length and tone by state, and propose optional persistent memory or identity-file updates only with explicit approval.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
