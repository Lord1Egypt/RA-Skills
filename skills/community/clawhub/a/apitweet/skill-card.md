## Description:

Apitweet CLI helps agents install, configure, preview, and run ApiTweet Twitter/X workflows from the terminal.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aliraza948](https://clawhub.ai/user/aliraza948)

### License/Terms of Use:

MIT

## Use Case:

Developers, AI agent builders, growth teams, and content operators use this skill to fetch Twitter/X data, manage ApiTweet credentials, preview requests, and perform account workflows through the apitweet CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI handles persistent ApiTweet and Twitter/X credentials, including API keys, cookies, auth_token values, and ct0 values.

Mitigation: Use isolated config directories, avoid shared machines and CI runners, and do not echo or log raw credentials.

Risk: The CLI can perform live social-account actions such as publishing, liking, following, profile updates, direct messages, and article publishing.

Mitigation: Use dry-run previews before write actions and require clear user confirmation before sending live requests.

Risk: Saved credentials can be forwarded to broad or arbitrary request destinations when custom base URLs or full URLs are used.

Mitigation: Avoid custom base URLs or full URLs with saved credentials unless the destination has been explicitly verified.

Risk: Unpinned npx install paths can make package provenance harder to verify.

Mitigation: Prefer pinned or otherwise verified installation sources before installing or executing the CLI.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aliraza948/skills/apitweet)
- [ApiTweet](https://apitweet.com)
- [ApiTweet dashboard](https://apitweet.com/dashboard)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON-oriented CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include dry-run previews and credential-aware command guidance for ApiTweet and Twitter/X workflows.]

## Skill Version(s):

0.1.4 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
