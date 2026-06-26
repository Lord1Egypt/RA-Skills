## Description: <br>
Douyin Video Forge helps short-video operators collect Douyin trend signals, plan content, generate scripts, optionally call Kling for AI video generation, and assemble vertical video outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Bruce-Agnet](https://clawhub.ai/user/Bruce-Agnet) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External operators, MCN teams, and brand marketers use this skill to turn campaign briefs and current Douyin trend data into video directions, scripts, and optional AI-generated short-video assets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create ongoing scheduled jobs for multi-day publishing workflows. <br>
Mitigation: Review the exact scheduled job before enabling it, confirm how to disable it, and avoid enabling automation for campaigns that require manual approval each day. <br>
Risk: The skill automates Douyin browsing, scraping, and local video downloads. <br>
Mitigation: Use only when the operator is comfortable with platform access, rights, and local storage implications, and review downloaded media before reuse. <br>
Risk: Optional Kling API video generation may upload prompts or assets and spend API credits. <br>
Mitigation: Configure Kling credentials only when needed, keep keys in environment variables, and verify generated tasks and expected costs before multi-segment or scheduled generation. <br>
Risk: The install flow can overwrite the existing skill install directory. <br>
Mitigation: Back up local edits before reinstalling or upgrading the skill. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Bruce-Agnet/douyin-video-forge) <br>
- [Publisher Profile](https://clawhub.ai/user/Bruce-Agnet) <br>
- [Browser Navigation Reference](artifact/references/browser-navigation.md) <br>
- [Douyin Algorithm Reference](artifact/references/douyin-algorithm.md) <br>
- [Trend Analysis Reference](artifact/references/trend-analysis.md) <br>
- [Script Templates](artifact/references/script-templates.md) <br>
- [Kling Prompt Guide](artifact/references/kling-prompt-guide.md) <br>
- [Seedance Prompt Guide](artifact/references/seedance-prompt-guide.md) <br>
- [Kling AI](https://klingai.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with scripts, command blocks, JSON API responses, and generated media file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May output campaign plans, analysis reports, segmented video scripts, Kling or Seedance prompts, shell commands, and local MP4 paths when video generation is enabled.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
