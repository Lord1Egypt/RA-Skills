## Description: <br>
Use this skill when the user wants to make content more likely to be cited or surfaced by AI answer engines such as ChatGPT, Perplexity, Google AI Overviews, Gemini, and Copilot through GEO strategy, content creation or audit, technical markup, and scoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[archlab-space](https://clawhub.ai/user/archlab-space) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content strategists, marketers, editors, and developers use this skill to create or revise pages so they are easier for AI answer engines to cite. It produces a GEO brief, optimized content or audit findings, structured-data and llms.txt guidance, and a scorecard for iteration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated content can include unverified claims, statistics, dates, author credentials, or source attributions if the user does not provide reliable evidence. <br>
Mitigation: Review every factual claim before publishing and keep placeholders such as [verify] until the value is confirmed from a trusted source. <br>
Risk: Structured data or llms.txt entries can misrepresent a page if placeholders are left unresolved or markup describes content that is not actually present. <br>
Mitigation: Replace placeholders with real values, mark up only visible page content, and validate JSON-LD and crawler guidance before shipping. <br>
Risk: Live citation-gap and competitor research may be stale, incomplete, or unavailable depending on web access and source quality. <br>
Mitigation: Treat web research as read-only context, state when live results were unavailable, and avoid presenting unverified competitive claims as fact. <br>


## Reference(s): <br>
- [Geo Content Tactics](references/geo-content-tactics.md) <br>
- [Technical GEO](references/technical-geo.md) <br>
- [schema.org](https://schema.org) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown with structured content briefs, rewrites, scorecards, JSON-LD code blocks, and llms.txt examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include clearly labeled placeholders such as [verify] when facts, dates, authors, sources, or URLs are not confirmed.] <br>

## Skill Version(s): <br>
0.1.0 (source: evidence.release.version and CHANGELOG, released 2026-06-02) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
