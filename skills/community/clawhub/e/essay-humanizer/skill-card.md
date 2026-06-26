## Description: <br>
Rewrite AI-drafted essays into more human-like academic prose using a Qwen3-8B MLX LoRA adapter, corpus-derived writing-pattern weights, and syntactic targets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kevin0818-lxd](https://clawhub.ai/user/kevin0818-lxd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, writers, and education-support agents use this skill to revise AI-drafted argumentative or academic essays into continuous plain-text prose while preserving the author's stance and citations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local setup installs Python ML packages and downloads a large HuggingFace model. <br>
Mitigation: Install only in a controlled environment that can support Apple Silicon MLX and review package/model sources before use. <br>
Risk: The optional HTTP API can expose essay text over a network if hosted remotely. <br>
Mitigation: Keep the API local where possible; for non-local use, require HUMANIZE_API_KEY authentication and HTTPS. <br>
Risk: Essay rewriting can conflict with school or workplace academic-integrity policies. <br>
Mitigation: Use outputs only within the applicable policy and review rewritten text before submission or publication. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/kevin0818-lxd/essay-humanizer) <br>
- [Hosted API](references/hosted_api.md) <br>
- [24 AI Writing Patterns](references/patterns.md) <br>
- [Training Pipeline](references/training.md) <br>
- [Wikipedia: Signs of AI Writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Plain text essay output with optional Markdown setup guidance and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Inference defaults to Qwen/Qwen3-8B-MLX-4bit with a local LoRA adapter and a 2048-token generation limit.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
