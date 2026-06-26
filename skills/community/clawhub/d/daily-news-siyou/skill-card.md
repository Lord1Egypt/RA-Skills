## Description: <br>
Fetches current news for user-defined categories and creates scheduled Chinese text or voice broadcasts through Feishu. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Anightmare2](https://clawhub.ai/user/Anightmare2) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to configure personalized news categories, generate daily news summaries, and post text or voice broadcasts to a Feishu chat on demand or by cron schedule. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Feishu, NoizAI, and Tavily credentials are required for normal operation and could be exposed through shared shell profiles, logs, or unattended cron jobs. <br>
Mitigation: Use least-privilege Feishu credentials, keep API keys out of shared profiles and logs, and review cron logging before enabling scheduled broadcasts. <br>
Risk: Unattended scheduled broadcasts can post recurring messages to the wrong chat or before the output format has been verified. <br>
Mitigation: Test with text-only output or a test chat before enabling cron, then add recurring jobs only when the target chat and content are confirmed. <br>
Risk: Voice mode depends on a separate Feishu voice skill and may fall back to text if that dependency is unavailable. <br>
Mitigation: Review and test the separate feishu-voice-skill before relying on voice broadcasts. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Anightmare2/daily-news-siyou) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [README.md](artifact/README.md) <br>
- [Cron Examples](artifact/examples/crontab.txt) <br>
- [Tavily Search API Endpoint](https://api.tavily.com/search) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash commands and generated Chinese news broadcast text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can post text or voice output to Feishu and can be scheduled with cron.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and artifact clawhub.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
