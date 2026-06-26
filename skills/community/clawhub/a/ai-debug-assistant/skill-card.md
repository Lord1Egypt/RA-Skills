## Description: <br>
AI-powered debugging assistant. Analyze error logs, explain error messages, parse stack traces, and get fix suggestions with cheatsheets for 8 languages. Powered by evolink.ai <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[evolinkai](https://clawhub.ai/user/evolinkai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to analyze error logs, explain error messages, parse stack traces, request fix suggestions for code with known errors, and access local debugging cheatsheets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: AI commands send user-selected logs, stack traces, error messages, or code snippets to EvoLink for analysis. <br>
Mitigation: Review and redact secrets, tokens, customer data, private paths, and proprietary code before using AI commands. <br>
Risk: Debugging suggestions may be incomplete or incorrect for the user's specific runtime and dependencies. <br>
Mitigation: Review suggested changes, run tests, and apply fixes in a controlled development environment before deploying. <br>
Risk: The AI analysis path requires network access and an EVOLINK_API_KEY. <br>
Mitigation: Use the local languages and cheatsheet commands when network transmission is not acceptable. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/evolinkai/ai-debug-assistant) <br>
- [Skill Homepage](https://github.com/EvoLinkAI/debug-skill-for-openclaw) <br>
- [EvoLink API Documentation](https://docs.evolink.ai/en/api-manual/language-series/claude/claude-messages-api?utm_source=clawhub&utm_medium=skill&utm_campaign=debug) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown text with command examples, analysis, and suggested code fixes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [AI commands require EVOLINK_API_KEY and send user-selected content to EvoLink; language and cheatsheet commands run locally.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence, frontmatter, and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
