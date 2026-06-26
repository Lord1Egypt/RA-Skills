## Description: <br>
Extracts YouTube transcripts and video metadata to support video analysis, content ideas, and blog post drafting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[akkualle](https://clawhub.ai/user/akkualle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and content teams use this skill to turn YouTube video IDs or URLs into transcripts, key points, content ideas, quotes, FAQs, and draft blog-post material. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Using the skill can send requested video identifiers or URLs to YouTube/Google or optional transcript tools. <br>
Mitigation: Use a restricted YouTube API key and verify any local helper, Python package, or yt-dlp command before running it. <br>
Risk: The required YouTube API key could be exposed if stored or shared carelessly. <br>
Mitigation: Keep the .env file private and avoid committing or pasting API keys into shared outputs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/akkualle/akkualle-youtube-transcript) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with transcript excerpts, video metadata, key points, and content ideas] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Primary use requires YOUTUBE_API_KEY; alternative transcript workflows may use yt-dlp or youtube-transcript-api.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
