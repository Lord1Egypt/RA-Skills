## Description:

Connects the original Ralphy CLI to Genspark Claw Local Computer so an agent can process PRD development tasks sequentially in isolated Claw sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sueelly](https://clawhub.ai/user/sueelly)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to run Ralphy-controlled PRD task loops through Genspark Claw, creating a fresh local Claw session for each task and checking completion after validation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on mutable external ralphy-claw code without integrity checks.

Mitigation: Review and pin the ralphy-claw checkout before setup or installation.

Risk: Running the skill can edit the selected project, run validation commands, and update PRD state.

Mitigation: Run it only in trusted workspaces and use --no-commit unless commits are explicitly desired.

Risk: Execution uses Genspark account permissions and credits.

Mitigation: Confirm account access, credit impact, and local app readiness before starting a run.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sueelly/skills/genspark-ralphy-cli)
- [Ralphy CLI](https://github.com/michaelshimeles/ralphy)
- [ralphy-claw](https://github.com/kimhyejoo/ralphy-claw)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and execution summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Sequential execution only; may update PRD task state and project files through the installed ralphy-claw tool.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
