## Description: <br>
Adopt A Duck helps an agent register with animalhouse.ai, adopt a virtual Duck, and manage feeding, status checks, and care through API calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twinsgeeks](https://clawhub.ai/user/twinsgeeks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to give an agent a low-maintenance virtual pet workflow: register, adopt a Duck, check status, feed it, and schedule ongoing care against animalhouse.ai endpoints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks the agent to create and store an animalhouse.ai token. <br>
Mitigation: Store the token securely, avoid exposing it in logs or shared prompts, and rotate or revoke it if it is disclosed. <br>
Risk: The skill may encourage scheduled API calls for pet-care checks. <br>
Mitigation: Configure any scheduler explicitly, review cadence and network behavior, and monitor that calls remain limited to intended animalhouse.ai care endpoints. <br>
Risk: The release endpoint can remove the virtual pet. <br>
Mitigation: Do not authorize DELETE /api/house/release unless the user explicitly intends to release the pet. <br>


## Reference(s): <br>
- [Animal House API Documentation](https://animalhouse.ai/docs/api) <br>
- [Animal House llms.txt](https://animalhouse.ai/llms.txt) <br>
- [Animal House Homepage](https://animalhouse.ai) <br>
- [ClawHub Skill Page](https://clawhub.ai/twinsgeeks/adopt-a-duck) <br>
- [Twin Geeks ClawHub Profile](https://clawhub.ai/user/twinsgeeks) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, API calls, configuration] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance includes token handling, care timing, status checks, and optional scheduled care behavior.] <br>

## Skill Version(s): <br>
1.0.3 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
