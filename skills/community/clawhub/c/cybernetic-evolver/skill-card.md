## Description:

Cybernetic Evolver is a Python-based agent self-optimization skill that uses closed-loop feedback, adaptive control, stability checks, structure mutation, and online learning to improve agent strategies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ywewanhuang](https://clawhub.ai/user/ywewanhuang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to embed feedback-driven strategy optimization into agents, tune decisions from performance signals, persist learned state, and inspect optimization history before applying recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent self-optimization can change agent routing or strategy based on learned recommendations.

Mitigation: Require explicit user approval before recommendations are applied, and review optimization history and performance metrics before changing agent behavior.

Risk: The integration guidance includes adding a workspace-controlled directory to the Python import path.

Mitigation: Use an isolated workspace, avoid placing writable directories at the front of the import path, and provide a reviewed loader instead of trusting an unverified init_evolver.py.

Risk: Saved and loaded evolver state can persist behavior across sessions.

Mitigation: Restrict save and load paths to a dedicated evolver state directory and review state files before reusing them.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ywewanhuang/skills/cybernetic-evolver)
- [README](artifact/README.md)
- [Architecture](artifact/ARCHITECTURE.md)
- [Workflow](artifact/WORKFLOW.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guidance with Python code examples, configuration values, JSON state files, and result dictionaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces optimization history, best-action recommendations, trigger decisions, and persisted JSON state when used from code.]

## Skill Version(s):

1.2.1 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
