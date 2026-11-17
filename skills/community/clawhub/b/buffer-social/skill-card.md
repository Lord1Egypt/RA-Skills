## Description:

Create, schedule, queue, and manage social media posts and drafts across Buffer-connected profiles using terminal commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ahmadabugosh](https://clawhub.ai/user/ahmadabugosh)

### License/Terms of Use:


## Use Case:

Developers, creators, and social media operators use this skill to let an agent list Buffer profiles, create immediate posts, queue or schedule posts, and save draft ideas from a CLI-backed workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles a live Buffer API key and can send it to a configured API URL.

Mitigation: Use only a Buffer API key acceptable for this tool, keep BUFFER_API_URL fixed to Buffer's official HTTPS API, and rotate the key if configuration exposure is suspected.

Risk: Posting to all connected profiles can publish or queue content more broadly than intended.

Mitigation: Verify profile IDs before posting, avoid --all until targets are confirmed, and test workflows with drafts or queueing first.

Risk: Local environment files can expose Buffer credentials if committed or shared.

Mitigation: Store credentials in a local .env file only when needed and ensure .env is ignored by version control before adding secrets.

Risk: Flagged dependencies may carry known issues until updated.

Mitigation: Update the flagged dependencies before operational use and re-run the security review after dependency changes.

## Reference(s):

- [Buffer Developer Docs](https://developers.buffer.com/)
- [Buffer API Key Settings](https://publish.buffer.com/settings/api)
- [ClawHub Skill Page](https://clawhub.ai/ahmadabugosh/skills/buffer-social)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and terminal output text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce Buffer profile IDs, post or idea IDs, queue summaries, validation errors, and setup guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
