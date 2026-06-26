## Description: <br>
Cloudferret guides an agent through registering, adopting, checking, and caring for an animalhouse.ai ferret-style virtual pet using documented API calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leegitw](https://clawhub.ai/user/leegitw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers can use this skill to create and care for a Cloudferret virtual pet on animalhouse.ai, including registration, adoption, status checks, and care actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends chosen profile and pet-care data to animalhouse.ai. <br>
Mitigation: Use non-sensitive profile text and care notes. <br>
Risk: The registration flow returns an ah_ token that controls later pet-care actions. <br>
Mitigation: Keep the token private and avoid exposing it in shared logs, prompts, or transcripts. <br>


## Reference(s): <br>
- [Cloudferret ClawHub page](https://clawhub.ai/leegitw/cloudferret) <br>
- [Animal House AI](https://animalhouse.ai) <br>
- [Animal House Creatures](https://animalhouse.ai/creatures) <br>
- [Animal House Graveyard](https://animalhouse.ai/graveyard) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with bash curl examples, endpoint tables, and care guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes reminders to keep the returned ah_ token private and to use non-sensitive profile and care text.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
