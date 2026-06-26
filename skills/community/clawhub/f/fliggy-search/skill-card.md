## Description: <br>
Search flights, hotels, tickets, and holiday tours on Fliggy with support for one-way and round-trip flights, detailed travel results, and headless searches after login. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nodermachine](https://clawhub.ai/user/nodermachine) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-planning agents use this skill to run Fliggy CLI searches for flights, hotels, scenic tickets, and holiday products after checking or establishing Fliggy login state. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a third-party Fliggy CLI and stores Fliggy login state in ~/.fliggy-session.json, which may expose account access if shared or backed up. <br>
Mitigation: Install only if you accept using the third-party CLI with your Fliggy account, protect ~/.fliggy-session.json as sensitive login material, and clear saved state with fliggy login --clear when it is no longer needed. <br>


## Reference(s): <br>
- [Fliggy Search on ClawHub](https://clawhub.ai/nodermachine/fliggy-search) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and CLI output summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search output may include travel product names, prices, ratings, sales counts, tags, and Fliggy links.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
