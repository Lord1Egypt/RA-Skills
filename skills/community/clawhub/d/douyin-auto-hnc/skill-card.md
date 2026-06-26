## Description: <br>
Automates Douyin content operations across Windows, macOS, and Linux, including setup, AI rewriting, long-form image/text publishing, comment replies, and optional cron scheduling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hnc87](https://clawhub.ai/user/hnc87) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creators use this skill to configure and run a local Douyin publishing pipeline for AI and quantitative-finance content, including dry runs, scheduled publishing, and comment reply workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate a logged-in Douyin browser session and perform public publishing or comment replies. <br>
Mitigation: Use a separate Douyin account and isolated Chrome profile, run dry-run mode first, and manually review generated posts and reply behavior before enabling live runs. <br>
Risk: Setup and runtime workflows require broad local authority, including package installation, repository cloning, browser automation, credentials, and local services. <br>
Mitigation: Review the scripts and cloned repositories before execution, run in an isolated environment, avoid exposing GitHub tokens, and stop local services when automation is complete. <br>
Risk: Cron scheduling can repeatedly publish or reply without fresh human approval. <br>
Mitigation: Keep cron disabled until dry-run and live single-run behavior are verified, then schedule conservative intervals and monitor early executions. <br>


## Reference(s): <br>
- [Douyin Automation on ClawHub](https://clawhub.ai/hnc87/douyin-auto-hnc) <br>
- [Publishing Rules and Safety Filters](references/publishing.md) <br>
- [Comment Export and Auto Reply](references/comment-reply.md) <br>
- [Cover AI Generation](references/cover-ai.md) <br>
- [Configuration Reference](references/config-reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Code, Markdown, JSON, Guidance] <br>
**Output Format:** [Markdown instructions with inline shell commands, JSON configuration blocks, and command output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can run local scripts, start browser automation and local services, schedule cron jobs, publish content, reply to comments, and emit status or result files.] <br>

## Skill Version(s): <br>
1.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
