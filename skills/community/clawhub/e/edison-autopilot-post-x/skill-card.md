## Description: <br>
Automatically generates and posts persona-matched tweets to X using GPT-5.1, with repetition checks, content filters, and optional Telegram alerts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[EdisonChenAI](https://clawhub.ai/user/EdisonChenAI) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and individual X account operators use this skill to generate, preview, schedule, and publish persona-matched posts with configurable voice, topics, banned phrases, and optional notifications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can autonomously publish AI-generated posts from a real X account. <br>
Mitigation: Start with --dry-run, use a test or low-risk account, and remove the cron entry when autonomous posting is no longer wanted. <br>
Risk: The script requires credentials for OpenAI, X, and optionally Telegram. <br>
Mitigation: Use dedicated least-privilege API keys and keep credentials in environment variables rather than editing them into files. <br>
Risk: Generated or error content may be shared with external services, including optional Telegram notifications. <br>
Mitigation: Leave Telegram disabled unless needed and keep SCAN_DIR unset unless it contains non-sensitive material. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/EdisonChenAI/edison-autopilot-post-x) <br>
- [X Developer Platform](https://developer.x.com) <br>
- [OpenAI Platform](https://platform.openai.com) <br>
- [Tweepy](https://github.com/tweepy/tweepy) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and Python-generated post text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can run in dry-run mode for preview or post directly to X when credentials and scheduling are configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
