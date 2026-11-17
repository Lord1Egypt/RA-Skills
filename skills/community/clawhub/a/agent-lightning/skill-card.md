## Description:

Microsoft Research's agent training framework optimizes AI agents with reinforcement learning, automatic prompt optimization, and supervised fine-tuning while working with LangChain, AutoGen, CrewAI, OpenAI Agent SDK, and plain Python OpenAI agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[olmmlo-cmd](https://clawhub.ai/user/olmmlo-cmd)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to install, configure, instrument, train, evaluate, export, and serve AI agents with Agent Lightning workflows. It is intended for agent optimization tasks that use reinforcement learning, prompt optimization, supervised fine-tuning, evaluation tasks, checkpoints, logs, and optional remote storage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Install instructions use unpinned packages and include an optional nightly TestPyPI path.

Mitigation: Install in a virtual environment or container, prefer a pinned stable PyPI release, and review nightly package sources before use.

Risk: Training workflows may expose API keys or cloud credentials.

Mitigation: Provide only required credentials, avoid unnecessary cloud secrets during install and training, and scope credentials to the task.

Risk: Training can write checkpoints, logs, traces, dashboards, and optional remote storage outputs.

Mitigation: Review local and remote output locations before running training, and avoid storing sensitive prompts, traces, or credentials in logs and checkpoints.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/olmmlo-cmd/skills/agent-lightning)
- [Agent Lightning Documentation](https://microsoft.github.io/agent-lightning/)
- [Train SQL Agent with RL](https://microsoft.github.io/agent-lightning/stable/how-to/train-sql-agent/)
- [Agent Lightning API Reference](https://microsoft.github.io/agent-lightning/stable/reference/)
- [Agent Lightning arXiv Paper](https://arxiv.org/abs/2508.03680)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash, Python, and YAML examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include install commands, training configuration, instrumentation examples, evaluation guidance, and checkpoint or logging paths.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
