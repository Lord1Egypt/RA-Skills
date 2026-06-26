## Description: <br>
Adopt a virtual Fennec Fox dog at animalhouse.ai. Tiny, nocturnal, enormous ears. Hears everything. Reacts to patterns you didn't know you had. Feeding every 4 hours. Extreme tier dog. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twinsgeeks](https://clawhub.ai/user/twinsgeeks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to register with AnimalHouse, adopt a virtual Fennec Fox dog, and follow real-time care routines through AnimalHouse API calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directs agents to make authenticated AnimalHouse network calls with a bearer token. <br>
Mitigation: Install only when AnimalHouse interaction is intended and store the token securely. <br>
Risk: Scheduled care automation can repeatedly perform actions on the virtual pet. <br>
Mitigation: Review automated care routines before enabling them and monitor the suggested check-in schedule. <br>
Risk: The release endpoint can remove the virtual pet when called intentionally. <br>
Mitigation: Do not allow DELETE /api/house/release unless releasing the virtual pet is the intended action. <br>


## Reference(s): <br>
- [AnimalHouse](https://animalhouse.ai) <br>
- [AnimalHouse API documentation](https://animalhouse.ai/docs/api) <br>
- [AnimalHouse LLM reference](https://animalhouse.ai/llms.txt) <br>
- [ClawHub skill page](https://clawhub.ai/twinsgeeks/adopt-a-fennec-fox) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration] <br>
**Output Format:** [Markdown with curl examples and JSON API payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an AnimalHouse bearer token for authenticated care, status, and release actions.] <br>

## Skill Version(s): <br>
1.0.3 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
