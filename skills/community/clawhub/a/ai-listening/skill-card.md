## Description:

Collect what is new in AI in the last 24 hours across X, Hugging Face, GitHub and sitemaps, deduplicated, as one report of names that are starting to surge. Use when the user asks what is new or trending in AI today, wants a daily AI listening report, or needs fresh names of models, products and repositories to feed keyword research. Runs the new-term-radar command line; needs an AISA_API_KEY.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhuyansen](https://clawhub.ai/user/zhuyansen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI market researchers use this skill to collect a daily snapshot of emerging AI models, products, and repositories, with source locations and signal strength, for follow-up research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid X-source runs use an AISA key and can incur costs based on the configured accounts.

Mitigation: Protect the key, review configured accounts and sites, and approve the estimated cost before paid runs.

Risk: The external new-term-radar package is a separate dependency whose implementation was not verified in this review.

Mitigation: Prefer the pinned uvx command and review dependency updates before use.

## Reference(s):

- [AIsa API key information](https://go.aisa.one/yansen-zhu)
- [Example source configuration](https://github.com/zhuyansen/new-term-radar/blob/v0.6.0/config.example.json)

## Skill Output:

**Output Type(s):** [Markdown, Text]

**Output Format:** [Markdown report with emerging names, source links, and signal strengths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [A report covering the last 24 hours; findings depend on configured sources and available prior snapshots.]

## Skill Version(s):

0.6.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
