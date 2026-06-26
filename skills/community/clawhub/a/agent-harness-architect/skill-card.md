## Description: <br>
Diagnoses long-running agent architectures and produces a harness optimization plan with deployable bridge artifacts such as progress state, a session protocol, and an output gate. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dottythehomeless](https://clawhub.ai/user/dottythehomeless) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to evaluate long-running agent setups, identify session continuity and verification gaps, and generate reusable harness artifacts for OpenClaw, Claude Code, or similar environments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The self-improvement section may persist user details or change future agent behavior without sufficiently clear approval. <br>
Mitigation: Require explicit user approval before writing learning logs, modifying skill files, or committing generated changes. <br>
Risk: Agent configuration, logs, or generated artifacts could accidentally include secrets or sensitive operational details. <br>
Mitigation: Do not paste secrets into agent configs or logs; review and redact generated artifacts before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dottythehomeless/agent-harness-architect) <br>
- [Agent Harness Architect homepage](https://clawgamers.com/skills/agent-harness-architect) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with JSON and shell command code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces an optimization plan and deployable bridge artifact templates for review before deployment.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
