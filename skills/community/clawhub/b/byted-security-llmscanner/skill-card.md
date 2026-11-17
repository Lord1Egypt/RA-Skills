## Description:

A workflow management skill for large-language-model and agent security evaluation, including asset creation and updates, resource discovery, compliance and security task launch, and result analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[volcengine-skills](https://clawhub.ai/user/volcengine-skills)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security evaluators use this skill in OpenClaw to create or update model and agent evaluation assets, query available evaluation resources, launch compliance and adversarial security tests, and summarize results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credentials and API keys may be exposed through configuration, chat prompts, command lines, or cached tokens.

Mitigation: Use test or least-privilege accounts, avoid pasting real secrets into chat or shell history, protect local cache files, and rotate any credentials used with this version.

Risk: TLS certificate verification is bypassed in the network scripts.

Mitigation: Review and fix the TLS bypasses before production use, and connect only to endpoints with trusted certificates.

Risk: Task identifiers and file paths can affect local analysis and report handling.

Mitigation: Validate task IDs before execution, keep generated files contained within the intended skill data directory, and review scripts before running mutating task or asset commands.

Risk: The skill installs and runs npm dependencies and can perform mutating platform operations.

Mitigation: Install in a controlled environment, verify npm dependencies, and run asset or task creation commands only with accounts scoped to the intended evaluation workspace.

## Reference(s):

- [Skill README](artifact/README.md)
- [Skill definition](artifact/SKILL.md)
- [ClawHub skill page](https://clawhub.ai/volcengine-skills/skills/byted-security-llmscanner)
- [Publisher profile](https://clawhub.ai/user/volcengine-skills)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and terminal-oriented text with inline shell commands and generated analysis reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local JSON caches and task report files under the skill data directory when the scripts are run.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence, README changelog, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
