## Description:

Deploy Cursor AI agents to GitHub repos. Automatically write code, generate tests, create documentation, and open PRs using your existing Cursor subscription.

This skill is ready for commercial/non-commercial use.

## Publisher:

[parcostabot](https://clawhub.ai/user/parcostabot)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to delegate coding tasks to Cursor Cloud Agents on GitHub repositories, monitor agent progress, send follow-up prompts, and retrieve results such as code changes, tests, documentation, and pull request links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cursor credentials could be exposed if they are stored in broad environment scopes, project files, or misconfigured local files.

Mitigation: Store CURSOR_API_KEY only in a dedicated file or tightly controlled environment variable, keep file permissions restricted, and avoid committing credential-bearing files.

Risk: Overriding CURSOR_API_BASE can direct authenticated requests away from the normal Cursor API endpoint.

Mitigation: Do not set CURSOR_API_BASE unless testing with throwaway credentials and a trusted endpoint.

Risk: Cached Cursor API responses and background task logs may contain repository, prompt, conversation, or pull request details on shared machines.

Mitigation: Protect or clear ~/.cache/cursor-api, especially on shared systems or when working with private repositories.

## Reference(s):

- [Cursor Cloud Agents API Reference](references/api-reference.md)
- [Skill Security Policy](SECURITY.md)
- [ClawHub Skill Page](https://clawhub.ai/parcostabot/skills/cursor-cloud-agents)
- [OpenClaw](https://openclaw.dev)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or read local cache files under ~/.cache/cursor-api and may emit background task status JSON.]

## Skill Version(s):

1.3.3 (source: server release metadata and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
