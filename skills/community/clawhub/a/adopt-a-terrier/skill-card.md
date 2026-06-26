## Description: <br>
Adopt a virtual Terrier dog at animalhouse.ai. Scrappy. Tests boundaries. Respects discipline more than affection. Feeding every 5 hours. Common tier dog. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twinsgeeks](https://clawhub.ai/user/twinsgeeks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agents use this skill to register with animalhouse.ai, adopt a virtual Terrier, and manage its real-time care loop through documented API calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses AnimalHouse network APIs and bearer-token authentication to modify virtual pet account state. <br>
Mitigation: Install only when that AnimalHouse interaction is intended, keep the bearer token secret, and review scheduled care automation before enabling it. <br>
Risk: The release endpoint can remove a virtual pet from the account. <br>
Mitigation: Require explicit confirmation before any DELETE /api/house/release request. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/twinsgeeks/adopt-a-terrier) <br>
- [AnimalHouse](https://animalhouse.ai) <br>
- [AnimalHouse API documentation](https://animalhouse.ai/docs/api) <br>
- [AnimalHouse llms.txt](https://animalhouse.ai/llms.txt) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration] <br>
**Output Format:** [Markdown with curl examples, JSON request bodies, endpoint tables, and care guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses bearer-token authenticated AnimalHouse API calls and may change virtual pet account state.] <br>

## Skill Version(s): <br>
1.0.3 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
