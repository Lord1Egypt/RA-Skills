## Description:

Fetch full text from Twitter/X tweets via fxtwitter API, then translate to Chinese.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dizhu](https://clawhub.ai/user/dizhu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to fetch public Twitter/X tweet text through fxtwitter and translate it into clean Simplified Chinese Markdown. It preserves original structure, URLs, author credit, and a source link for single tweets or threads.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tweet URLs and fetched public tweet text are requested through the public fxtwitter service.

Mitigation: Use this skill for public tweets only and avoid private, sensitive, or access-controlled content.

Risk: Image, video, and quoted-retweet context may be omitted because the skill translates fetched text content.

Mitigation: Review the original tweet when visual media or quoted content may affect meaning.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dizhu/skills/fxtwitter-translate)
- [fxtwitter API endpoint pattern](https://api.fxtwitter.com/:username/status/:tweetId)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Simplified Chinese Markdown with original URLs, author credit, and source link]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Text-only tweet content; images and video are not fetched.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
