## Description:

Bird identification, life list tracking, and trading card generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tonbistudio](https://clawhub.ai/user/tonbistudio)

### License/Terms of Use:


## Use Case:

External users use Birdfolio to identify birds from photos, initialize a regional checklist, log sightings, review life-list statistics, and generate visual trading cards from their own photos.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can store a user's Telegram ID, home region, bird photos, sightings, and generated cards.

Mitigation: Require clear user confirmation before setup or logging, keep data in a dedicated workspace, and document deletion and retention controls.

Risk: Generated card images may be uploaded to public cloud storage.

Mitigation: Confirm before upload, avoid sensitive photos, verify bucket public-access settings, and provide a removal path for uploaded cards.

Risk: Scripts call external services and accept workspace paths or image sources.

Mitigation: Review the API URL before use, restrict workspace and image paths to expected locations, and prefer user-supplied local photos over fetched image URLs.

## Reference(s):

- [Birdfolio Skill Page](https://clawhub.ai/tonbistudio/skills/birdfolio)
- [tonbistudio Publisher Profile](https://clawhub.ai/user/tonbistudio)
- [Birdfolio Data Schemas](references/data-schema.md)
- [Birdfolio You.com Search Query Templates](references/you-search-queries.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with JSON script outputs, shell command examples, and generated HTML/PNG card files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses user-submitted photos and regional bird data to log sightings and generate cards.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
