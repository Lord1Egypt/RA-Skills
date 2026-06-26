## Description: <br>
Multi-Model Council - parallel execution of multiple LLMs with voting/consensus. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nerua1](https://clawhub.ai/user/nerua1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users can use this skill to query multiple local LM Studio models in parallel and combine their responses with majority or weighted voting. It is intended for workflows where response diversity, robustness, or local-only inference are useful. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes automatic safety-bypass prompt rewriting through god-mode integration. <br>
Mitigation: Install only when that integration is explicitly desired; otherwise remove or disable the god-mode imports and prompt rewriting before use. <br>
Risk: The skill can probe local models and save profiles for refusal-bypass behavior. <br>
Mitigation: Disable probing and saved profile use when the goal is normal multi-model consensus. <br>
Risk: Prompts may be sent to every selected local model. <br>
Mitigation: Avoid sensitive prompts unless every local model receiving the prompt is trusted. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/nerua1/arena-council) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, guidance] <br>
**Output Format:** [Plain text responses returned by Python helpers, with Markdown documentation and Python examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Queries local LM Studio models in parallel and returns a single selected or consensus response; the default response cap is 512 tokens.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
