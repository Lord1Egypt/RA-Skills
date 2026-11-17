## Description:

Train autonomous OpenClaw AI agents through LLM-guided curriculum design and multi-turn dialogue evaluation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[myismyname](https://clawhub.ai/user/myismyname)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use ClawSergeant to design, run, and evaluate multi-stage training sessions for OpenClaw agents. The skill helps turn a training intent into curriculum JSON, LLM-generated training messages, evaluator feedback, and session results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: LLM-generated training messages are sent to the configured OpenClaw recipient.

Mitigation: Use a test recipient or restricted OpenClaw profile before connecting the skill to a real agent workspace.

Risk: Training results and lessons may be stored for later use by the agent.

Mitigation: Avoid sensitive prompts or secrets, and review or disable the MEMORY.md write path before production use.

Risk: The skill depends on an OpenAI-compatible LLM endpoint for curriculum design, training dialogue, and evaluation.

Mitigation: Keep LLM_BASE_URL pointed at a trusted HTTPS provider and verify API-key handling before running training sessions.

## Reference(s):

- [ClawSergeant ClawHub skill page](https://clawhub.ai/myismyname/skills/clawsergeant)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON curriculum objects, and JSON training results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write training_results.json and accumulated lesson markdown files during a training run.]

## Skill Version(s):

1.0.0 (source: server release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
