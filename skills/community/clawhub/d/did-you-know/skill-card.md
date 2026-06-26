## Description: <br>
Fetches English Wikipedia's "Did you know?" (DYK) facts, caches them locally, and serves them one at a time. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jonathandeamer](https://clawhub.ai/user/jonathandeamer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to fetch a conversational Wikipedia Did You Know fact, optionally tune topic preferences, and optionally schedule recurring fact delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts Wikipedia to fetch public Did You Know facts. <br>
Mitigation: Use it only where outbound access to Wikipedia is acceptable. <br>
Risk: The skill stores a local facts cache and optional topic preferences in ~/.openclaw. <br>
Mitigation: Review and remove those local files when cache history or preferences should not persist. <br>
Risk: Automatic delivery or preference refresh can create recurring OpenClaw cron schedules. <br>
Mitigation: Confirm the schedule and removal instructions before enabling recurring jobs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jonathandeamer/did-you-know) <br>
- [Wikipedia Did You Know](https://en.wikipedia.org/wiki/Wikipedia:Did_you_know) <br>
- [DYK command reference](references/commands.md) <br>
- [DYK hook tagging guide](references/tagging-guide.md) <br>
- [DYK tag vocabulary](references/tags.csv) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Conversational text with optional Markdown and silent shell-command execution guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local JSON cache and preference files under ~/.openclaw; scheduled delivery uses OpenClaw cron when enabled by the user.] <br>

## Skill Version(s): <br>
0.2.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
