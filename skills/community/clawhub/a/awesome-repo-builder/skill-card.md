## Description:

Create a topic-specific GitHub awesome-list repository scaffold with a polished README, concise contribution rules, AI-agent instructions, URL verification, license, and reusable templates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zjsxply](https://clawhub.ai/user/zjsxply)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and documentation maintainers use this skill to create an initial awesome-list repository for a chosen topic, including taxonomy, contribution guidance, agent instructions, templates, and a URL verification script.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The generated URL verifier can make unrestricted outbound HTTP(S) requests from the user's environment.

Mitigation: Run the verifier only on trusted README content, or sandbox network access and add controls for private addresses, redirects, and explicit consent before use in CI or corporate networks.

## Reference(s):

- [Awesome Repository Structure](references/awesome-repo-structure.md)
- [ClawHub Skill Page](https://clawhub.ai/zjsxply/skills/awesome-repo-builder)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, JSON spec, shell command, and generated repository files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated files include README.md, CONTRIBUTING.md, AGENTS.md, LICENSE, .gitignore, verify_urls.py, and reusable Markdown templates.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
