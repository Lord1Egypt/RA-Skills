## Description: <br>
谛听.skill is an installable digest skill for OpenClaw or Claude Code that helps users configure personalized ScoutX briefings with local preferences and minimal setup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yangchao228](https://clawhub.ai/user/yangchao228) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to set up recurring or on-demand AI information digests from ScoutX curated media, X/Twitter, and podcast feeds. They configure frequency, language, topics, and delivery through conversation instead of maintaining feed URLs or raw filters. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches digest content from bundled public feed endpoints. <br>
Mitigation: Confirm the packaged feed endpoints are trusted before installation; reserve configure-service and feed URL overrides for operators. <br>
Risk: Scheduled OpenClaw delivery can send digests to the wrong target if the schedule or channel is misconfigured. <br>
Mitigation: Use preview or install-openclaw-cron dry run first, inspect the delivery target, and run --apply only after the schedule and destination are correct. <br>
Risk: The skill stores schedule, delivery, topic, and language preferences locally. <br>
Mitigation: Treat the local ~/.follow_scoutx profile as user preference data and avoid adding API tokens or credentials, which are not required for normal use. <br>
Risk: A digest may be incomplete if one selected feed cannot be reached. <br>
Mitigation: Check JSON preview or delivery status, failed_source_types, and errors before treating a partial run as complete. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yangchao228/follow-scoutx) <br>
- [Publisher profile](https://clawhub.ai/user/yangchao228) <br>
- [Bundled ScoutX public feed](https://input.reai.group/v1/public/feed) <br>
- [Bundled ScoutX metadata endpoint](https://input.reai.group/v1/public/meta) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown digests, JSON payloads, and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores local user preferences and can split long delivery output into sequential channel messages.] <br>

## Skill Version(s): <br>
0.2.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
