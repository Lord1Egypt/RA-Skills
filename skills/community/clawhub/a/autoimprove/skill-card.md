## Description: <br>
Autoimprove helps AI agents optimize measurable outcomes by editing scoped files, running checks, comparing scores, and keeping only successful changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zanetworker](https://clawhub.ai/user/zanetworker) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use Autoimprove to run guided or headless optimization loops for code performance, ML training, Docker images, SQL queries, prompts, CI speed, frontend bundles, Kubernetes configs, and other measurable targets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can edit repository files, run configured shell commands, create commits, and hard-reset failed experiments. <br>
Mitigation: Run it only in a clean dedicated branch, worktree, disposable clone, or container, and commit or stash existing work before use. <br>
Risk: A malicious or poorly reviewed improve.md or exported program.md could direct the agent toward unsafe commands or unintended changes. <br>
Mitigation: Inspect improve.md and any exported program.md before execution, confirm the resolved change scope, and run interactively before headless or overnight use. <br>
Risk: Configured commands may interact with production credentials, Kubernetes contexts, databases, cloud resources, or other sensitive environments. <br>
Mitigation: Strip production credentials and avoid production kube, database, and cloud contexts during optimization runs. <br>


## Reference(s): <br>
- [ClawHub Autoimprove release](https://clawhub.ai/zanetworker/autoimprove) <br>
- [Autoimprove README](README.md) <br>
- [Autoimprove Protocol](references/protocol.md) <br>
- [Autoimprove Examples](references/examples.md) <br>
- [Karpathy autoresearch](https://github.com/karpathy/autoresearch) <br>
- [Shopify Liquid optimization PR](https://github.com/Shopify/liquid/pull/2056) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands, configuration snippets, generated files, and JSON experiment logs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May modify scoped repository files, create commits, run configured commands, export program.md, and write .autoimprove experiment logs.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
