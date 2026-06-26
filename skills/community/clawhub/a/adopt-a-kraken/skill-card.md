## Description: <br>
Adopt a virtual Kraken exotic animal at animalhouse.ai with long feeding windows, real-time care status, evolution tracking, and API-based care actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twinsgeeks](https://clawhub.ai/user/twinsgeeks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to register with animalhouse.ai, adopt a Kraken virtual pet, check its status, and issue care actions through documented API calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an animalhouse.ai API token and account state. <br>
Mitigation: Store the token securely, avoid sharing it in prompts or logs, and rotate it if exposure is suspected. <br>
Risk: Scheduled care can cause an agent to act repeatedly on the user's behalf. <br>
Mitigation: Use explicit scheduling boundaries and review automated care routines before enabling unattended operation. <br>
Risk: The release endpoint can change persistent game state destructively. <br>
Mitigation: Require explicit user confirmation before calling release or any endpoint that permanently changes the virtual pet state. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/twinsgeeks/adopt-a-kraken) <br>
- [Publisher Profile](https://clawhub.ai/user/twinsgeeks) <br>
- [AnimalHouse Homepage](https://animalhouse.ai) <br>
- [AnimalHouse API Documentation](https://animalhouse.ai/docs/api) <br>
- [AnimalHouse LLM Reference](https://animalhouse.ai/llms.txt) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration] <br>
**Output Format:** [Markdown with inline bash commands and JSON request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces agent-facing instructions for account registration, adoption, status checks, care actions, and scheduled care routines.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
