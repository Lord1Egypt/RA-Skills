## Description:

从 GitHub 找到最匹配的技术人才，生成个性化触达话术。适用于招聘工程师、寻找技术合伙人、猎头交付候选人等场景。

This skill is ready for commercial/non-commercial use.

## Publisher:

[kedoupi](https://clawhub.ai/user/kedoupi)

### License/Terms of Use:

MIT-0

## Use Case:

Recruiters, HR teams, technical leaders, founders, and hiring partners use this skill to search public GitHub activity for candidates matching a technical role, review ranked candidate profiles, and draft personalized outreach for manually approved contacts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a GitHub token and documentation asks for broader token access than public search may need.

Mitigation: Use a dedicated, short-lived token with the minimum scopes that work for the hiring workflow; avoid read:org unless verified as required.

Risk: Token storage guidance includes plaintext .env examples.

Mitigation: Prefer a temporary environment variable or secret manager, never commit tokens, and rotate the token after use.

Risk: Candidate records and outreach drafts can contain personal data.

Mitigation: Store results locally with restricted access, review candidates manually, avoid automated outreach, and follow applicable privacy, anti-spam, and employment-law requirements.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kedoupi/skills/ai-talent-hunter)
- [Compliance guidance](references/compliance.md)
- [OpenClaw](https://openclaw.com)
- [GitHub personal access tokens](https://github.com/settings/tokens)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown tables and prose, JSON search parameters, JSON/JSONL candidate records, shell commands, and outreach draft text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Candidate search requires a user-provided GITHUB_TOKEN and may write local candidate records to data/candidates.jsonl.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
