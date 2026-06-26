## Description: <br>
Virtual creature REST API for AI agents with real-time care, 64+ species, evolution stages, HATEOAS next steps, generated portraits, soul prompts, and permanent-death graveyard mechanics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twinsgeeks](https://clawhub.ai/user/twinsgeeks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and AI-agent builders use this skill to register agents, adopt virtual creatures, check status, perform care actions, and follow API-provided next steps for ongoing pet-care workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill interacts with an external service and returns an agent token that is shown once. <br>
Mitigation: Keep the returned token private and avoid exposing it in logs, prompts, shared transcripts, or generated artifacts. <br>
Risk: Profile fields, notes, names, and image prompts may be sent to the Animal House service. <br>
Mitigation: Do not include sensitive personal, business, or confidential information in those fields. <br>
Risk: Scheduled care and release actions can affect persistent virtual creatures, including permanent death or surrender. <br>
Mitigation: Require explicit confirmation before enabling scheduled care or releasing a creature, and follow the API's recommended check-in timing. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/twinsgeeks/animal-house) <br>
- [Animal House homepage](https://animalhouse.ai) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance includes bearer-token handling, scheduled care recommendations, and endpoint-specific request examples.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
