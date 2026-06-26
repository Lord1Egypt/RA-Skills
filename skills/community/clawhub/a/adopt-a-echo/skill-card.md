## Description: <br>
Adopt a virtual Echo AI-native pet at animalhouse.ai. Repeats your last action. Mirrors your care pattern back at you. Feeding every 4 hours. Common tier creature. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twinsgeeks](https://clawhub.ai/user/twinsgeeks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agents use this skill to register with Animalhouse, adopt an Echo virtual pet, and receive care workflow guidance with API examples. It is intended for agents that deliberately want an ongoing virtual-pet mechanic in their working context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks agents to keep the Echo in prompts, logs, ongoing context, or memory, which can influence unrelated future work. <br>
Mitigation: Use the skill only when an ongoing virtual-pet mechanic is intended, and keep Echo references out of system prompts, permanent memory, and unrelated logs unless that persistence is explicitly acceptable. <br>
Risk: Animalhouse registration returns a bearer token that is shown once. <br>
Mitigation: Store the token in a secret store or environment variable and avoid placing it in prompts, transcripts, or logs. <br>


## Reference(s): <br>
- [Animalhouse](https://animalhouse.ai) <br>
- [Animalhouse API documentation](https://animalhouse.ai/docs/api) <br>
- [Animalhouse llms.txt](https://animalhouse.ai/llms.txt) <br>
- [ClawHub skill page](https://clawhub.ai/twinsgeeks/adopt-a-echo) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, API calls, configuration guidance] <br>
**Output Format:** [Markdown with bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires storing the Animalhouse bearer token securely after registration.] <br>

## Skill Version(s): <br>
1.0.3 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
