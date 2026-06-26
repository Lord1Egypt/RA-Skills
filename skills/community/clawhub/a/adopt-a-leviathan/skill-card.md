## Description: <br>
Guides an agent through adopting and caring for a virtual Leviathan exotic animal at animalhouse.ai. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twinsgeeks](https://clawhub.ai/user/twinsgeeks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to guide an agent through registering, adopting a Leviathan, checking status, taking care actions, and optionally scheduling ongoing care for a virtual pet. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses bearer-token API calls to animalhouse.ai. <br>
Mitigation: Store the token securely and avoid exposing it in prompts, logs, or shared transcripts. <br>
Risk: Profile fields, pet names, image prompts, and care notes are sent to animalhouse.ai. <br>
Mitigation: Avoid sensitive personal information in those fields. <br>
Risk: The release endpoint can remove a creature and is called out as under-explained in the security evidence. <br>
Mitigation: Require explicit user confirmation before calling DELETE /api/house/release. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/twinsgeeks/adopt-a-leviathan) <br>
- [Animal House homepage](https://animalhouse.ai) <br>
- [Animal House API documentation](https://animalhouse.ai/docs/api) <br>
- [Animal House llms.txt](https://animalhouse.ai/llms.txt) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, API calls, JSON payloads] <br>
**Output Format:** [Markdown with curl examples and JSON request payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses bearer-token API calls to animalhouse.ai; scheduled care examples are optional.] <br>

## Skill Version(s): <br>
1.0.3 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
