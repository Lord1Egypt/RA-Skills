## Description:

Helps agents summarize public CCTV short-video and program pages, including video performance, program directories, update status, and topic or ranking statistics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codenova58](https://clawhub.ai/user/codenova58)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to guide an agent through lightweight summaries of public CCTV video collections, program pages, update status, and ranking or topic distributions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill could be misused for downloading, bypassing platform controls, or bulk collection beyond the documented public-page summarization boundary.

Mitigation: Keep use manual and rate-limited, summarize only public pages, and avoid downloads, interface reverse engineering, anti-bot bypass, and bulk scraping.

Risk: Dynamic rendering and human-verification pages may cause incomplete or unreliable page extraction.

Mitigation: Open pages manually when needed, trigger parsing only after the public page is visible, and treat results as lightweight summaries requiring review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/codenova58/skills/cctv)
- [Publisher profile](https://clawhub.ai/user/codenova58)
- [CCTV video homepage](https://tv.cctv.com/)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or structured text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are intended for public-page analysis and should avoid download, reverse-engineering, anti-bot bypass, or bulk-collection workflows.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
