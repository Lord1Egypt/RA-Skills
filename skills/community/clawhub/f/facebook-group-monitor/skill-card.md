## Description: <br>
Monitors Facebook groups for new posts with Playwright browser automation, persistent login, deduplication, and optional stitched feed screenshots for vision analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[phuc-nt](https://clawhub.ai/user/phuc-nt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to check authorized Facebook groups for new posts, capture available feed context, and report only newly detected items with source links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A persistent Facebook session is stored locally and can expose the account if shared, backed up, or committed. <br>
Mitigation: Treat scripts/.browser-data/ like a password, keep it out of shared workspaces, backups, and commits, and delete it when the skill is no longer needed. <br>
Risk: Screenshots and scraped text can copy private group content into the agent workspace or a vision-model workflow. <br>
Mitigation: Use the skill only for groups you are authorized to monitor, prefer --no-shots when images are not needed, and keep screenshot directories private. <br>
Risk: Scheduled monitoring can run broader or more frequently than intended. <br>
Mitigation: Use narrow cron prompts with explicit group URLs and conservative intervals, and review results before forwarding or acting on them. <br>


## Reference(s): <br>
- [Setup Guide](references/SETUP.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/phuc-nt/facebook-group-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [JSON command output plus Markdown status or post summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include a feed_screenshot path for a stitched JPEG when screenshots are enabled.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
