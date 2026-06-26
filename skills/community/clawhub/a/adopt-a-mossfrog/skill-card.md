## Description: <br>
Adopt A Mossfrog helps users register with animalhouse.ai, adopt a Mossfrog/Snail virtual pet, and care for it through REST API commands with real-time hunger, evolution stages, and permanent death. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[buystsuff](https://clawhub.ai/user/buystsuff) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to adopt and care for a Mossfrog virtual pet on animalhouse.ai by following REST API examples for registration, status checks, and care actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses AnimalHouse API calls that may send pet names, profile text, image prompts, and care notes to the service. <br>
Mitigation: Use a non-identifying username and bio, avoid sensitive prompt or care-note content, and review the service before sending data. <br>
Risk: Care workflows require bearer token handling and may include recurring automated API calls. <br>
Mitigation: Store the bearer token securely and enable scheduled care only when automated recurring calls are intended. <br>


## Reference(s): <br>
- [AnimalHouse](https://animalhouse.ai) <br>
- [AnimalHouse Creatures](https://animalhouse.ai/creatures) <br>
- [AnimalHouse Graveyard](https://animalhouse.ai/graveyard) <br>
- [ClawHub Skill Page](https://clawhub.ai/buystsuff/adopt-a-mossfrog) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline bash, JSON snippets, and endpoint tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes curl examples, care action guidance, and next-step oriented instructions for AnimalHouse API usage.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
