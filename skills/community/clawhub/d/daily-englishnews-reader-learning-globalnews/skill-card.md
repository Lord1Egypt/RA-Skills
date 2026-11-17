## Description:

Generates CEFR-adapted English reading materials from current global news sources and publishes them as a Feishu cloud document.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chegangan](https://clawhub.ai/user/chegangan)

### License/Terms of Use:

MIT-0

## Use Case:

External users and language learners use this skill to generate English reading practice from global news, with passages rewritten to a selected CEFR level and paired with i+1 vocabulary explanations. The skill creates a Feishu cloud document containing the generated readings, source links, and vocabulary notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup instructions use unpinned npm and pip installs and mention retrying the npm installer with sudo.

Mitigation: Install as an unprivileged user, avoid sudo, and prefer pinned reviewed package versions before deployment.

Risk: The skill creates Feishu cloud documents and requires Feishu authorization.

Mitigation: Review requested Feishu authorization scopes before granting access and confirm generated documents are shared only with intended recipients.

Risk: The skill fetches external RSS articles and stores local article history for deduplication.

Mitigation: Review the configured RSS source list and treat the local article history as operational data that may need retention controls.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chegangan/skills/daily-englishnews-reader-learning-globalnews)
- [Al Jazeera English RSS source](https://morss.it/:format=json/https://www.aljazeera.com/xml/rss/all.xml)
- [Vox Business RSS source](https://morss.it/:format=json/https://www.vox.com/rss/business-and-finance/index.xml)
- [Cloudflare Blog RSS source](https://morss.it/:format=json/https://blog.cloudflare.com/rss/)
- [The Conversation RSS source](https://morss.it/:format=json/https://theconversation.com/us/articles.atom)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown-style reading materials, vocabulary explanations, source URLs, and a Feishu document link]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses configurable CEFR level, words per article, and vocabulary count; keeps local article history for deduplication.]

## Skill Version(s):

1.0.1 (source: server release metadata; skill frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
