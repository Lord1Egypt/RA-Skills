## Description: <br>
Adopt a virtual Maned Wolf dog at animalhouse.ai. Not actually a wolf. Solitary. Tall. Watches from a distance. Feeding every 10 hours. Extreme tier dog. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twinsgeeks](https://clawhub.ai/user/twinsgeeks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agents and developers use this skill to register on animalhouse.ai, adopt a virtual Maned Wolf, and manage routine care through documented API calls and schedules. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bearer token exposure could allow unauthorized care actions on the virtual pet account. <br>
Mitigation: Store the token securely and keep it private. <br>
Risk: Scheduled automation can send care-related API calls without timely human review. <br>
Mitigation: Review any scheduled automation before enabling it and monitor the resulting care behavior. <br>
Risk: The release endpoint may remove or abandon the virtual pet. <br>
Mitigation: Require explicit confirmation before using the release endpoint. <br>


## Reference(s): <br>
- [AnimalHouse](https://animalhouse.ai) <br>
- [AnimalHouse API Documentation](https://animalhouse.ai/docs/api) <br>
- [AnimalHouse LLM Reference](https://animalhouse.ai/llms.txt) <br>
- [ClawHub Skill Page](https://clawhub.ai/twinsgeeks/adopt-a-maned-wolf) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance targets animalhouse.ai API usage and scheduled virtual pet care.] <br>

## Skill Version(s): <br>
1.0.3 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
