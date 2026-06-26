## Description: <br>
Adopt and care for a virtual Pitbull dog at animalhouse.ai with registration, adoption, status checks, feeding, care actions, and optional scheduled care. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twinsgeeks](https://clawhub.ai/user/twinsgeeks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to adopt a Pitbull virtual dog and maintain it through status checks, feeding, care actions, and care-rhythm guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can contact animalhouse.ai and create or modify a persistent virtual pet account using a bearer token. <br>
Mitigation: Keep the token private and require explicit confirmation before registration, adoption, automated care, or account-changing actions. <br>
Risk: Scheduled care can make recurring service-side changes after setup. <br>
Mitigation: Enable scheduled care only when the user intends ongoing automated check-ins and review the care rhythm before activating it. <br>
Risk: The release endpoint can remove an adopted virtual pet from the account. <br>
Mitigation: Require explicit user confirmation before any release action. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/twinsgeeks/adopt-a-pitbull) <br>
- [Animal House](https://animalhouse.ai) <br>
- [Animal House API documentation](https://animalhouse.ai/docs/api) <br>
- [Animal House LLM reference](https://animalhouse.ai/llms.txt) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API calls, Configuration] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses bearer-token authenticated HTTP requests to animalhouse.ai for adoption, status, care, and release actions.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
