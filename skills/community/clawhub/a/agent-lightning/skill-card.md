## Description: <br>
Microsoft Research's Agent Lightning framework helps developers optimize AI agents with reinforcement learning, automatic prompt optimization, and supervised fine-tuning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[olmmlo-cmd](https://clawhub.ai/user/olmmlo-cmd) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to configure, instrument, train, evaluate, export, and serve optimized AI agents with Agent Lightning across common agent frameworks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agent tracing and training workflows may capture prompts, responses, tool calls, or other sensitive workflow data. <br>
Mitigation: Avoid tracing production or secret-bearing workflows by default, review collected traces before training, and use scoped API keys. <br>
Risk: Nightly or unpinned package installation can introduce unexpected upstream changes. <br>
Mitigation: Prefer stable pinned package versions and only install upstream packages that the user trusts. <br>
Risk: Optional remote storage can expose training traces or checkpoints if cloud permissions are too broad. <br>
Mitigation: Configure S3 storage with encryption, limited IAM permissions, retention limits, and access logging. <br>


## Reference(s): <br>
- [Agent Lightning ClawHub Release](https://clawhub.ai/olmmlo-cmd/agent-lightning) <br>
- [Agent Lightning Documentation](https://microsoft.github.io/agent-lightning/) <br>
- [Agent Lightning GitHub Repository](https://github.com/microsoft/agent-lightning) <br>
- [Agent Lightning API Reference](https://microsoft.github.io/agent-lightning/stable/reference/) <br>
- [Agent Lightning Paper](https://arxiv.org/abs/2508.03680) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python, YAML, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include training configuration, instrumentation examples, command-line workflows, and operational recommendations.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
