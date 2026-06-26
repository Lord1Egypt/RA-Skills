## Description: <br>
AI-powered code review that combines fast local static analysis with deep AI reasoning. Catches bugs, security vulnerabilities, performance issues, and style problems. Supports Anthropic, OpenAI, and Ollama models. Falls back to local regex analysis when offline. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TheShadowRose](https://clawhub.ai/user/TheShadowRose) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to review files or directories for bugs, security issues, performance concerns, style problems, and maintainability findings. It can run local static checks only, or combine local findings with a configured Anthropic, OpenAI, or Ollama model for deeper analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: When an external AI provider is configured, reviewed source code and local findings are sent to that provider. <br>
Mitigation: For proprietary or sensitive repositories, leave external API keys unset, use local Ollama, or avoid reviewing files that contain secrets unless organizational policy allows that provider. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/TheShadowRose/code-review-sr) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance] <br>
**Output Format:** [Structured JSON review results with issue lists, scores, suggestions, summaries, and directory aggregate metrics] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Files reviewed with AI are truncated at 8,000 characters before model submission; directory reviews use configurable concurrency.] <br>

## Skill Version(s): <br>
1.0.4 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
