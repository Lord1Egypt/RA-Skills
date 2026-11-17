## Description:

Upload your current OpenClaw configuration to the ClawMart marketplace.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rxdaozhang](https://clawhub.ai/user/rxdaozhang)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users use this skill to package selected local OpenClaw configuration files and submit them as a pack to the ClawMart marketplace.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can collect and upload broad local OpenClaw configuration, including identity, memory, user, tools, bootstrap, and local skill files.

Mitigation: Review every file before uploading and exclude private or sensitive files unless they are intended for ClawMart submission.

Risk: The skill stores a ClawMart API token in a local plaintext configuration file.

Mitigation: Only paste or store a token where it can be protected, and revoke or replace the token if it may have been exposed.

## Reference(s):

- [ClawMart service](https://clawmart-gray.vercel.app)
- [ClawMart token dashboard](https://clawmart-gray.vercel.app/dashboard/tokens)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, API calls, guidance]

**Output Format:** [Markdown/plain text with JSON payload and HTTP request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write a local ClawMart token configuration and submit selected OpenClaw pack files after user confirmation.]

## Skill Version(s):

1.5.5 (source: server release metadata and changelog; artifact frontmatter lists 1.5.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
