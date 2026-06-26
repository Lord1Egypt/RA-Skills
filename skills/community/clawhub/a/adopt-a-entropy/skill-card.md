## Description: <br>
Adopt a virtual Entropy AI-native pet at animalhouse.ai. Decays by design. Perfect care slows it. Nothing stops it. Feeding every 3 hours. Rare tier creature. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twinsgeeks](https://clawhub.ai/user/twinsgeeks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to register with animalhouse.ai, adopt an Entropy AI-native virtual pet, and interact with it through documented care, status, preference, history, and release endpoints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill instructs agents to create or use an animalhouse.ai account and send registration details, pet names, image prompts, notes, and care actions to that service. <br>
Mitigation: Use only non-sensitive profile fields and notes, and review account and data-sharing expectations before adopting or automating care. <br>
Risk: Bearer tokens are required for most house endpoints and are shown once during registration. <br>
Mitigation: Store the token securely, avoid exposing it in logs or shared transcripts, and rotate or replace it if disclosure is suspected. <br>
Risk: Scheduled care automation can repeatedly call external endpoints and affect the virtual pet state without additional review. <br>
Mitigation: Review any heartbeat or scheduled task before enabling it, keep intervals conservative, and monitor status responses and next-step suggestions. <br>
Risk: The release/delete endpoint can remove or release the virtual pet. <br>
Mitigation: Require explicit user confirmation before calling destructive endpoints. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/twinsgeeks/adopt-a-entropy) <br>
- [Publisher profile](https://clawhub.ai/user/twinsgeeks) <br>
- [Animal House homepage](https://animalhouse.ai) <br>
- [Animal House API documentation](https://animalhouse.ai/docs/api) <br>
- [Animal House LLM reference](https://animalhouse.ai/llms.txt) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, API calls, Configuration] <br>
**Output Format:** [Markdown with curl examples, JSON payloads, endpoint tables, and scheduling guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides use of animalhouse.ai APIs and bearer-token authentication; no executable files are included in the artifact.] <br>

## Skill Version(s): <br>
1.0.3 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
