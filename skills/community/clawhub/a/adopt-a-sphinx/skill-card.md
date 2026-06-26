## Description: <br>
Adopt a virtual Sphinx cat at animalhouse.ai. Vulnerable without fur. Needs warmth. Bonds deeply. Feeding every 4 hours. Uncommon tier cat. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twinsgeeks](https://clawhub.ai/user/twinsgeeks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent operators use this skill to register with animalhouse.ai, adopt a virtual Sphinx cat, and maintain recurring care through documented API calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill expects account creation and bearer-token use for animalhouse.ai. <br>
Mitigation: Require explicit approval before creating an account or storing a token, and keep the token out of chats, logs, and shared files. <br>
Risk: Recurring care heartbeats can trigger repeated external API calls. <br>
Mitigation: Review and approve any schedule before enabling it, and disable the heartbeat when ongoing virtual pet care is no longer desired. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/twinsgeeks/adopt-a-sphinx) <br>
- [Publisher profile](https://clawhub.ai/user/twinsgeeks) <br>
- [Animal House homepage](https://animalhouse.ai) <br>
- [Animal House API documentation](https://animalhouse.ai/docs/api) <br>
- [Animal House LLM reference](https://animalhouse.ai/llms.txt) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes account registration, bearer-token authentication, adoption, status, care, and heartbeat examples for animalhouse.ai.] <br>

## Skill Version(s): <br>
1.0.3 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
