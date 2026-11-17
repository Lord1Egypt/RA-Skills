## Description:

Bazhuayu Webhook helps agents trigger Octoparse RPA tasks through a signed webhook with custom parameters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blogwebsem](https://clawhub.ai/user/blogwebsem)

### License/Terms of Use:

MIT

## Use Case:

Developers and automation operators use this skill to configure a Bazhuayu/Octoparse RPA webhook, test the request payload, and trigger a selected RPA workflow with default or custom parameters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Webhook keys can trigger the configured RPA workflow if exposed.

Mitigation: Treat BAZHUAYU_WEBHOOK_KEY as an account credential, prefer environment variables, and keep real keys out of config files, screenshots, shell history, and Git.

Risk: Setup and migration helpers handle secrets and may create local environment examples or configuration backups.

Mitigation: Run helper scripts only from a trusted skill directory, review generated .env.example, .env.migrated, and backup files, and delete or protect them after migration.

Risk: Live execution can trigger the configured RPA task.

Mitigation: Use test or dry-run mode first, then run live commands only when the webhook URL, key, parameters, and target workflow are intentional.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/blogwebsem/skills/bazhuayu-webhook)
- [Bazhuayu RPA Help Center](https://rpa.bazhuayu.com/helpcenter)
- [Webhook Trigger Task Documentation](https://rpa.bazhuayu.com/helpcenter/docs/skmvua)
- [RPA API Documentation](https://rpa.bazhuayu.com/helpcenter/docs/rpaapi)
- [Webhook Setup Guide](WEBHOOK_SETUP.md)
- [Security Guide](SECURITY.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON configuration examples; runtime commands emit console text and dry-run JSON payload previews.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 plus BAZHUAYU_WEBHOOK_URL and BAZHUAYU_WEBHOOK_KEY; live run commands send a POST request to the configured webhook.]

## Skill Version(s):

2.0.4 (source: package.json, release evidence, RELEASE-2.0.4.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
