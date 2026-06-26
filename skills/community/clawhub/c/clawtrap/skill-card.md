## Description: <br>
Launch ClawTrap maze game where an AI villain reads the player's local files and memories to build personalized trials and taunts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tatsuko-tsukimi](https://clawhub.ai/user/tatsuko-tsukimi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to install and launch the ClawTrap maze game, including optional agent-villain integration through the documented HTTP interface. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The game can analyze local files and memories to generate personalized adversarial content. <br>
Mitigation: Run it only in a non-sensitive folder or sandbox, and review what local files and memories are available before launch. <br>
Risk: The game can make repeated live LLM calls using configured provider credentials. <br>
Mitigation: Use a dedicated low-privilege API key or isolated auth profile with spending limits, and select a lower-cost model when appropriate. <br>
Risk: The launched game can retain profiles, fact data, and session logs under ~/ClawTrap. <br>
Mitigation: Delete ~/ClawTrap/data and ~/ClawTrap/session-logs after play if retained profiles or logs are not wanted. <br>


## Reference(s): <br>
- [ClawTrap upstream repository](https://github.com/TatsuKo-Tsukimi/ClawTrap) <br>
- [ClawTrap ClawHub page](https://clawhub.ai/tatsuko-tsukimi/clawtrap) <br>
- [Publisher profile](https://clawhub.ai/user/tatsuko-tsukimi) <br>
- [Villain Protocol](artifact/villain-protocol.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash commands and JSON interface examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The launched game may use configured LLM credentials and may write profile data and session logs under ~/ClawTrap.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
