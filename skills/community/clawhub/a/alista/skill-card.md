## Description:

Save restaurants, bars, and cafes from TikTok and Instagram videos. Search your saved places and get weekend suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bgrober](https://clawhub.ai/user/bgrober)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use Alista to save restaurants, bars, cafes, and events from Instagram or TikTok posts into a local SQLite bookmark database, then search saved places or ask for weekend suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Social-media URLs, captions, tagged users, transcripts, media metadata, and place queries may be sent to Apify and Google Places.

Mitigation: Use the skill only when that data sharing is acceptable, and provide API keys only in workspaces authorized for those services.

Risk: The security evidence says the social-media fetcher can be tricked into contacting non-social or local network URLs.

Mitigation: Avoid processing untrusted links until URL validation is fixed, and run the skill in a tightly network-restricted workspace.

Risk: Optional media download and frame extraction can write files outside the intended workspace.

Mitigation: Avoid --download-images and --extract-frames for untrusted links, or pass only reviewed output directories inside an isolated workspace.

## Reference(s):

- [Alista ClawHub Skill Page](https://clawhub.ai/bgrober/skills/alista)
- [Publisher Profile](https://clawhub.ai/user/bgrober)
- [Google Places API](https://console.cloud.google.com/apis/library/places-backend.googleapis.com)
- [Apify Console](https://console.apify.com/)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Conversational Markdown with inline shell commands, JSON script output, and local SQLite data files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update a local alista.db SQLite database and optional downloaded image or frame files when those script options are used.]

## Skill Version(s):

1.1.1 (source: release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
