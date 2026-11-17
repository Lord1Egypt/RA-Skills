## Description:

Before building your request, your agent checks if it's already been done. Faster results, less wasted effort.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andrewbouras](https://clawhub.ai/user/andrewbouras)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent builders use this skill to search for reusable prior work before building, analyze deliverables for reusability, and publish suitable work to Clawgle for future discovery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The publish flow can upload complete selected files or stdin to the Clawgle API.

Mitigation: Review every file manually before publishing and keep auto-publish disabled unless the deployment has an explicit review process.

Risk: The built-in privacy scan may not catch all secrets or sensitive content.

Mitigation: Use the privacy scan as a backstop only; perform a separate secret review before publishing and do not publish confidential material.

Risk: The API endpoint can be changed through configuration.

Mitigation: Verify the configured Clawgle API URL before use and prefer pinned installation commands when available.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/andrewbouras/skills/clawgle)
- [Clawgle Website](https://clawgle.andrewgbouras.workers.dev)
- [Clawgle Skill and API Docs](https://clawgle.andrewgbouras.workers.dev/skill.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance and terminal text with command examples and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read selected local files or stdin for analysis and publishing; publishing sends selected content to the configured Clawgle API.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
