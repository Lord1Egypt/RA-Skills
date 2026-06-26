## Description: <br>
Gemma 3 by Google helps agents run Gemma 3 models across a local device fleet through Ollama Herd, with cross-platform guidance for macOS, Linux, and Windows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twinsgeeks](https://clawhub.ai/user/twinsgeeks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to configure and call Gemma 3 models through a local Ollama Herd fleet router. It provides model selection guidance, OpenAI-compatible SDK examples, curl requests, and fleet health checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, documents, generated-image prompts, or uploaded audio may be processed by devices on the user's local fleet. <br>
Mitigation: Use the skill only on trusted local networks and avoid sensitive data unless local fleet processing and logs are acceptable. <br>
Risk: The workflow depends on installing and running the ollama-herd package and router/node services. <br>
Mitigation: Verify the PyPI package and upstream repository before installation, and run router/node services only on machines the user trusts. <br>
Risk: Gemma model downloads can be large and may affect local storage or bandwidth. <br>
Mitigation: Keep model pulls user-confirmed and review model size before downloading. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/twinsgeeks/gemma-gemma3) <br>
- [Ollama Herd](https://github.com/geeks-accelerator/ollama-herd) <br>
- [Ollama Herd PyPI Package](https://pypi.org/project/ollama-herd/) <br>
- [Agent Setup Guide](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/guides/agent-setup-guide.md) <br>
- [API Reference](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/api-reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with bash, Python, curl, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes local network endpoint examples, hardware-based model guidance, and guardrails for user-confirmed model pulls and deletions.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
