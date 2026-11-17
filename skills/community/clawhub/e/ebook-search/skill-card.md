## Description:

Search and download Chinese and English ebooks from jbiaojerry.github.io/ebook-treasure-chest by title, author, category, or keyword.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eyslce](https://clawhub.ai/user/eyslce)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to search a large ebook catalog, browse categories, and present matching titles with available formats and third-party download links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill disables TLS verification while downloading the ebook catalog, so an intercepted connection could replace catalog data or unsafe links.

Mitigation: Fix TLS verification before use on shared, corporate, public, or otherwise untrusted networks.

Risk: The skill presents third-party ebook download links.

Mitigation: Treat displayed download links as untrusted until verified by the user or deployment owner.

Risk: The skill stores a local ebook catalog cache in the user's home cache directory.

Mitigation: Review cache location and retention expectations before deployment in managed or shared environments.

## Reference(s):

- [Ebook Search ClawHub listing](https://clawhub.ai/eyslce/skills/ebook-search)
- [Ebook Treasure Chest book database](https://jbiaojerry.github.io/ebook-treasure-chest/all-books.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and plain-text search results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include ebook titles, authors, categories, available formats, and third-party download links.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
