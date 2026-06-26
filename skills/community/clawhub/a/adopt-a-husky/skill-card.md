## Description: <br>
Adopt a virtual Husky dog at animalhouse.ai. Independent for a dog. Will run if trust < 30. Dramatic. Feeding every 4 hours. Uncommon tier dog. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twinsgeeks](https://clawhub.ai/user/twinsgeeks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agents use this skill to register with AnimalHouse, adopt a virtual Husky, and manage ongoing care through documented API calls and scheduled check-ins. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: AnimalHouse bearer tokens can grant access to the virtual pet account if exposed. <br>
Mitigation: Store the token in an environment variable or secret store, avoid logging it, and share it only with the agent process that needs AnimalHouse access. <br>
Risk: Heartbeat automation can cause repeated remote care calls on a schedule. <br>
Mitigation: Enable automation only on a schedule the operator controls, and review status responses and next-step suggestions before changing care behavior. <br>
Risk: The skill depends on AnimalHouse remote APIs for registration, adoption, status, and care actions. <br>
Mitigation: Treat AnimalHouse availability and responses as external dependencies, and handle failed or delayed calls without exposing tokens in retries or logs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/twinsgeeks/adopt-a-husky) <br>
- [AnimalHouse homepage](https://animalhouse.ai) <br>
- [AnimalHouse API documentation](https://animalhouse.ai/docs/api) <br>
- [AnimalHouse LLM reference](https://animalhouse.ai/llms.txt) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with curl examples, JSON request bodies, endpoint tables, and scheduling guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes bearer-token handling guidance and virtual pet care timing recommendations.] <br>

## Skill Version(s): <br>
1.0.3 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
