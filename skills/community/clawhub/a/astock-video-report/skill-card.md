## Description: <br>
A股每日复盘视频自动生成：拉取非凸科技行情数据、抓取热点新闻、进行 AI 归因分析，并生成横屏 PPT 幻灯片、视频、封面图和发布文案。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eddiexux](https://clawhub.ai/user/eddiexux) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, analysts, and agent users use this skill to turn A-share market data and financial news into a daily recap package with slides, video, cover image, and publication copy. It is intended for informational market commentary, not investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs Python packages, installs dependency skills, and downloads external font and music assets. <br>
Mitigation: Run setup in a virtual environment when possible, review dependencies and downloaded assets before use, and keep asset licensing appropriate for the intended publication. <br>
Risk: Market data, news linkage, and AI attribution can be incomplete or misleading if used without review. <br>
Mitigation: Independently verify financial data and wording before publishing, keep the provided investment disclaimer, and avoid presenting generated commentary as investment advice. <br>
Risk: Video generation creates publishable media after slide generation, so errors can propagate into the final video. <br>
Mitigation: Review and approve the generated slides before video synthesis, especially stock data, index values, news relevance, and attribution text. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/eddiexux/astock-video-report) <br>
- [行情数据字段说明](references/data-schema.md) <br>
- [发布文案生成规范](references/copywriting.md) <br>
- [Pixabay Music](https://pixabay.com/music/) <br>
- [Google Noto Sans SC](https://fonts.google.com/noto/specimen/Noto+Sans+SC) <br>
- [FFmpeg downloads](https://ffmpeg.org/download.html) <br>
- [OpenClaw](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with shell commands and generated files, including PNG slides, an MP4 video, a JPG cover image, and posting copy.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires explicit trading-date confirmation when the market is closed or not open, and slide approval before video synthesis.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
