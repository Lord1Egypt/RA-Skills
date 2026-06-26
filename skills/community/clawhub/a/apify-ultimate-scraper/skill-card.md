## Description: <br>
Universal AI-powered web scraper for any platform. Scrape data from Instagram, Facebook, TikTok, YouTube, Google Maps, Google Search, Google Trends, Booking.com, and TripAdvisor. Use for lead generation, brand monitoring, competitor analysis, influencer discovery, trend research, content analytics, audience analysis, or any data extraction task. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[apify](https://clawhub.ai/user/apify) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, analysts, and business users use this skill to select and run Apify Actors for public web-data extraction across social, search, maps, travel, and review platforms. It supports lead generation, brand monitoring, competitor analysis, influencer discovery, trend research, content analytics, audience analysis, and related extraction tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run broad third-party Apify Actors with the user's APIFY_TOKEN, which may cause unintended scraping activity or cost. <br>
Mitigation: Before each run, confirm the exact Actor, whether it came from the curated list or store search, expected cost, permission level, target site rules, and result limits. <br>
Risk: Scraper outputs may include emails, phone numbers, comments, followers, profile information, or other personal data from public sources. <br>
Mitigation: Handle exported CSV and JSON files as sensitive data and collect only data permitted by the target site's rules and the user's intended use. <br>


## Reference(s): <br>
- [Apify Ultimate Scraper on ClawHub](https://clawhub.ai/apify/apify-ultimate-scraper) <br>
- [Apify](https://apify.com) <br>
- [Apify Actor API](https://api.apify.com/v2/acts/:actorId) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text, files] <br>
**Output Format:** [Markdown guidance with bash commands, chat summaries, and optional CSV or JSON exports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires APIFY_TOKEN, Node.js, and mcpc; exported files are written under the current working directory.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter says 1.0.8) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
