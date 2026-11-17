## Description:

AI tool that generates structured news digests from Twitter, RSS, and other feeds with summaries available in 4-hour, daily, weekly, or monthly formats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ma-star](https://clawhub.ai/user/ma-star)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use Clawfeed to deploy a local or hosted digest service that curates Twitter, RSS, and other sources into scheduled summaries, feed outputs, bookmarks, and source packs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The server and test behavior can affect more than a user may reasonably expect.

Mitigation: Review before installing or deploying, and run only in a controlled local or protected environment.

Risk: Public deployment can expose API, session, OAuth, or source-resolution attack surfaces.

Mitigation: Set strong API, session, and OAuth secrets, restrict allowed origins, use HTTPS-only webhooks, and address source-resolver SSRF controls before public exposure.

Risk: The test suite may target non-local services if AI_DIGEST_API or AI_DIGEST_FEED are not isolated.

Mitigation: Run tests only against an isolated local test server with explicit AI_DIGEST_API and AI_DIGEST_FEED values.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ma-star/skills/clawfeed-3)
- [Skill entry documentation](artifact/SKILL.md)
- [Product documentation](artifact/docs/PRODUCT.md)
- [Architecture documentation](artifact/docs/ARCHITECTURE.md)
- [Testing documentation](artifact/docs/TESTING.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May also produce digest content and RSS or JSON feed output when deployed.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata; artifact package.json and CHANGELOG report 0.8.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
