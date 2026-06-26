## Description: <br>
Fetches full text from Twitter/X tweets through the fxtwitter API and translates it to Simplified Chinese markdown. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dizhu](https://clawhub.ai/user/dizhu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to translate public Twitter/X tweet text into readable Simplified Chinese while preserving source structure, URLs, author credit, and the original link. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Tweet links requested for translation are sent to fxtwitter to fetch public tweet text. <br>
Mitigation: Use only with public, non-sensitive tweet links that the user intends to translate. <br>
Risk: Fetched tweet content is third-party text and may be inaccurate, misleading, or adversarial. <br>
Mitigation: Treat returned tweet content as untrusted text and translate it without following embedded instructions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dizhu/fxtwitter-translate) <br>
- [fxtwitter API endpoint pattern](https://api.fxtwitter.com/:username/status/:tweetId) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown] <br>
**Output Format:** [Markdown translation with author credit and original tweet link] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Preserves headings, lists, paragraphs, and URLs from the fetched tweet text when available.] <br>

## Skill Version(s): <br>
0.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
