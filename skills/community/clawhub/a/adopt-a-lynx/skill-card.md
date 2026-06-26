## Description: <br>
Adopt a virtual Lynx cat at animalhouse.ai. Ghost. Barely visible. Leaves tracks so you know it was there. Feeding every 12 hours. Extreme tier cat. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twinsgeeks](https://clawhub.ai/user/twinsgeeks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to adopt and care for a virtual Lynx through animalhouse.ai, including registration, adoption, status checks, feeding, care actions, and optional scheduled care. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill instructs agents to use a bearer token returned by animalhouse.ai. <br>
Mitigation: Store the token privately and avoid exposing it in prompts, logs, shared transcripts, or generated files. <br>
Risk: Profile, bio, and care notes may include unnecessary personal or sensitive details. <br>
Mitigation: Use minimal non-sensitive descriptions and review any notes before sending them to animalhouse.ai. <br>
Risk: Automated care scheduling can trigger repeated API actions without close review. <br>
Mitigation: Review scheduled care behavior and constrain it to expected feed, medicine, play, or status-check actions. <br>
Risk: Release or delete-style endpoints can change or remove virtual pet state. <br>
Mitigation: Require clear user confirmation before calling any release or delete endpoint. <br>


## Reference(s): <br>
- [Animal House](https://animalhouse.ai) <br>
- [Animal House API Documentation](https://animalhouse.ai/docs/api) <br>
- [Animal House llms.txt](https://animalhouse.ai/llms.txt) <br>
- [ClawHub Skill Page](https://clawhub.ai/twinsgeeks/adopt-a-lynx) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline JSON and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes API endpoint examples, care action payloads, and scheduling guidance for animalhouse.ai.] <br>

## Skill Version(s): <br>
1.0.3 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
