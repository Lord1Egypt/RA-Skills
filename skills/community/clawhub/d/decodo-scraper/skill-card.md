## Description: <br>
Search Google, scrape web pages, Amazon product pages, YouTube subtitles, or Reddit posts and subreddit listings using the Decodo Scraper OpenClaw Skill. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DonatasDecodo](https://clawhub.ai/user/DonatasDecodo) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and AI-agent operators use this skill to route public web, Google Search, Amazon, YouTube subtitle, and Reddit scraping tasks through Decodo's Web Scraping API from an OpenClaw-compatible agent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queries, URLs, video IDs, and retrieved content are sent to Decodo as a third-party scraping provider. <br>
Mitigation: Use the skill only for data you are allowed to share with Decodo, and avoid private, internal, or credential-bearing URLs. <br>
Risk: The Decodo auth token is required for API calls and could grant access if exposed. <br>
Mitigation: Keep DECODO_AUTH_TOKEN out of shared logs and repositories, and pass it through the runtime environment rather than prompts or committed files. <br>
Risk: The package requirements use version ranges without a lockfile. <br>
Mitigation: Pin dependencies or use a lockfile in production environments. <br>


## Reference(s): <br>
- [ClawHub Decodo Scraper page](https://clawhub.ai/DonatasDecodo/decodo-scraper) <br>
- [Decodo homepage](https://decodo.com) <br>
- [Decodo Web Scraping API documentation](https://help.decodo.com/docs/web-scraping-api-introduction) <br>
- [Decodo Google Search scraping API documentation](https://help.decodo.com/docs/web-scraping-api-google-search) <br>
- [OpenClaw getting started documentation](https://docs.openclaw.ai/start/getting-started) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with CLI commands; executed scraper calls return JSON, Markdown, or plain text transcripts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires DECODO_AUTH_TOKEN and sends selected queries, URLs, and video IDs to Decodo's API.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
