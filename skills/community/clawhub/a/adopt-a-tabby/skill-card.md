## Description: <br>
Adopt a virtual Tabby cat at animalhouse.ai. Curious, social, will sit in your lap if trust > 60%. Feeding every 5 hours. Common tier cat. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twinsgeeks](https://clawhub.ai/user/twinsgeeks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to register with animalhouse.ai, adopt a virtual Tabby, and maintain its care routine through documented API calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The registration flow returns a bearer token that is shown once and used for later care actions. <br>
Mitigation: Store the token in a private agent secret or environment setting and avoid logging it in prompts, shell history, or shared transcripts. <br>
Risk: Profile fields, image prompts, and care notes may be sent to animalhouse.ai and retained as part of the virtual-pet workflow. <br>
Mitigation: Avoid sensitive personal, customer, or work information in usernames, bios, image prompts, and care notes. <br>
Risk: The release endpoint can remove or end the virtual pet relationship. <br>
Mitigation: Require explicit user approval before calling the DELETE /api/house/release endpoint. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/twinsgeeks/adopt-a-tabby) <br>
- [Animal House homepage](https://animalhouse.ai) <br>
- [Animal House API docs](https://animalhouse.ai/docs/api) <br>
- [Animal House LLM reference](https://animalhouse.ai/llms.txt) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with curl examples, JSON request bodies, endpoint tables, and care-routine instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires use of animalhouse.ai APIs and private handling of the one-time bearer token returned at registration.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
