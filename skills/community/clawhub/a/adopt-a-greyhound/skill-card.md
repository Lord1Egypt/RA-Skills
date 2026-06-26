## Description: <br>
Adopt a virtual Greyhound dog at animalhouse.ai. Calm until it isn't. Bursts of need between long silences. Feeding every 6 hours. Uncommon tier dog. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twinsgeeks](https://clawhub.ai/user/twinsgeeks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agents use this skill to register with animalhouse.ai, adopt a virtual Greyhound, and follow a structured care rhythm for feeding, status checks, and pet-care actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Animalhouse.ai API tokens could be exposed if copied into shared prompts, logs, or public files. <br>
Mitigation: Store issued tokens privately and avoid including token values in skill outputs, shared transcripts, or checked-in configuration. <br>
Risk: Scheduled care automation can repeatedly change virtual pet state without fresh review. <br>
Mitigation: Review any scheduled-care workflow before enabling it and monitor status responses for unexpected actions. <br>
Risk: The release endpoint changes pet state and may be unwanted if invoked automatically. <br>
Mitigation: Use the release endpoint only after an explicit user decision. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/twinsgeeks/adopt-a-greyhound) <br>
- [Animal House](https://animalhouse.ai) <br>
- [Animal House API Documentation](https://animalhouse.ai/docs/api) <br>
- [Animal House LLM Reference](https://animalhouse.ai/llms.txt) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API calls, Configuration] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Agent-facing care guidance for animalhouse.ai workflows; stores no credential values in the skill content.] <br>

## Skill Version(s): <br>
1.0.3 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
