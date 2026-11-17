## Description:

find-ebooks / 搜好书 searches Anna's Archive for EPUB/PDF ebooks, extracts book metadata and download links, and compares availability across six Chinese book platforms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leisurelinux](https://clawhub.ai/user/leisurelinux)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to search for ebook metadata, discover EPUB/PDF availability, and collect related purchase or search links across Chinese book platforms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms are sent to Anna's Archive and multiple third-party book platforms.

Mitigation: Avoid sensitive search terms and use the skill only where those third-party requests are acceptable.

Risk: Results may include copyright-sensitive download links.

Mitigation: Use the skill only for lawful book discovery and access.

Risk: Setting WEREAD_API_KEY can make account-linked WeRead requests.

Mitigation: Leave WEREAD_API_KEY unset unless account-linked lookup is intentional, and store the token securely.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/leisurelinux/skills/find-ebooks)
- [Publisher profile](https://clawhub.ai/user/leisurelinux)
- [Anna's Archive](https://annas-archive.gd)
- [Douban Book](https://book.douban.com)
- [iReader](https://www.ireader.com)
- [Tmall Books](https://list.tmall.com)
- [Dangdang](https://search.dangdang.com)
- [JD Books](https://search.jd.com)
- [China Machine Press](https://www.cmpbook.com)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [Markdown report with overview tables and per-book detail blocks, or JSON when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes complete single-line URLs; supports proxy configuration and optional WeRead account-linked lookup via WEREAD_API_KEY.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
