## Description:

Deploy simple web pages and HTML apps live to the internet using the Deno Deploy REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hosainnet](https://clawhub.ai/user/hosainnet)

### License/Terms of Use:

Apache-2.0

## Use Case:

Developers and agents use this skill to prepare Deno-compatible web apps, configure Deno Subhosting credentials, deploy through the bundled script, and verify the resulting public URL before sharing it.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can reuse a Deno deployment token and publish generated code to a public URL.

Mitigation: Use scoped and revocable Deno credentials, require explicit approval before each deployment, and verify the deployed URL before presenting success.

Risk: The skill stores Deno credentials in plaintext config files under the user's home directory.

Mitigation: Store credentials with restrictive file permissions or in a secret manager, and rotate tokens after use when appropriate.

Risk: Broad activation language may deploy content when a user only asks for a hosted or shareable result.

Mitigation: Confirm the user's intent to publish publicly before running the deployment script.

## Reference(s):

- [Deno Subhosting Setup](https://dash.deno.com/subhosting/new_auto)
- [ClawHub Skill Page](https://clawhub.ai/hosainnet/skills/deno-subhosting-deploy-skill)

## Skill Output:

**Output Type(s):** [guidance, code, shell commands, configuration]

**Output Format:** [Markdown guidance with TypeScript and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May run the bundled deployment script, print Deno deployment JSON, and return a public deno.dev URL after verification.]

## Skill Version(s):

0.1.0 (source: server release metadata; skill frontmatter metadata states 0.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
