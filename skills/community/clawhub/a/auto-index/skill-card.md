## Description: <br>
Google SEO GEO Auto Index helps agents submit sitemap-derived or user-specified URLs to the Google Indexing API using a Google Cloud service account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[geoly-geo](https://clawhub.ai/user/geoly-geo) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, site operators, and SEO teams use this skill to submit new, updated, or deleted URLs for Google indexing after confirming they control the target site and service account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can submit indexing or deletion notifications for URLs selected from a sitemap or command-line input. <br>
Mitigation: Use it only for sites you control, confirm Google Search Console ownership, and review sitemap and URL inputs before using --force or --delete. <br>
Risk: The Google service account JSON key grants access needed to call the Indexing API. <br>
Mitigation: Use a dedicated least-privilege service account and keep the key path private. <br>
Risk: Cached sitemap state and forced submissions can affect which URLs are sent and may consume quota. <br>
Mitigation: Review the local cache behavior, clear the cache only when intentionally resetting indexing history, and monitor the 200 request per day quota. <br>


## Reference(s): <br>
- [Google Indexing API Quickstart](https://developers.google.com/search/apis/indexing-api/v3/quickstart) <br>
- [ClawHub Skill Page](https://clawhub.ai/geoly-geo/auto-index) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and structured JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write a local sitemap cache at ~/.cache/auto-index/sitemap-cache.json.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
