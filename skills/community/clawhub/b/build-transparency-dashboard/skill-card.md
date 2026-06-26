## Description: <br>
Scaffold a public build dashboard that publishes commit counts, last commit details, timestamps, shipped work, queue items, and optional community ideas from a private GitHub repository to a public static site. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cryptocana](https://clawhub.ai/user/cryptocana) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and project teams use this skill to build in public by publishing selected progress signals from a private repository to a public dashboard without exposing the repository itself. It is also useful for adding an optional community ideas board to a product or project site. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The GitHub workflow can use a broad personal access token and writes private-repo activity into a public site repository. <br>
Mitigation: Use a fine-grained GitHub token or GitHub App limited to the destination public site repository with only the permissions required to update published files. <br>
Risk: Commit messages and timing metadata from a private repository may disclose sensitive roadmap, customer, incident, or security information when published. <br>
Mitigation: Sanitize or disable public commit messages and review which status fields are published before enabling the workflow. <br>
Risk: The optional ideas API is public by default and can accept user-generated content without authentication, moderation, or a specific CORS origin. <br>
Mitigation: Add rate limiting, moderation, storage limits, and a specific CORS origin before enabling the ideas API in production. <br>
Risk: The hourly scheduled workflow can repeatedly publish status data even when push-based updates are sufficient. <br>
Mitigation: Remove the hourly schedule if heartbeat publishing is unnecessary. <br>


## Reference(s): <br>
- [Setup Guide](artifact/references/setup-guide.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/cryptocana/build-transparency-dashboard) <br>
- [Live Example](https://novaiok-site.fly.dev/build) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with HTML, JavaScript, CSS, YAML workflow templates, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a drop-in static dashboard template, GitHub Actions workflow, status generation script, optional Express ideas API, and setup guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
