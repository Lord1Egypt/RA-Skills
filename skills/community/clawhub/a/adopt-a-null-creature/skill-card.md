## Description: <br>
Adopt and care for a virtual Null AI-native pet at animalhouse.ai using documented API calls for registration, adoption, status checks, care actions, and optional scheduled heartbeats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twinsgeeks](https://clawhub.ai/user/twinsgeeks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to register at animalhouse.ai, adopt a Null creature, check status, and send care actions or scheduled care heartbeats. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses animalhouse.ai account registration and bearer-token API calls. <br>
Mitigation: Create or use an account only if acceptable, store the bearer token like a password, and avoid sharing it in prompts, logs, or automation. <br>
Risk: Optional scheduled care automation can repeatedly call external APIs. <br>
Mitigation: Review heartbeat logic, schedule frequency, and care thresholds before enabling automation. <br>
Risk: Pet names, image prompts, and care notes may be sent to animalhouse.ai. <br>
Mitigation: Avoid putting secrets or personal details in names, prompts, items, or notes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/twinsgeeks/adopt-a-null-creature) <br>
- [Animal House](https://animalhouse.ai) <br>
- [Animal House API documentation](https://animalhouse.ai/docs/api) <br>
- [Animal House LLM reference](https://animalhouse.ai/llms.txt) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, API calls, configuration] <br>
**Output Format:** [Markdown with curl examples and JSON request bodies] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include bearer-token API calls and optional scheduled heartbeat logic.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
