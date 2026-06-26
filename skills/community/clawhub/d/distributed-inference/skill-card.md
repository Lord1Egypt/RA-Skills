## Description: <br>
Coordinates distributed Ollama inference across heterogeneous macOS, Linux, and Windows machines using scoring, adaptive capacity learning, and context-aware model placement. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twinsgeeks](https://clawhub.ai/user/twinsgeeks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to install, operate, inspect, and troubleshoot a self-hosted distributed inference coordinator and node agents for local Ollama workloads. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Model pull, auto-pull, and delete actions can download large model files or remove local models. <br>
Mitigation: Require explicit user approval before running pull, auto-pull, or delete operations. <br>
Risk: The distributed inference coordinator exposes local HTTP endpoints that can affect model routing and lifecycle actions. <br>
Mitigation: Run the coordinator only on machines and networks the user controls and restrict access to the coordinator port. <br>
Risk: Installing and running the underlying ollama-herd package executes third-party software. <br>
Mitigation: Install only after the user confirms they trust the package and repository. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/twinsgeeks/distributed-inference) <br>
- [ollama-herd PyPI Package](https://pypi.org/project/ollama-herd/) <br>
- [ollama-herd Project Repository](https://github.com/geeks-accelerator/ollama-herd) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and HTTP API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference local service endpoints, SQLite trace data, and OpenClaw metadata for required and optional command-line tools.] <br>

## Skill Version(s): <br>
1.0.4 (source: release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
