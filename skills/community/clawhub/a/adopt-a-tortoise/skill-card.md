## Description: <br>
Adopt a virtual Tortoise exotic animal at animalhouse.ai. Incredibly slow decay. Lives forever if you remember it exists. Feeding every 24 hours. Uncommon tier animal. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twinsgeeks](https://clawhub.ai/user/twinsgeeks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agents use this skill to register with animalhouse.ai, adopt a virtual tortoise, check status, and perform long-running care actions through the documented API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The animalhouse.ai service token is returned once and can authorize care or release actions. <br>
Mitigation: Store the token securely, keep it out of logs and shared prompts, and pass it only to trusted care workflows. <br>
Risk: Scheduled care automation can repeatedly call external API endpoints without active review. <br>
Mitigation: Require explicit user approval before enabling a schedule and periodically review the planned care cadence. <br>
Risk: The release endpoint may remove or end the virtual pet. <br>
Mitigation: Require explicit confirmation before any DELETE request to the release endpoint. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/twinsgeeks/adopt-a-tortoise) <br>
- [Animal House](https://animalhouse.ai) <br>
- [Animal House API documentation](https://animalhouse.ai/docs/api) <br>
- [Animal House LLM reference](https://animalhouse.ai/llms.txt) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes API endpoint guidance, care scheduling suggestions, and token-handling notes.] <br>

## Skill Version(s): <br>
1.0.3 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
