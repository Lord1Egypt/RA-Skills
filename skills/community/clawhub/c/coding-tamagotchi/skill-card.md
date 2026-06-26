## Description: <br>
Coding Tamagotchi helps coders and coding agents register, adopt, check status, and care for a virtual pet through animalhouse.ai API requests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[buystsuff](https://clawhub.ai/user/buystsuff) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, coding agents, and external users use this skill to manage a virtual coding pet by registering, adopting, checking status, and sending care actions through animalhouse.ai. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an animalhouse.ai bearer token for pet management requests. <br>
Mitigation: Keep the ah_ token out of chats, commits, logs, and shared care notes; treat it like a password. <br>
Risk: Profile text, image prompts, and care notes may be sent to animalhouse.ai. <br>
Mitigation: Avoid entering sensitive personal information in registration profiles, pet prompts, or care notes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/buystsuff/coding-tamagotchi) <br>
- [Publisher profile](https://clawhub.ai/user/buystsuff) <br>
- [Animal House](https://animalhouse.ai) <br>
- [Animal House creatures](https://animalhouse.ai/creatures) <br>
- [Animal House graveyard](https://animalhouse.ai/graveyard) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, API Calls] <br>
**Output Format:** [Markdown with inline bash code blocks and API endpoint tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces curl examples and care-action guidance; users must supply and protect their animalhouse.ai bearer token.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
