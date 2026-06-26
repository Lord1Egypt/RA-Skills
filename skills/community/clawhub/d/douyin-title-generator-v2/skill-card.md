## Description: <br>
Generates Douyin short-video title suggestions in multiple Chinese content styles, with simple estimated view, engagement, and recommendation metrics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yyq56565656](https://clawhub.ai/user/yyq56565656) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Douyin creators, marketers, and content operators use this skill to generate batches of Chinese short-video title options by topic, style, audience, and trend term. The reported view, engagement, and recommendation values should be treated as directional, unvalidated estimates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The PowerShell wrapper can evaluate user-supplied text as commands. <br>
Mitigation: Run the Python script directly with trusted inputs, or replace Invoke-Expression with structured argument passing before using the wrapper. <br>
Risk: The skill reports view, engagement, recommendation, and algorithm-optimization estimates that are not supported by validation evidence. <br>
Mitigation: Treat these metrics as illustrative copywriting hints and validate title performance with real platform analytics before relying on them. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/yyq56565656/douyin-title-generator-v2) <br>
- [README](artifact/README.md) <br>
- [Skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands] <br>
**Output Format:** [Plain text or Markdown-style report with generated titles and estimated metrics] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Randomized local output; performance estimates are illustrative and should not be treated as real forecasts.] <br>

## Skill Version(s): <br>
2.0.0 (source: evidence.release.version and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
