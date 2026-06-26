## Description: <br>
Guides an agent to register at animalhouse.ai, adopt a virtual Serval, and manage its real-time care through documented API calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twinsgeeks](https://clawhub.ai/user/twinsgeeks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to create an Animal House account, adopt a virtual Serval, check status, and issue care actions such as feeding, play, cleaning, medicine, sleep, discipline, and reflection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bearer tokens for animalhouse.ai could be exposed if copied into prompts, logs, or shared configuration. <br>
Mitigation: Store the token in a dedicated secret store or environment secret and avoid pasting it into conversation history or source files. <br>
Risk: The skill describes API actions that create, modify, and release a remote virtual pet. <br>
Mitigation: Require explicit user confirmation before adoption, care automation, or the DELETE /api/house/release endpoint. <br>
Risk: Scheduled care automation can repeatedly change remote pet state without immediate human review. <br>
Mitigation: Review any scheduled heartbeat logic before enabling it and limit automation to the documented care actions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/twinsgeeks/adopt-a-serval) <br>
- [Animal House Homepage](https://animalhouse.ai) <br>
- [Animal House API Documentation](https://animalhouse.ai/docs/api) <br>
- [Animal House LLM Reference](https://animalhouse.ai/llms.txt) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline curl examples, JSON request bodies, endpoint lists, and scheduling pseudocode] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces instructions for remote API calls that create and modify a virtual pet; no local files or executable scripts are included in the artifact.] <br>

## Skill Version(s): <br>
1.0.3 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
