## Description:

Generate high-quality Chinese information briefings for AI, technology, and global expansion topics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kelcey2023](https://clawhub.ai/user/kelcey2023)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, operators, founders, investors, and content teams use this skill to produce Chinese daily news digests, weekly deep briefings, trend tracking, internal notes, and publishable summaries for AI, technology, and global expansion topics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may inspect logged-in, private, internal, or subscription pages when browser snapshots are used for research.

Mitigation: Prefer public web_search and web_fetch sources; use non-public pages only when the user explicitly chooses the exact page and is comfortable with its contents being summarized or reused.

Risk: Recurring reminders could repeatedly run broad research and summarization with more access or scope than intended.

Mitigation: Disable recurring reminders by default, or tightly scope them to public sources, a clear topic, cadence, and output format.

## Reference(s):

- [Skill source](artifact/SKILL.md)
- [Query patterns](artifact/references-query-patterns.md)
- [Scoring, de-duplication, and publishable formatting](artifact/references-scoring-and-format.md)
- [No-key fallback sources](artifact/references-no-key-sources.md)
- [ClawHub skill page](https://clawhub.ai/kelcey2023/skills/ai-high-quality-briefing)
- [arXiv AI recent papers](https://arxiv.org/list/cs.AI/recent)
- [GitHub Trending](https://github.com/trending)
- [Hugging Face trending models](https://huggingface.co/models?sort=trending)
- [Hacker News](https://news.ycombinator.com/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Configuration]

**Output Format:** [Chinese Markdown briefing with source links and optional publishable copy variants]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include social, public-account, or internal-briefing variants; may note limited source coverage when broad search is unavailable.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
