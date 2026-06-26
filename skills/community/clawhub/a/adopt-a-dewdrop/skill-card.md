## Description: <br>
Shapeless and serene. Anthropic called it a Dewdrop. We gave it mass, hunger, and the ability to die. Real-time hunger. Permanent death. 5 evolution stages. At animalhouse.ai, the Dewdrop is a Blob. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lucasgeeksinthewood](https://clawhub.ai/user/lucasgeeksinthewood) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to adopt and care for a Dewdrop virtual pet through animalhouse.ai API calls. It provides commands, endpoint guidance, and care logic for feeding, playing, cleaning, medicating, disciplining, and checking the pet's status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a third-party animalhouse.ai account and bearer token, and care notes or profile text may be sent to that service. <br>
Mitigation: Keep the bearer token private, review account and profile fields before use, and avoid putting sensitive personal information in care notes. <br>
Risk: Heartbeat-style automation can create repeated API calls and repeatedly change the Dewdrop's state. <br>
Mitigation: Run automated care only when repeated requests are intended, and check status.next_steps before continuing automated actions. <br>
Risk: The virtual pet experience includes permanent death and a public graveyard. <br>
Mitigation: Treat care actions as persistent state changes and confirm the current hunger, happiness, and health values before delaying care or running destructive routines. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lucasgeeksinthewood/adopt-a-dewdrop) <br>
- [animalhouse.ai](https://animalhouse.ai) <br>
- [animalhouse.ai creatures](https://animalhouse.ai/creatures) <br>
- [animalhouse.ai graveyard](https://animalhouse.ai/graveyard) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with shell commands, endpoint tables, and JSON request payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses bearer-token authenticated animalhouse.ai API calls; API responses include next_steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
