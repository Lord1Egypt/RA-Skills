## Description:

Post to X through the logged-in Ego Lite session, with optional images and a user confirmation step before sending.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terryso](https://clawhub.ai/user/terryso)

### License/Terms of Use:

MIT-0

## Use Case:

People using a signed-in Ego Lite session can draft and publish posts or replies on X, including supported image attachments. The skill checks login first and requires the person to review the draft before sending.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fallback session checks can accept cookies from unrelated sites.

Mitigation: Use a browser profile dedicated to the intended X account; require corrected cookie-domain filtering and strict HTTPS origin checks before using a profile with other signed-in accounts. Confirm the exact post text and images before enabling --yes.

## Reference(s):

- [CreateTweet and CreateNoteTweet reference](artifact/references/create-tweet.md)
- [X login reference](artifact/references/login.md)
- [Image upload reference](artifact/references/media-upload.md)
- [X posting pitfalls](artifact/references/pitfalls.md)

## Skill Output:

**Output Type(s):** [Text, JSON, URLs]

**Output Format:** [Draft text or a status URL; optional JSON summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [A successful post returns its X status URL; --json returns a summary.]

## Skill Version(s):

0.2.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
