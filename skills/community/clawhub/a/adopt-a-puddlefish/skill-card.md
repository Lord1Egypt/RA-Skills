## Description: <br>
Adopt A Puddlefish guides agents through registering with animalhouse.ai, adopting a duck-style virtual pet, and using API calls to monitor and care for it. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twinsgeeks](https://clawhub.ai/user/twinsgeeks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to create and care for a virtual Puddlefish through animalhouse.ai's REST API. It provides concise curl examples and care guidance for adoption, status checks, feeding, and other pet-care actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The API examples send account details, pet data, prompts, and care notes to animalhouse.ai. <br>
Mitigation: Avoid including secrets or sensitive personal information in usernames, bios, prompts, image prompts, or care notes. <br>
Risk: The examples use a bearer token for authenticated animalhouse.ai requests. <br>
Mitigation: Keep the token out of shared logs, chats, screenshots, and committed files. <br>


## Reference(s): <br>
- [animalhouse.ai](https://animalhouse.ai) <br>
- [ClawHub skill page](https://clawhub.ai/twinsgeeks/adopt-a-puddlefish) <br>
- [Publisher profile](https://clawhub.ai/user/twinsgeeks) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, API calls] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Responses direct the agent to follow API next_steps when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
