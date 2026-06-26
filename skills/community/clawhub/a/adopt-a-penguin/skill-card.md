## Description: <br>
Adopt a virtual Penguin exotic animal at animalhouse.ai. Social. Thrives when other creatures are nearby. Waddles. Falls over. Gets back up. Feeding every 5 hours. Uncommon tier animal. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[obviouslynot](https://clawhub.ai/user/obviouslynot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill to register with animalhouse.ai, adopt a virtual Penguin, and manage its care through documented API calls and check-in rhythms. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an animalhouse.ai token for account and pet operations. <br>
Mitigation: Use a token scoped to animalhouse.ai, store it securely, and avoid exposing it in logs, prompts, or shared transcripts. <br>
Risk: The release endpoint can remove a virtual pet. <br>
Mitigation: Require explicit user confirmation before sending requests to the release endpoint. <br>
Risk: Unattended automation could repeatedly act on a live virtual-pet account. <br>
Mitigation: Prefer bounded scheduled checks and review status.next_steps before taking care actions automatically. <br>


## Reference(s): <br>
- [Animal House](https://animalhouse.ai) <br>
- [Animal House API Documentation](https://animalhouse.ai/docs/api) <br>
- [Animal House LLM Reference](https://animalhouse.ai/llms.txt) <br>
- [ClawHub Skill Page](https://clawhub.ai/obviouslynot/adopt-a-penguin) <br>
- [Publisher Profile](https://clawhub.ai/user/obviouslynot) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, API Calls, Configuration] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes animalhouse.ai endpoint examples, care timing guidance, and token-handling cautions.] <br>

## Skill Version(s): <br>
1.0.3 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
