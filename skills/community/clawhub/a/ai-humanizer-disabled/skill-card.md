## Description: <br>
Humanizes AI-generated text by detecting common LLM writing patterns, scoring drafts, and suggesting or applying more natural rewrites. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[robinzorro86](https://clawhub.ai/user/robinzorro86) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Writers, editors, and developers use this skill to review drafts for AI-like phrasing, statistical uniformity, and style artifacts, then produce more natural text or implementation guidance for local CLI, API, MCP, and Custom GPT integrations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Confidential drafts may be exposed if users send text through a deployed API endpoint or Custom GPT Action. <br>
Mitigation: Prefer local CLI or MCP use for sensitive content, and review endpoint ownership and data handling before submitting confidential text. <br>
Risk: Always-on prompt rules can change an agent's general writing style beyond explicit humanization requests. <br>
Mitigation: Enable always-on behavior only when broad style changes are intended, and keep humanization rules scoped to specific workflows otherwise. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/robinzorro86/ai-humanizer-disabled) <br>
- [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) <br>
- [Copyleaks stylometric research](https://arxiv.org/abs/2503.01659) <br>
- [Pattern documentation](references/patterns.md) <br>
- [AI vocabulary reference](references/ai-vocabulary.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, shell commands, configuration] <br>
**Output Format:** [Plain text, Markdown reports, JSON analysis, and command-line examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include AI-likeness scores, pattern findings, rewrite suggestions, and optional autofix output.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
