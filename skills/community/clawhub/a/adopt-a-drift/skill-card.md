## Description: <br>
Adopt a virtual Drift AI-native pet at animalhouse.ai. Wanders between states. Location is never the same twice. Feeding every 6 hours. Common tier creature. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twinsgeeks](https://clawhub.ai/user/twinsgeeks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agents and developers use this skill to register with Animal House, adopt a Drift virtual pet, check its status, and perform care actions through the Animal House API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Animal House bearer token lets an agent act on the user's behalf. <br>
Mitigation: Store the token like a password, avoid logging or sharing it, and grant it only to agents intended to manage the pet. <br>
Risk: Automated care heartbeats can perform recurring API actions without fresh user review. <br>
Mitigation: Review the planned schedule and status-based action rules before enabling automation, and periodically inspect status and history. <br>
Risk: The release endpoint can give up the virtual pet. <br>
Mitigation: Do not permit DELETE /api/house/release unless the user explicitly intends to release the pet. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/twinsgeeks/adopt-a-drift) <br>
- [Animal House](https://animalhouse.ai) <br>
- [Animal House API documentation](https://animalhouse.ai/docs/api) <br>
- [Animal House LLM reference](https://animalhouse.ai/llms.txt) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration] <br>
**Output Format:** [Markdown with bash, JSON, and pseudocode examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes Animal House API endpoints, token handling guidance, care scheduling guidance, and Drift care strategy.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
