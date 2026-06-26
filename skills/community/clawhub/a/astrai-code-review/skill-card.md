## Description: <br>
AI-powered code review with intelligent model routing -- saves 40%+ vs always using the most expensive model. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[beee003](https://clawhub.ai/user/beee003) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineering teams use this skill to review code diffs, staged changes, pull requests, or individual files for bugs, quality issues, and security concerns. It returns structured findings with severity, location, summary, and concrete remediation guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reviewed code and diffs are sent to Astrai for routing and model inference. <br>
Mitigation: Run reviews only on code that policy allows you to transmit to Astrai and selected providers; avoid sending sensitive private code unless approved. <br>
Risk: Configured provider API keys can be forwarded to Astrai in BYOK mode. <br>
Mitigation: Prefer hosted routing with only ASTRAI_API_KEY, or use restricted low-quota provider keys dedicated to this service and unset unrelated provider keys before running reviews. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/beee003/astrai-code-review) <br>
- [Astrai Service](https://as-trai.com) <br>
- [Astrai Chat Completions Endpoint](https://as-trai.com/v1/chat/completions) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, guidance, configuration] <br>
**Output Format:** [Structured JSON issues with a summary, model, cost, and savings metadata] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Findings include file, line, severity, message, and suggested fix.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
