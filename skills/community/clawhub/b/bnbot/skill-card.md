## Description:

BNBot helps agents automate Twitter/X through a real browser session and CLI tools for posting, engagement, scraping, profiles, articles, and jobs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jackleeio](https://clawhub.ai/user/jackleeio)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use BNBot to let an agent operate a Twitter/X browser session through the bnbot CLI for account status, navigation, posting, engagement, scraping, content fetching, article publishing, authentication, and job search workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can direct an external CLI and Chrome extension to control an authenticated Twitter/X session, including posting, deleting, following, unfollowing, scraping, publishing articles, and uploading media.

Mitigation: Use it only when that level of account control is acceptable, and manually confirm every account-changing or publishing action before execution.

Risk: The workflow uses a persistent local daemon connected to browser automation.

Mitigation: Check the daemon status before use and stop the local service when BNBot is not actively needed.

Risk: Media parameters accept local file paths and URLs, and local files may be converted for upload.

Mitigation: Avoid passing sensitive local files and review all media inputs before sending them to the CLI.

Risk: Server-resolved provenance is unavailable for this version.

Mitigation: Verify the npm package version and Chrome extension provenance before installation or use.

## Reference(s):

- [BNBot ClawHub Skill Page](https://clawhub.ai/jackleeio/skills/bnbot)
- [BNBot CLI npm Package](https://www.npmjs.com/package/bnbot-cli)
- [BNBot Chrome Extension](https://chromewebstore.google.com/detail/bnbot-your-ai-growth-agen/haammgigdkckogcgnbkigfleejpaiiln)
- [BNBot CLI Homepage](https://github.com/bnbot-ai/bnbot-cli)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with inline shell commands; referenced CLI tool output is JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires bnbot-cli, a running local daemon on port 18900, and the BNBot Chrome Extension connected to an authenticated Twitter/X session.]

## Skill Version(s):

1.5.0 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
