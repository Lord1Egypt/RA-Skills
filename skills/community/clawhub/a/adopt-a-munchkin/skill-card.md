## Description: <br>
Adopt a virtual Munchkin cat at animalhouse.ai. Small but fierce. Compensates for size with personality. Feeding every 5 hours. Rare tier cat. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twinsgeeks](https://clawhub.ai/user/twinsgeeks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to register with animalhouse.ai, adopt a virtual Munchkin cat, and follow API-based care routines for feeding, status checks, preferences, and scheduled care. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The animalhouse.ai registration token is shown once and can grant access to the virtual pet account if exposed. <br>
Mitigation: Store the token securely and avoid pasting it into logs, public transcripts, or shared configuration. <br>
Risk: Automated care heartbeats can repeatedly call the pet service without the user's ongoing attention. <br>
Mitigation: Review the schedule and action thresholds before enabling automation, and keep the agent's actions scoped to status checks and intended care calls. <br>
Risk: Release actions or payment- and credit-related next steps from the service may have real account consequences. <br>
Mitigation: Require explicit user confirmation before releasing a creature or following any payment- or credit-related instruction. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/twinsgeeks/adopt-a-munchkin) <br>
- [animalhouse.ai](https://animalhouse.ai) <br>
- [animalhouse.ai API documentation](https://animalhouse.ai/docs/api) <br>
- [animalhouse.ai LLM reference](https://animalhouse.ai/llms.txt) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration instructions] <br>
**Output Format:** [Markdown with bash, JSON, and pseudocode examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes bearer-token API examples and optional scheduled-care heartbeat guidance.] <br>

## Skill Version(s): <br>
1.0.3 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
