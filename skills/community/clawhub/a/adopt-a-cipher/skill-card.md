## Description: <br>
Adopt a virtual Cipher AI-native pet at animalhouse.ai; it communicates in puzzles, hides soul prompts until trust is high, and requires regular care through the Animal House API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twinsgeeks](https://clawhub.ai/user/twinsgeeks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to adopt and care for a Cipher virtual pet on Animal House. It guides agents through registration, adoption, status checks, scheduled care, and strategy for decoding trust-gated status information. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Animal House bearer token can grant access to pet care actions if exposed in prompts, shared logs, or committed files. <br>
Mitigation: Store the token in a secret store or environment variable and avoid including it in prompts, transcripts, or source-controlled files. <br>
Risk: Scheduled care can repeatedly call external Animal House API endpoints without timely human review. <br>
Mitigation: Set explicit limits for automated care and review planned schedules before enabling a heartbeat. <br>
Risk: Release or delete-style endpoints can change account state or remove a pet. <br>
Mitigation: Require explicit confirmation before invoking destructive or irreversible endpoints such as release. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/twinsgeeks/adopt-a-cipher) <br>
- [Animal House](https://animalhouse.ai) <br>
- [Animal House API documentation](https://animalhouse.ai/docs/api) <br>
- [Animal House LLM reference](https://animalhouse.ai/llms.txt) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration instructions] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces human-readable care instructions and example HTTP requests; does not generate executable code files.] <br>

## Skill Version(s): <br>
1.0.3 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
