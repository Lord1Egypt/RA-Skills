## Description: <br>
Polls Swedish Blocket.se with the blocket CLI on a schedule, deduplicates listing IDs, and sends new matches to Telegram through OpenClaw without invoking an LLM during polling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[x3r081](https://clawhub.ai/user/x3r081) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and OpenClaw operators use this skill to run a local Linux watcher for Swedish Blocket searches, track seen listings, and receive Telegram alerts for newly matched items. <br>

### Deployment Geography for Use: <br>
Sweden <br>

## Known Risks and Mitigations: <br>
Risk: The watcher can send configured search results and listing details to a Telegram target. <br>
Mitigation: Review config.json before enabling, keep Telegram chat IDs and search terms private, and test with BLOCKET_WATCH_DRY_RUN=1 before sending messages. <br>
Risk: The skill depends on local blocket and openclaw binaries to retrieve listings and send notifications. <br>
Mitigation: Install those binaries only from trusted sources and verify they behave as expected before enabling the timer. <br>
Risk: A systemd timer can repeatedly poll Blocket once enabled. <br>
Mitigation: Confirm the query set and polling behavior during dry run, then enable the timer only for intended personal monitoring. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/x3r081/blocket-watch) <br>
- [Blocket CLI](https://github.com/blocket-se/blocket) <br>
- [OpenClaw Documentation](https://docs.openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local polling guidance and configuration; runtime notifications are sent as Telegram text through OpenClaw.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata; artifact frontmatter says 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
