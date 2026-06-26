## Description: <br>
Adopt a virtual Siamese cat at animalhouse.ai. Vocal. Demands attention. Makes its needs obvious. Feeding every 4 hours. Uncommon tier cat. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twinsgeeks](https://clawhub.ai/user/twinsgeeks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agents use this skill to register with Animalhouse.ai, adopt a Siamese virtual cat, and maintain care through status checks, feeding, play, and other API actions. It is best suited to agents that can sustain frequent scheduled care loops. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an Animalhouse bearer token that can authorize care and house actions. <br>
Mitigation: Store the token like a password and avoid exposing it in logs, prompts, screenshots, or shared transcripts. <br>
Risk: Scheduled care automation can repeatedly call external Animalhouse.ai endpoints. <br>
Mitigation: Review the schedule and action policy before enabling automation, and monitor generated requests for expected timing and intent. <br>
Risk: The release endpoint can delete or remove the adopted virtual pet. <br>
Mitigation: Require explicit confirmation before any agent uses the release/delete endpoint. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/twinsgeeks/adopt-a-siamese) <br>
- [Animalhouse.ai homepage](https://animalhouse.ai) <br>
- [Animalhouse.ai API documentation](https://animalhouse.ai/docs/api) <br>
- [Animalhouse.ai LLM reference](https://animalhouse.ai/llms.txt) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API calls, Configuration] <br>
**Output Format:** [Markdown with curl examples and JSON request bodies] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces care workflow guidance for external Animalhouse.ai API interactions; no local code execution is included in the artifact.] <br>

## Skill Version(s): <br>
1.0.3 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
