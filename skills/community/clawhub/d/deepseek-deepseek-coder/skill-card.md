## Description: <br>
DeepSeek DeepSeek-Coder helps agents set up and use DeepSeek-V3, DeepSeek-R1, and DeepSeek-Coder across a local Ollama Herd fleet with cross-platform routing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twinsgeeks](https://clawhub.ai/user/twinsgeeks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to configure local DeepSeek model access through Ollama Herd, route requests across available machines, and generate example API calls for local model, image, speech, and embedding endpoints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill instructs users to install and run a third-party package. <br>
Mitigation: Verify the ollama-herd package and linked repository before installation, and prefer an isolated environment. <br>
Risk: Local model pulls can consume substantial disk space, memory, and bandwidth. <br>
Mitigation: Confirm model downloads before pulling and choose smaller DeepSeek variants when available hardware is insufficient. <br>
Risk: A local routing endpoint may expose model access if bound to untrusted interfaces. <br>
Mitigation: Keep the router bound to trusted interfaces and review network exposure before accepting requests. <br>
Risk: Model deletion or local fleet-manager file changes could remove useful local state. <br>
Mitigation: Confirm deletion prompts before proceeding and avoid deleting or modifying files under ~/.fleet-manager/. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/twinsgeeks/deepseek-deepseek-coder) <br>
- [ollama-herd package](https://pypi.org/project/ollama-herd/) <br>
- [ollama-herd repository](https://github.com/geeks-accelerator/ollama-herd) <br>
- [Agent Setup Guide](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/guides/agent-setup-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash, Python, and curl examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes local endpoint examples, hardware sizing guidance, and operational guardrails for model pulls and deletions.] <br>

## Skill Version(s): <br>
1.0.3 (source: server evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
