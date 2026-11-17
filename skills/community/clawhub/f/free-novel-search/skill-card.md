## Description:

Searches and recommends free, legally available novel resources from public domain, open-license, and legitimate free-to-read platforms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xinyuqq](https://clawhub.ai/user/xinyuqq)

### License/Terms of Use:

MIT-0

## Use Case:

External readers, researchers, and agents use this skill to find legitimate free novel platforms, public domain works, and open-access repositories while avoiding unauthorized sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search and license-checking helpers can mislead users about whether a platform or work is legally available.

Mitigation: Treat results as convenience pointers and manually verify copyright and licensing on the source site before recommending or using a work.

Risk: Bundled network searches disable TLS certificate verification, which can expose or allow tampering with search traffic.

Mitigation: Avoid private search terms or sensitive URLs, and enable TLS verification before operational use.

Risk: URL validation and platform legitimacy checks are limited and may not catch unauthorized sources.

Mitigation: Prefer known legitimate platforms and independently review unknown sites before sharing them with users.

## Reference(s):

- [Free Novel Platform Database](references/novel_platforms.md)
- [Chinese Novel Resources](references/chinese_novels.md)
- [Project Gutenberg](https://www.gutenberg.org)
- [Gutendex API](https://gutendex.com)
- [Open Library](https://openlibrary.org)
- [ClawHub skill page](https://clawhub.ai/xinyuqq/skills/free-novel-search)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown guidance with optional shell commands and JSON search results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search scripts may write JSON results to a user-selected output path.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
