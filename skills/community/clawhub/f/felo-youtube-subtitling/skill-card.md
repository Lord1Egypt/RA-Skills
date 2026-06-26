## Description: <br>
Fetches YouTube video subtitles or captions using the Felo YouTube Subtitling API, with support for video IDs or URLs, optional language selection, and optional timestamps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangzhiming1999](https://clawhub.ai/user/wangzhiming1999) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, agents, and end users use this skill to retrieve YouTube subtitles or transcripts for analysis, translation, summarization, or downstream processing when they have a Felo API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends requested YouTube video IDs or URLs to Felo's API and uses a Felo API key. <br>
Mitigation: Install and run it only when you trust Felo with those video identifiers and the configured API key. <br>
Risk: Installing the optional global felo-ai npm package or redirecting FELO_API_BASE can change the code or service endpoint used for subtitle retrieval. <br>
Mitigation: Prefer the bundled script, verify any global npm package before installation, and avoid setting FELO_API_BASE to an untrusted server. <br>


## Reference(s): <br>
- [Felo YouTube Subtitling API](https://openapi.felo.ai/docs/api-reference/v2/youtube-subtitling.html) <br>
- [Felo Open Platform](https://openapi.felo.ai/docs/) <br>
- [ClawHub Skill Page](https://clawhub.ai/wangzhiming1999/felo-youtube-subtitling) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Plain text transcript, timestamped text, or full JSON API response] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires FELO_API_KEY; optional language and timestamp parameters affect transcript content.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
