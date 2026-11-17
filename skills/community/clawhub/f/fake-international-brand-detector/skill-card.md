## Description:

Checks public brand signals across websites, sales channels, marketplaces, media exposure, WHOIS, trademark timing, and seller location to classify whether a brand appears internationally established, suspicious, or falsely international.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tompchen](https://clawhub.ai/user/tompchen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to investigate brand authenticity claims and generate leads for follow-up review before purchasing, legal, or reputational decisions. It is most useful for checking supplement or consumer brands that claim overseas origin or mature international presence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Brand names may be sent to public websites and Tavily during checks.

Mitigation: Do not use sensitive unreleased brand names, and run the skill only when external lookups are acceptable.

Risk: The skill can produce overconfident authenticity verdicts from hard-coded or weak evidence.

Mitigation: Treat verdicts as investigative leads and require human review before purchasing, legal, or reputational decisions.

Risk: Unsafe input handling can make arbitrary URL-like brand strings risky.

Mitigation: Pass plain brand names only and avoid arbitrary URL-like strings as inputs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tompchen/skills/fake-international-brand-detector)
- [Publisher profile](https://clawhub.ai/user/tompchen)
- [API and data source list](artifact/reference/apis.md)
- [Content quality standards](artifact/reference/quality-standards.md)
- [Known international brands database](artifact/reference/known_international_brands.json)
- [Brand examples](artifact/reference/brand-examples.json)
- [Wayback Machine](https://web.archive.org/)
- [Tavily Search](https://tavily.com/search)
- [NewsAPI](https://newsapi.org/)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Terminal text with optional JSON or Markdown brand verification reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports include brand name, timestamp, verification findings, scores, verdict, confidence, and recommendation when supported by the selected script.]

## Skill Version(s):

2.1.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
