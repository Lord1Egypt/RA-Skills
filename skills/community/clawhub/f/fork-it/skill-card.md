## Description:

Before the user starts coding a new project idea, search GitHub for an existing repo to fork as a starting point. Skip for debugging, learning, or a specific algorithm/function.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gdwhisper](https://clawhub.ai/user/gdwhisper)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use fork-it before starting a new project to search GitHub for existing repositories, compare reuse fit, and recommend whether to fork, extend, reference, or build from scratch.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Project search terms and selected repository names are sent to GitHub when the scripts are used.

Mitigation: Avoid sensitive project names, private repository identifiers, or confidential search terms unless sharing them with GitHub is acceptable.

Risk: If GITHUB_TOKEN is set, the scripts include it in GitHub API requests for rate limits.

Mitigation: Use a least-privilege token or unset GITHUB_TOKEN when higher rate limits are unnecessary.

## Reference(s):

- [fork-it Script Reference](artifact/references/schema.md)
- [GitHub repository search API endpoint](https://api.github.com/search/repositories)
- [GitHub repository details API endpoint](https://api.github.com/repos)

## Skill Output:

**Output Type(s):** [guidance, shell commands, text]

**Output Format:** [Markdown with inline bash commands and summarized repository data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include repository names, URLs, stars, language, license, recent activity, topics, and reuse advice.]

## Skill Version(s):

3.0.1 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
