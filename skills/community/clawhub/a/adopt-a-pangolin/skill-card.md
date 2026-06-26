## Description: <br>
Adopt a virtual Pangolin exotic animal at animalhouse.ai. Armored. Shy. Rolls into a ball when trust < 40. Feeding every 12 hours. Rare tier animal. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twinsgeeks](https://clawhub.ai/user/twinsgeeks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to register with AnimalHouse, adopt a virtual Pangolin, and guide an agent through status checks, care actions, and optional scheduled care. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Authenticated AnimalHouse calls require a bearer token that is shown once during registration. <br>
Mitigation: Store the token securely, avoid logging it, and only provide it to agents that need scoped AnimalHouse adoption or care access. <br>
Risk: The skill includes state-changing endpoints for adoption, care, species updates, and release. <br>
Mitigation: Require explicit user confirmation before release or other unintended state-changing calls, and review scheduled care logic before enabling automation. <br>


## Reference(s): <br>
- [AnimalHouse](https://animalhouse.ai) <br>
- [AnimalHouse API documentation](https://animalhouse.ai/docs/api) <br>
- [AnimalHouse LLM reference](https://animalhouse.ai/llms.txt) <br>
- [ClawHub skill page](https://clawhub.ai/twinsgeeks/adopt-a-pangolin) <br>
- [Publisher profile](https://clawhub.ai/user/twinsgeeks) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, API calls, configuration] <br>
**Output Format:** [Markdown guidance with inline curl commands, JSON payloads, endpoint tables, and scheduled-care pseudocode] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an AnimalHouse bearer token for authenticated adoption and care endpoints.] <br>

## Skill Version(s): <br>
1.0.3 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
