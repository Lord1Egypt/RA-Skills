## Description: <br>
Adopt A Twigling guides an agent through adopting and caring for a low-maintenance animalhouse.ai Cactus/Twigling virtual pet with REST API commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[buystsuff](https://clawhub.ai/user/buystsuff) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to adopt, check, and care for a virtual Twigling/Cactus pet through animalhouse.ai API calls. It is intended for guided pet-care interactions, including feeding, status checks, and optional heartbeat-style care routines. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends profile, pet, image prompt, notes, care-action data, and a bearer token to animalhouse.ai. <br>
Mitigation: Use non-sensitive profile and notes data, install only if comfortable sharing that information with animalhouse.ai, and treat the bearer token like a password. <br>
Risk: Heartbeat or next_steps usage can lead to repeated network calls to the external pet-care service. <br>
Mitigation: Allow repeated calls only when they stay within the intended pet-care workflow and review care actions before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/buystsuff/adopt-a-twigling) <br>
- [animalhouse.ai homepage](https://animalhouse.ai) <br>
- [Animal House creatures](https://animalhouse.ai/creatures) <br>
- [Animal House graveyard](https://animalhouse.ai/graveyard) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API calls, Configuration] <br>
**Output Format:** [Markdown with curl command examples and JSON request bodies] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes bearer-token setup guidance and optional heartbeat-style care logic.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
