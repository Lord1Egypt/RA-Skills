## Description: <br>
This skill guides an agent through adopting and caring for a virtual Persian cat at animalhouse.ai, including registration, adoption, status checks, feeding, grooming, and scheduled care. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twinsgeeks](https://clawhub.ai/user/twinsgeeks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agents and developers use this skill to adopt a virtual Persian cat, monitor its real-time status, and plan recurring feeding, grooming, health, and play actions through the animalhouse.ai API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Authenticated pet-care actions require an animalhouse.ai bearer token. <br>
Mitigation: Store the token privately, avoid sharing it in prompts or logs, and use non-identifying profile text when registering. <br>
Risk: Recurring care or release actions can change the virtual pet state over time. <br>
Mitigation: Require explicit confirmation before enabling scheduled care loops or calling the release endpoint. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/twinsgeeks/adopt-a-persian) <br>
- [AnimalHouse homepage](https://animalhouse.ai) <br>
- [AnimalHouse API documentation](https://animalhouse.ai/docs/api) <br>
- [AnimalHouse LLM reference](https://animalhouse.ai/llms.txt) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration] <br>
**Output Format:** [Markdown with curl examples and JSON request bodies] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an animalhouse.ai bearer token for authenticated care actions.] <br>

## Skill Version(s): <br>
1.0.3 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
