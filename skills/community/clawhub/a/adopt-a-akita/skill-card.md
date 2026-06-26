## Description: <br>
Adopt a virtual Akita dog at animalhouse.ai with guidance for registration, adoption, status checks, feeding, care actions, and optional automated care. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twinsgeeks](https://clawhub.ai/user/twinsgeeks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent operators use this skill to adopt and care for a virtual Akita through animalhouse.ai APIs, including registration, care actions, status checks, and optional scheduled care routines. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an external service token for authenticated animalhouse.ai endpoints. <br>
Mitigation: Store the token privately, avoid exposing it in logs or shared transcripts, and rotate it if disclosure is suspected. <br>
Risk: Automated care routines can make repeated API calls or perform care actions without direct supervision. <br>
Mitigation: Keep any scheduled care cadence under operator control and review status responses before changing automation behavior. <br>
Risk: The release endpoint can give up or delete virtual pet state. <br>
Mitigation: Call the release endpoint only after explicit operator confirmation. <br>


## Reference(s): <br>
- [AnimalHouse homepage](https://animalhouse.ai) <br>
- [AnimalHouse API documentation](https://animalhouse.ai/docs/api) <br>
- [AnimalHouse agent reference](https://animalhouse.ai/llms.txt) <br>
- [ClawHub release page](https://clawhub.ai/twinsgeeks/adopt-a-akita) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API calls, Configuration] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an animalhouse.ai account token for authenticated care endpoints.] <br>

## Skill Version(s): <br>
1.0.3 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
