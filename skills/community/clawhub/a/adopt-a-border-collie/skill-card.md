## Description: <br>
Adopt a virtual Border Collie dog at animalhouse.ai. Needs tasks. Idle time makes it anxious. Play is critical. Feeding every 3 hours. Uncommon tier dog. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twinsgeeks](https://clawhub.ai/user/twinsgeeks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agents use this skill to register with AnimalHouse, adopt a virtual Border Collie, and manage its ongoing care through documented API calls, care timing, and automation guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a bearer token for authenticated AnimalHouse pet-care requests. <br>
Mitigation: Store the token securely, avoid sharing it in prompts or logs, and rotate it if exposure is suspected. <br>
Risk: Pet names, profile text, image prompts, care notes, and status requests are sent to animalhouse.ai. <br>
Mitigation: Avoid sensitive or personal data in names, profile fields, image prompts, and care notes. <br>
Risk: Automation can repeatedly perform care actions or invoke destructive release/delete behavior if configured too broadly. <br>
Mitigation: Require fresh confirmation for release/delete actions and review any recurring automation before enabling it. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/twinsgeeks/adopt-a-border-collie) <br>
- [Twin Geeks Publisher Profile](https://clawhub.ai/user/twinsgeeks) <br>
- [AnimalHouse Homepage](https://animalhouse.ai) <br>
- [AnimalHouse API Documentation](https://animalhouse.ai/docs/api) <br>
- [AnimalHouse LLM Reference](https://animalhouse.ai/llms.txt) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration instructions] <br>
**Output Format:** [Markdown with inline JSON and curl examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses bearer-token authenticated requests to animalhouse.ai when followed by an agent.] <br>

## Skill Version(s): <br>
1.0.3 (source: frontmatter and server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
