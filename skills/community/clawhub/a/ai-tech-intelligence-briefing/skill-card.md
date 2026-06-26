## Description: <br>
Automatically curates and summarizes daily AI and tech news worldwide, delivering concise, time-zone aware briefings for quick updates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[greatworks](https://clawhub.ai/user/greatworks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Professionals, teams, and community maintainers use this skill to generate short AI and technology briefings for daily scanning, sharing, or saved local updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A broad natural-language trigger may create local briefing files in the configured output directory. <br>
Mitigation: Set BRIEFING_OUTPUT_DIR to an intended location and review generated files before sharing or relying on them. <br>
Risk: Fetch commands that are not date-like may target unintended local Markdown filenames. <br>
Mitigation: Use explicit YYYY-MM-DD dates when fetching saved briefings. <br>
Risk: Documentation advertises live news fetching, while reviewed runtime behavior currently uses built-in demo content. <br>
Mitigation: Treat generated briefings as sample or locally generated summaries unless live-source fetching is independently verified. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/greatworks/ai-tech-intelligence-briefing) <br>
- [Publisher profile](https://clawhub.ai/user/greatworks) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, shell commands, configuration] <br>
**Output Format:** [Plain text briefing or Markdown file saved under briefings/YYYY-MM-DD.md] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Environment variables configure language, region, story count, and output directory.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
