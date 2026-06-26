## Description: <br>
Helps an agent guide users through adopting, checking, and caring for a Cloudferret virtual pet on animalhouse.ai using documented REST API actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lucasgeeksinthewood](https://clawhub.ai/user/lucasgeeksinthewood) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to adopt a Cloudferret, call animalhouse.ai care endpoints, and understand available care actions, status checks, history, graveyard, and hall views. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends profile fields, pet names, care actions, and notes to animalhouse.ai. <br>
Mitigation: Use non-sensitive profile text and do not include secrets or unrelated personal data in care notes. <br>
Risk: Heartbeat-style automation can make repeated authenticated API calls. <br>
Mitigation: Supervise automation and keep care loops bounded so repeated calls remain intentional. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/lucasgeeksinthewood/adopt-a-cloudferret) <br>
- [Animal House](https://animalhouse.ai) <br>
- [Animal House Creatures](https://animalhouse.ai/creatures) <br>
- [Animal House Graveyard](https://animalhouse.ai/graveyard) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration] <br>
**Output Format:** [Markdown with inline bash, JSON, and endpoint examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes next-step guidance for authenticated animalhouse.ai API interactions.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
