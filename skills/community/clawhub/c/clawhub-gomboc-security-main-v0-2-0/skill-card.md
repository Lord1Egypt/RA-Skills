## Description:

Automatically scan codebases for security issues and generate deterministic, merge-ready fixes for CLI, CI/CD, and agent workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[matthewsweeney](https://clawhub.ai/user/matthewsweeney)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security engineers use this skill to scan repositories, generate remediation guidance or fixes, and automate code security remediation through local CLI, MCP, or GitHub Actions workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Repository context may be sent to the Gomboc service during scanning or remediation.

Mitigation: Install and run the skill only when the user trusts Gomboc and has approved sharing the relevant repository context.

Risk: Docker MCP mode uses an unpinned container image with access to the mounted workspace and token.

Mitigation: Pin the container image digest, bind the service to 127.0.0.1, and restrict workspace and token scope before using MCP mode.

Risk: Autonomous remediation can commit or push changes to a repository.

Mitigation: Avoid commit or push automation on important branches without branch protection, pull request review, and human approval of generated changes.

Risk: Personal access tokens can be exposed through shell profiles, logs, or broad environment inheritance.

Mitigation: Store the token in a secret manager or scoped CI secret, avoid printing it, and rotate it if exposure is suspected.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/matthewsweeney/skills/clawhub-gomboc-security-main-v0-2-0)
- [Setup Guide](references/setup.md)
- [MCP Integration Guide](references/mcp-integration.md)
- [GitHub Actions Integration](references/github-action.md)
- [Security Audit and Practices](SECURITY.md)
- [Changelog](CHANGELOG.md)
- [Gomboc Docs](https://docs.gomboc.ai)
- [Gomboc Community Edition](https://docs.gomboc.ai/getting-started-ce)
- [Gomboc GitHub Discussions](https://github.com/Gomboc-AI/gomboc-ai-feedback/discussions)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown, JSON, SARIF, code snippets, shell commands, and YAML workflow examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Gomboc personal access token; remediation workflows may send repository context to Gomboc and can modify, commit, or push code when configured.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact documentation reports 0.2.0 dated 2026-03-25)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
