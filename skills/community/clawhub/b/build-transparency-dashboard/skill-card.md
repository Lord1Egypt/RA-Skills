## Description:

Scaffolds a public build dashboard that displays commit activity, last commit details, timestamps, shipped work, and optional community ideas from a private GitHub repository without exposing the repository itself.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cryptocana](https://clawhub.ai/user/cryptocana)

### License/Terms of Use:


## Use Case:

Developers and project teams use this skill to create a public progress dashboard for build-in-public workflows while keeping the source repository private. It provides templates and setup guidance for GitHub Actions automation, a static dashboard page, and an optional community ideas API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow guidance asks for a broad GitHub token that may have more access than the dashboard needs.

Mitigation: Use a fine-grained personal access token or GitHub App limited to the single public site repository and required write permissions.

Risk: Publishing raw commit metadata may expose sensitive commit messages from a private repository.

Mitigation: Review or sanitize commit messages before publishing status data, and avoid including secrets, customer names, vulnerability details, or internal identifiers in commit subjects.

Risk: Public dashboard and ideas-board rendering can introduce security or abuse issues if untrusted content is inserted without strict handling.

Mitigation: Render untrusted values with textContent or strict sanitization, and add rate limits, moderation, and clear privacy disclosure for submissions and voting.

## Reference(s):

- [Setup Guide](artifact/references/setup-guide.md)
- [ClawHub Skill Page](https://clawhub.ai/cryptocana/skills/build-transparency-dashboard)
- [Live Example](https://novaiok-site.fly.dev/build)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with HTML, JavaScript, CSS, YAML, JSON, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a static dashboard template, GitHub Actions workflow, status generation script, optional Express ideas API, and setup instructions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
