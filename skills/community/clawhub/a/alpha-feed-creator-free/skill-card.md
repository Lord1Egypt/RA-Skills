## Description: <br>
Alpha Feed Creator Free collects and ranks daily AI content to help individual creators find topic ideas. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, independent bloggers, and AI learners use this skill to collect AI-related X/Twitter posts from configured accounts and keywords, rank them by basic engagement signals, and generate a local Markdown daily brief for Obsidian or another notes workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The artifact contains contradictory SEO trigger text that does not match the AI content collection use case. <br>
Mitigation: Remove or ignore the SEO trigger text before use and only invoke the skill for AI content collection and daily report generation. <br>
Risk: The skill can read configured X/Twitter sources and may use an existing browser or API session. <br>
Mitigation: Run it with a dedicated browser profile or isolated session when normal logged-in browser state should not be touched. <br>
Risk: The skill creates Markdown reports and logs in local paths. <br>
Mitigation: Confirm the output directory before execution and restrict writes to a local path approved for generated reports. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/alpha-feed-creator-free) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/thcjp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown daily reports with local file paths and optional shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local Markdown reports and run logs in a user-approved output directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
