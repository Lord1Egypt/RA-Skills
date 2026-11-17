## Description:

Fetch DMM/FANZA public rankings (daily/weekly/monthly) without API keys and output top 10 in numbered text format with Japanese title, Chinese translation, and cover image URL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leeeroyjoy-pixel](https://clawhub.ai/user/leeeroyjoy-pixel)

### License/Terms of Use:


## Use Case:

External users use this skill to collect public DMM/FANZA daily, weekly, or monthly ranking entries and receive a numbered Top N summary with Japanese titles, Chinese translations, and cover image URLs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill opens and extracts entries from DMM/FANZA adult-content ranking pages.

Mitigation: Install and use only in environments where adult-content browsing is permitted and appropriate.

Risk: Ranking page structure can change, causing incomplete or failed extraction.

Mitigation: Inspect the page snapshot and update selectors before relying on results when extraction returns too few entries.

Risk: Chinese title translations may be imprecise or over-literal.

Mitigation: Review translated titles before publishing or reusing them in user-facing material.

## Reference(s):

- [DMM/FANZA Ranking Page](https://video.dmm.co.jp/av/ranking/?term=<term>)
- [ClawHub Skill Page](https://clawhub.ai/leeeroyjoy-pixel/skills/dmm-ranking-lite)
- [ClawHub Publisher Profile](https://clawhub.ai/user/leeeroyjoy-pixel)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Guidance]

**Output Format:** [Numbered text or Markdown list with fixed title, translation, and cover URL fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default output language is zh-CN while preserving the original Japanese title.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
