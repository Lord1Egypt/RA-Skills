## Description:

Cli Notion lets agents create, list, and retrieve Notion pages from the command line using the Notion API with optional JSON output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaising-openclaw1](https://clawhub.ai/user/kaising-openclaw1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to connect to a Notion workspace, check API access, and create, list, or retrieve pages from Notion databases through CLI commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A Notion API key can grant workspace access if exposed through shared terminals, logs, or prompts.

Mitigation: Use a least-privilege Notion integration and avoid pasting or echoing the API key in shared contexts.

Risk: The create-page command can write to a live Notion database.

Mitigation: Test against a non-production database before allowing agent-driven writes to production workspace content.

## Reference(s):

- [Cli Notion ClawHub listing](https://clawhub.ai/kaising-openclaw1/skills/cli-notion)
- [Notion integrations](https://www.notion.so/my-integrations)

## Skill Output:

**Output Type(s):** [shell commands, configuration, JSON, text]

**Output Format:** [Command-line output, optionally JSON for agent workflows]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Notion API key and target database or page identifiers.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
