## Description:

Council Brief installs, queries, and manages LLM Council, a multi-model consensus app that produces synthesized answers through a quick CLI or web UI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeadland](https://clawhub.ai/user/jeadland)

### License/Terms of Use:


## Use Case:

Developers and other ClawHub users use this skill to install and operate a local LLM Council workflow, ask questions across multiple models, inspect service status, and stop the related services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer runs mutable external code from the linked LLM Council project at install time.

Mitigation: Install only in an isolated workspace after reviewing the cloned repository revision and confirming the external project is trusted.

Risk: The installer copies OpenRouter or OpenClaw gateway credentials into plaintext environment files.

Mitigation: Restrict permissions on generated .env files and use scoped or revocable credentials where possible.

Risk: The installer may kill unrelated local services listening on ports 8001, 5173, or 4173.

Mitigation: Check local port usage before installation and stop or move important services before running the installer.

Risk: The web UI is exposed on the LAN by default.

Mitigation: Bind the UI to localhost only or run it on a trusted network.

## Reference(s):

- [Council Brief ClawHub listing](https://clawhub.ai/jeadland/skills/council-brief)
- [LLM Council repository](https://github.com/jeadland/llm-council)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain text and Markdown with shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Quick query mode returns the chairman synthesis from a local backend and may take 30-60 seconds.]

## Skill Version(s):

2.0.0 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
