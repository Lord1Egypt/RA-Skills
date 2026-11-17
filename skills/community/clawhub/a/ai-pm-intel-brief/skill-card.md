## Description:

Create a daily AI PM intelligence brief from Twitter/X or similar high-signal sources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qrg-cloud](https://clawhub.ai/user/qrg-cloud)

### License/Terms of Use:

MIT-0

## Use Case:

External users and product teams use this skill to turn recent social posts and curated account watchlists into concise AI product-management intelligence briefs with key signals, product implications, excerpts, and links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Briefs may overstate weak or incomplete social-media signals if source coverage is partial or noisy.

Mitigation: State coverage limits briefly, filter aggressively, and prefer a smaller set of high-signal posts over exhaustive feed summaries.

Risk: The default output template is Chinese-first and may not match every user's expected language or format.

Mitigation: Ask for or honor the user's preferred language and structure when they specify one.

## Reference(s):

- [Output Template](artifact/references/output-template.md)
- [Default Watchlist](artifact/references/watchlist.txt)
- [ClawHub Skill Page](https://clawhub.ai/qrg-cloud/skills/ai-pm-intel-brief)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown brief with concise judgments, synthesized signal summaries, optional short excerpts, and original links.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-first default template; users can request another language, source set, time range, or brief structure.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
