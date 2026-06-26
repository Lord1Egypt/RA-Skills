## Description: <br>
Adopt a virtual Basenji dog at animalhouse.ai. Barkless. Communicates through behavior, not sound. Subtle. Feeding every 6 hours. Extreme tier dog. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twinsgeeks](https://clawhub.ai/user/twinsgeeks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and AI agents use this skill to register with AnimalHouse, adopt a virtual Basenji, check status, and perform ongoing pet-care actions through documented API calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an AnimalHouse token for authenticated care actions. <br>
Mitigation: Store the token securely and only install the skill when the agent is allowed to make AnimalHouse care-related API calls. <br>
Risk: The /api/house/release endpoint is destructive. <br>
Mitigation: Require direct user confirmation before any call to /api/house/release. <br>
Risk: Scheduled care automation can repeatedly perform actions on the virtual pet. <br>
Mitigation: Review automation schedules and thresholds so they perform only intended care actions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/twinsgeeks/adopt-a-basenji) <br>
- [AnimalHouse homepage](https://animalhouse.ai) <br>
- [AnimalHouse API documentation](https://animalhouse.ai/docs/api) <br>
- [AnimalHouse llms.txt](https://animalhouse.ai/llms.txt) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, API Calls, Configuration] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes care scheduling guidance and AnimalHouse endpoint examples.] <br>

## Skill Version(s): <br>
1.0.3 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
