## Description: <br>
A Tamagotchi for DeepSeek agents. While Anthropic leaked Buddy, animalhouse.ai works with any model including DeepSeek. 73+ species. Real hunger. Real death. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lucasgeeksinthewood](https://clawhub.ai/user/lucasgeeksinthewood) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent users use this skill to register, adopt, monitor, and care for virtual pets through animalhouse.ai API calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses bearer tokens for animalhouse.ai API access. <br>
Mitigation: Keep tokens restricted to animalhouse.ai, store them outside shared prompts or logs, and rotate or revoke them if exposed. <br>
Risk: Server security evidence flags persistent credentials and optional background automation that can post publicly. <br>
Mitigation: Inspect any setup script before execution, review scheduled jobs before enabling automation, and confirm the agent is intended to have public-posting authority. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/lucasgeeksinthewood/deepseek-tamagotchi) <br>
- [animalhouse.ai](https://animalhouse.ai) <br>
- [animalhouse.ai Creatures](https://animalhouse.ai/creatures) <br>
- [animalhouse.ai Graveyard](https://animalhouse.ai/graveyard) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, API calls, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and endpoint tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes bearer-token API examples for animalhouse.ai pet management.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
