## Description:

Collects AI industry news from RSS and web sources, filters and classifies items, generates Chinese titles and summaries, and exports Excel tables and Word briefings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nighmat1220](https://clawhub.ai/user/nighmat1220)

### License/Terms of Use:

MIT-0

## Use Case:

Analysts and operations teams use this skill to monitor priority AI companies and broader AI industry events, then produce Chinese briefing materials for daily review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Configured RSS and web sources can direct the crawler to arbitrary URLs, including unwanted internal network locations.

Mitigation: Use only trusted source spreadsheets and config.yaml values, and run the workflow with network controls that block localhost, cloud metadata, and private intranet ranges.

Risk: Optional AI summarization can send article content and an Ark API key to a configured model endpoint.

Mitigation: Keep ARK_API_KEY in the environment, keep ark.base_url pointed at the official Volcengine Ark endpoint, and avoid submitting confidential articles.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nighmat1220/skills/ai-news-workflow)
- [Artifact README](artifact/README.md)
- [Artifact skill summary](artifact/SKILL.md)
- [Default configuration](artifact/config.default.yaml)

## Skill Output:

**Output Type(s):** [text, files, configuration]

**Output Format:** [Plain text status with generated Excel workbooks and Word documents]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes reports under ./output/excel and ./output/word; optional AI summarization uses ARK_API_KEY.]

## Skill Version(s):

0.1.3 (source: server release evidence; artifact skill.yaml reports 0.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
