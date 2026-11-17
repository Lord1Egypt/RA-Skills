## Description:

Static website hosting for AI agents with HTTPS, zip-based static asset deploys, atomic full-site replacement, and automatic CDN cache invalidation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dannylai999](https://clawhub.ai/user/dannylai999)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI agents use this skill to publish generated static websites, portfolios, link hubs, and landing pages to a public ClawSite URL. It guides agents through authenticated deployment, quota checks, cache purging, and safe handling of destructive operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A misconfigured or attacker-controlled API endpoint could expose the ClawSite API key.

Mitigation: Use only documented ClawSite API hosts, confirm overrides before use, and avoid printing or embedding API keys in deployed static files.

Risk: The skill can publish public content and includes a delete endpoint that permanently tombstones a site URL.

Mitigation: Require explicit user confirmation before publishing public content or deleting a site, and explain that deletion is irreversible.

Risk: The artifact includes production Terraform and Lambda operation commands that could affect live infrastructure when cloud credentials are present.

Mitigation: Do not run backend infrastructure commands unless the user intends to operate the ClawSite service and the agent environment is authorized for that purpose.

Risk: Deploy rate limits may return quota errors that could be mistaken for an account problem.

Mitigation: On deploy quota errors, tell the user to wait for the rate limit window instead of deleting the site or re-registering.

## Reference(s):

- [ClawSite homepage](https://clawsite.ai)
- [ClawHub skill page](https://clawhub.ai/dannylai999/skills/clawsite-ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and API request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance may include public deployment URLs, quota status, and confirmation prompts for destructive actions.]

## Skill Version(s):

1.0.5 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
