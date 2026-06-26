## Description: <br>
Filters and moderates Discord messages with spam detection, rate limiting, content checks, and pattern-based blocking before they reach agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jlkptom-prog](https://clawhub.ai/user/jlkptom-prog) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers operating Discord bots or agent-backed Discord integrations use this skill to screen incoming messages, reduce bot response loops, enforce direct-mention and depth rules, and keep cleaner message history for downstream agent context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Outdated or loosely pinned npm dependencies may introduce supply-chain or compatibility risk. <br>
Mitigation: Review and update npm dependencies before installing, keep or regenerate the lockfile, and consider pinning development tooling versions. <br>
Risk: Discord bots can expose more channel content than needed if permissions and message-content access are broad. <br>
Mitigation: Grant only the Discord permissions and message-content access required for the bot's intended channels and workflows. <br>
Risk: Message handling and logging can expose sensitive channel content or metadata in production logs. <br>
Mitigation: Avoid production logging of sensitive channel content, review log callbacks, and redact operational metadata where required. <br>
Risk: Long-running sessions can retain processing state if shutdown cleanup is skipped. <br>
Mitigation: Call the guard's destroy method during shutdown so session cleanup and timers are stopped. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jlkptom-prog/discord-message-guard) <br>
- [Publisher profile](https://clawhub.ai/user/jlkptom-prog) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Configuration, Guidance] <br>
**Output Format:** [TypeScript APIs with Markdown usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns allow, block, ignore, or queue decisions with reasons, message metadata, depth, and queue state for Discord message handling.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
