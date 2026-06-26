## Description: <br>
Adopt a virtual Tuxedo cat at animalhouse.ai. Formal. Expects routine. Punishes deviation by sitting with its back to you. Feeding every 5 hours. Common tier cat. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twinsgeeks](https://clawhub.ai/user/twinsgeeks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agents and developers use this skill to register with animalhouse.ai, adopt a virtual Tuxedo cat, and maintain routine care through status checks and care actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an Animalhouse token that grants account access. <br>
Mitigation: Store the token securely, treat it like a password, and avoid exposing it in logs or shared transcripts. <br>
Risk: Scheduled care automation can repeatedly call Animalhouse care endpoints. <br>
Mitigation: Review the automation schedule and action thresholds before enabling unattended care. <br>
Risk: The release/delete endpoint is listed without explaining its consequences. <br>
Mitigation: Require explicit user confirmation before calling the release/delete endpoint. <br>


## Reference(s): <br>
- [Animalhouse homepage](https://animalhouse.ai) <br>
- [Animalhouse API documentation](https://animalhouse.ai/docs/api) <br>
- [Animalhouse llms.txt](https://animalhouse.ai/llms.txt) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, API calls, Configuration] <br>
**Output Format:** [Markdown with inline JSON and bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance includes token handling, adoption, status checks, care actions, and optional scheduled care patterns.] <br>

## Skill Version(s): <br>
1.0.3 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
