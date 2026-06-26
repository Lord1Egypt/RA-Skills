## Description: <br>
Auto News Podcast generates news briefings from user-provided keywords by searching for news, summarizing results, writing broadcast scripts, finding cover images, and producing spoken audio. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiazengtian](https://clawhub.ai/user/jiazengtian) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and content teams use this skill to generate single or batch news podcast packages from a topic or event keyword, including summaries, broadcast scripts, cover imagery, and audio narration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read OpenClaw model configuration and API keys and send search terms, news text, and prompts to external search, model, image, and speech providers. <br>
Mitigation: Use limited-scope API keys, verify provider base URLs before use, and avoid submitting sensitive or private topics as prompts. <br>
Risk: The security evidence says the skill can automatically run other installed helper skills. <br>
Mitigation: Install and pair it only with trusted helper skills, and review generated files and invoked tools before deployment. <br>
Risk: Generated news summaries and narration may contain stale, incomplete, or misleading information from upstream search and model providers. <br>
Mitigation: Review source results, summaries, scripts, and final audio before publishing or using them in decision-making contexts. <br>


## Reference(s): <br>
- [Auto news podcast on ClawHub](https://clawhub.ai/jiazengtian/auto-news-podcast) <br>
- [jiazengtian publisher profile](https://clawhub.ai/user/jiazengtian) <br>
- [Unsplash Developers](https://unsplash.com/developers) <br>
- [Unsplash Photo Search API](https://api.unsplash.com/search/photos) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Audio files, Image files, Configuration] <br>
**Output Format:** [Markdown summaries and reports, plain-text broadcast scripts, MP3 narration files, JPEG cover images, and configuration summaries written to workspace/news/] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports single-broadcast and batch workflows, optional dual-host dialogue, and optional event deep analysis outputs.] <br>

## Skill Version(s): <br>
1.0.12 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
