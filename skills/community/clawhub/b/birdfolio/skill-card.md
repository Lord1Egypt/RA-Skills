## Description: <br>
Bird identification, life list tracking, and trading card generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tonbistudio](https://clawhub.ai/user/tonbistudio) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use Birdfolio to identify birds from photos, track personal sightings and checklist progress, and generate shareable bird trading cards. The skill also supports setup, regional rarity lookup, species facts, and life-list summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Birdfolio stores bird photos locally and sends Telegram-linked sightings to a hosted API. <br>
Mitigation: Use only with non-sensitive photos and review the configured API endpoint, local workspace contents, and Telegram identifier before setup or logging sightings. <br>
Risk: Generated cards may be uploaded to Cloudflare R2 and become public. <br>
Mitigation: Confirm upload intent before running the upload step, and avoid sharing cards that include private locations, people, or sensitive image content. <br>
Risk: The skill guidance allows broad local temp or media folder searching when a submitted photo path is unavailable. <br>
Mitigation: Prefer explicit attachment paths and limit any fallback file search to the expected media directory and current user request. <br>


## Reference(s): <br>
- [Birdfolio on ClawHub](https://clawhub.ai/tonbistudio/birdfolio) <br>
- [tonbistudio publisher profile](https://clawhub.ai/user/tonbistudio) <br>
- [Data schema](references/data-schema.md) <br>
- [Search query templates](references/you-search-queries.md) <br>
- [Birdfolio hosted API](https://api-production-d0e2.up.railway.app) <br>
- [Birdfolio PWA](https://birdfolio.tonbistudio.com/app/[telegram_id]) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses with JSON-producing script commands and generated HTML/PNG card files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local Birdfolio configuration, checklist, sighting, bird photo, HTML card, and PNG card files; may call a hosted API and upload card images to Cloudflare R2.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
