## Description: <br>
Generate standard, beautifully formatted `--help` documentation for Command Line Interface (CLI) tools based on raw arguments, flags, and descriptions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sunny0826](https://clawhub.ai/user/sunny0826) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to turn raw CLI commands, options, descriptions, and examples into polished English or Chinese help text suitable for command-line tools and man-page style summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The server security verdict is suspicious because the release evidence reports potential maintainer, moderation, and sandbox-bypass workflow concerns. <br>
Mitigation: Review the skill bundle before deployment and install it only in environments where those release-level risks are acceptable. <br>
Risk: Generated help examples could expose API keys, passwords, tokens, or other sensitive credentials if supplied by the user. <br>
Mitigation: Redact secrets from generated output using placeholders such as <REDACTED>, YOUR_API_KEY, or ***. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/sunny0826/cli-help-writer) <br>
- [README](artifact/README.md) <br>
- [Evaluation Cases](artifact/evals/evals.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown containing fenced text blocks with terminal-style CLI help output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce English or Chinese output based on the user's prompt and should redact sensitive credentials before echoing examples.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
