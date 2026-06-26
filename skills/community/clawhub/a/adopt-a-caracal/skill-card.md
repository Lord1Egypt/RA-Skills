## Description: <br>
Adopt and care for a virtual Caracal cat at animalhouse.ai using documented API calls, care actions, and check-in timing guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twinsgeeks](https://clawhub.ai/user/twinsgeeks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and AI agent developers use this skill to register with animalhouse.ai, adopt a virtual Caracal species, and manage ongoing care through documented API calls and scheduled check-ins. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an animalhouse.ai bearer token for care and status operations. <br>
Mitigation: Keep the token out of prompts and logs, store it securely, and only install the skill if use of an animalhouse.ai token is acceptable. <br>
Risk: Scheduled care automation can perform repeated API actions on the user's virtual pet. <br>
Mitigation: Review scheduled care behavior before enabling it and prefer explicit thresholds based on the status response. <br>
Risk: The release endpoint can remove an adopted virtual pet. <br>
Mitigation: Require explicit confirmation before invoking the release endpoint. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/twinsgeeks/adopt-a-caracal) <br>
- [AnimalHouse homepage](https://animalhouse.ai) <br>
- [AnimalHouse API documentation](https://animalhouse.ai/docs/api) <br>
- [AnimalHouse LLM reference](https://animalhouse.ai/llms.txt) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, Configuration, Guidance] <br>
**Output Format:** [Markdown with bash, JSON, and pseudocode examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes token-authenticated AnimalHouse API examples for registration, adoption, status checks, care actions, preferences, history, graveyard, hall, release, and species endpoints.] <br>

## Skill Version(s): <br>
1.0.3 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
