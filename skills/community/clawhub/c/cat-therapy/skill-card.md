## Description:

Cat Therapy helps users take short relaxation breaks by returning cat images, meow text or audio cues, and bilingual calming quotes, with optional user-provided cat media.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yyxy](https://clawhub.ai/user/yyxy)

### License/Terms of Use:

MIT-0

## Use Case:

External users can invoke this skill in chat platforms when they want a brief stress-relief break with cat images, simple sound cues, and short calming messages. Users can also save a preferred image or sound for later responses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package includes saved user metadata for custom cat media.

Mitigation: Remove bundled user preference data before release and document what user photos or sounds are stored and for how long.

Risk: Broad auto-response triggers may activate the skill in more conversations than intended.

Mitigation: Narrow or confirm trigger phrases before deployment so responses occur only on clear user intent.

Risk: Language file selection could read unexpected locale files if inputs are not constrained.

Mitigation: Restrict language selection to the documented zh and en allowlist.

## Reference(s):

- [ClawHub Cat Therapy Skill](https://clawhub.ai/yyxy/skills/cat-therapy)
- [TheCatAPI image search endpoint](https://api.thecatapi.com/v1/images/search)
- [Cataas cat image service](https://cataas.com/cat)
- [PlaceKitten fallback image source](https://placekitten.com/400/300)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, API Calls, Files, Configuration]

**Output Format:** [Chat text with media URLs and JSON response data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include image URLs, TTS text, localized quotes, and locally stored user preference data.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
