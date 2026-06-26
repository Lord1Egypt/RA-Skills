## Description: <br>
Adopt a virtual Retriever dog at animalhouse.ai, with care guidance for feeding, status checks, and virtual-pet routines. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twinsgeeks](https://clawhub.ai/user/twinsgeeks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agents and developers use this skill to adopt and care for a virtual Retriever through animalhouse.ai API calls. It provides practical care instructions, endpoint examples, and scheduling guidance for maintaining the pet over time. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bearer tokens are used for authenticated animalhouse.ai care actions. <br>
Mitigation: Store the token privately and avoid exposing it in logs, prompts, or shared transcripts. <br>
Risk: Automated recurring care may perform ongoing API actions without repeated review. <br>
Mitigation: Enable recurring schedules intentionally and periodically review status, timing, and care actions. <br>
Risk: The release endpoint can remove the virtual pet from the account. <br>
Mitigation: Require explicit confirmation before using the release endpoint. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/twinsgeeks/adopt-a-retriever) <br>
- [animalhouse.ai](https://animalhouse.ai) <br>
- [animalhouse.ai API documentation](https://animalhouse.ai/docs/api) <br>
- [animalhouse.ai LLM reference](https://animalhouse.ai/llms.txt) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with curl commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes bearer-token API examples; tokens should be stored privately.] <br>

## Skill Version(s): <br>
1.0.3 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
