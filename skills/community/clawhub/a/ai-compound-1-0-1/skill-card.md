## Description: <br>
Make your AI agent learn and improve automatically. Reviews sessions, extracts learnings, updates memory files, and compounds knowledge over time. Set up nightly review loops that make your agent smarter every day. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AmanGarg1999](https://clawhub.ai/user/AmanGarg1999) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers and agent users use this skill to set up manual or scheduled review loops that extract lessons from sessions and update agent memory files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unattended memory extraction could capture irrelevant, sensitive, or incorrect session details. <br>
Mitigation: Start with manual review and exclude secrets or sensitive sessions before allowing persistent memory updates. <br>
Risk: Automated edits to MEMORY.md or AGENTS.md could introduce incorrect or misleading guidance into future agent behavior. <br>
Mitigation: Inspect diffs before writing or retaining changes to memory and instruction files. <br>
Risk: Scheduled cron or launchd jobs and git commit or push workflows can run without enough approval controls. <br>
Mitigation: Do not enable scheduled jobs until there is a clear disable path, a review process, and verified git remote and commit contents. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose updates to MEMORY.md, daily memory notes, AGENTS.md, cron or launchd configuration, and git commit workflows for review.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
