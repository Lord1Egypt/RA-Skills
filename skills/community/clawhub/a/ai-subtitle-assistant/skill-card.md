## Description: <br>
Download YouTube subtitles and use AI to summarize, translate, or extract key points. No login or cookies required. Powered by evolink.ai <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[evolinkai](https://clawhub.ai/user/evolinkai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to download public YouTube subtitles, summarize video content, translate transcripts, and extract key points from YouTube URLs or local subtitle files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: AI commands send the selected subtitle or transcript text to EvoLink's API for processing. <br>
Mitigation: Use only the download and languages commands when API transmission is not acceptable, and avoid passing sensitive non-subtitle files to summarize, translate, or keypoints. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/evolinkai/ai-subtitle-assistant) <br>
- [Project Homepage](https://github.com/EvoLinkAI/subtitle-skill-for-openclaw) <br>
- [EvoLink API Documentation](https://docs.evolink.ai/en/api-manual/language-series/claude/claude-messages-api?utm_source=clawhub&utm_medium=skill&utm_campaign=subtitle) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Shell commands, Guidance] <br>
**Output Format:** [Terminal text, Markdown-formatted analysis, and downloaded subtitle text files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Download and language listing commands avoid EvoLink transmission; summarize, translate, and keypoints commands require EVOLINK_API_KEY and send selected transcript text to EvoLink's API.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata, SKILL.md frontmatter, and npm/package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
