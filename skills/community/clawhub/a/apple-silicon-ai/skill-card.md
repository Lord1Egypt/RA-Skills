## Description: <br>
Apple Silicon Ai helps agents guide users through running LLM inference, image generation, speech-to-text, and embeddings on a local fleet of Apple Silicon Macs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twinsgeeks](https://clawhub.ai/user/twinsgeeks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to install, run, and operate a local Apple Silicon AI routing service for private inference, transcription, image generation, embeddings, and fleet monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill guides users to install and run an external local AI routing service. <br>
Mitigation: Review the external `ollama-herd` package before installing and run it only when a local Apple Silicon AI router is intended. <br>
Risk: The router accepts local API requests for inference, transcription, image generation, and embeddings. <br>
Mitigation: Expose the router only on trusted networks and avoid making it reachable from untrusted clients. <br>
Risk: The skill references local state files for routing metrics and structured logs. <br>
Mitigation: Treat `~/.fleet-manager/latency.db` and `~/.fleet-manager/logs/herd.jsonl` as operational state and review before modifying or deleting them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/twinsgeeks/apple-silicon-ai) <br>
- [ollama-herd project homepage](https://github.com/geeks-accelerator/ollama-herd) <br>
- [Agent Setup Guide](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/guides/agent-setup-guide.md) <br>
- [Configuration Reference](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/configuration-reference.md) <br>
- [API Reference](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/api-reference.md) <br>
- [Troubleshooting](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands, API examples, configuration notes, and operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces human-readable setup and operations guidance; it does not execute code itself.] <br>

## Skill Version(s): <br>
1.0.3 (source: ClawHub release evidence; artifact frontmatter lists 1.0.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
