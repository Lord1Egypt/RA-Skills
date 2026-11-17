## Description:

Cross Model Review provides adversarial implementation-plan review using two different AI models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[don-gbot](https://clawhub.ai/user/don-gbot)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineering teams use this skill to run higher-risk or longer implementation plans through a cross-model adversarial review loop before execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Plan or project context may be sent to spawned model sessions and can expose secrets, credentials, regulated data, or sensitive design details.

Mitigation: Do not include secrets, credentials, regulated data, or untrusted third-party code snippets in plan or project context.

Risk: Prompt-boundary protections may not fully prevent adversarial plan content from influencing reviewer behavior.

Mitigation: Prefer explicit invocation and tool-restricted spawned sessions for sensitive auth, payment, or data-model plans.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/don-gbot/skills/cross-model-review)
- [Publisher Profile](https://clawhub.ai/user/don-gbot)
- [README](README.md)
- [Security Policy](SECURITY.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown plans and summaries, JSON review records, and shell command sequences]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates per-run review artifacts including plan versions, issue tracking, changelog, and summary files.]

## Skill Version(s):

2.1.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
