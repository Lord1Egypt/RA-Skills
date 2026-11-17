## Description:

Posts a user-provided image to the Synerunify appearance prediction API and returns face appearance scores with face regions and image size.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qiushosens](https://clawhub.ai/user/qiushosens)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill when asked to score one or more faces in a photo. It uploads the image to Synerunify and reports scores, face regions, image size, and failures in user-facing terms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uploads user-provided photos, including any faces in them, to Synerunify for processing.

Mitigation: Use only images you have permission to share and are comfortable uploading to that external service.

## Reference(s):

- [Synerunify Appearance Predict API](https://synerunify.com/api/process/appearance/predict)
- [ClawHub Skill Page](https://clawhub.ai/qiushosens/skills/appearance-score)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown or plain text with JSON-derived score summaries and optional bash or Python examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scores for multiple faces should be sorted left-to-right; failures should surface the API message and HTTP status.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
