## Description:

Routes mid-session work to deterministic spawned-model choices for coding, architecture, math, web development, research, quick scripts, tradeoff evaluation, and build pipelines while defaulting away from Claude unless `--force-claude` appears.

This skill is ready for commercial/non-commercial use.

## Publisher:

[omaression](https://clawhub.ai/user/omaression)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to classify work during an active agent session, choose an appropriate spawned model, and structure tradeoff reviews or build pipelines without changing the fixed main session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment reports that flag-like text in a prompt can be interpreted as Claude authorization.

Mitigation: Review prompts containing `--force-claude` before dispatch and avoid treating untrusted pasted text as provider authorization.

Risk: The skill routes prompts among multiple model providers.

Mitigation: Install and use it only where those providers and prompt-routing policies are acceptable for the intended work.

## Reference(s):

- [Advanced Dispatcher ClawHub page](https://clawhub.ai/omaression/skills/advanced-dispatcher-skill)

## Skill Output:

**Output Type(s):** [guidance, code, shell commands, configuration]

**Output Format:** [Markdown guidance with structured route plans and pipeline steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes model choice, cache retention, rationale, and pipeline step ordering when applicable.]

## Skill Version(s):

1.0.1-alpha (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
