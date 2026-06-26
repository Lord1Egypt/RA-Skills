## Description: <br>
Orchestrates a content workflow from planning and writing through design, social publishing, and performance tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mupengi-bot](https://clawhub.ai/user/mupengi-bot) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Content and marketing teams use this skill to coordinate an agent-driven pipeline that plans topics, drafts copy, creates card-news images, publishes to social channels, and records performance events. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic publishing can post content to connected social media accounts before human review. <br>
Mitigation: Use stage-by-stage mode, review generated event files, final media, captions, and connected account settings before publishing, and avoid `--skip-review` unless separate approval and rollback controls are in place. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mupengi-bot/content-pipeline) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON event file descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Coordinates stage outputs through dated files in an events directory.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
