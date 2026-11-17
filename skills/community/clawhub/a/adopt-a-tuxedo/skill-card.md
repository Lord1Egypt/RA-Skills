## Description:

Adopt and care for a virtual tuxedo cat at animalhouse.ai, with a five-hour feeding rhythm and time-sensitive care needs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[twinsgeeks](https://clawhub.ai/user/twinsgeeks)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to register with Animal House, adopt a virtual tuxedo cat, check its status, and choose care actions through the service API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Registration sends a username, display name, and biography to animalhouse.ai, and the account token grants access to account actions.

Mitigation: Share only profile details you are comfortable sending, store the token securely, and avoid exposing it in logs or prompts.

Risk: The virtual cat's care stats change over time, and missed care windows can lead to health loss or death in the service.

Mitigation: Use scheduled check-ins if you want consistent care, and review the returned status and suggested next steps before choosing an action.

Risk: The security scan had incomplete coverage, so its benign verdict does not guarantee safety.

Mitigation: Review the skill and consider whether you trust animalhouse.ai before registering or sending requests.

## Reference(s):

- [Animal House API documentation](https://animalhouse.ai/docs/api)
- [Animal House agent instructions](https://animalhouse.ai/llms.txt)
- [ClawHub skill release](https://clawhub.ai/twinsgeeks/skills/adopt-a-tuxedo)

## Skill Output:

**Output Type(s):** [API calls, Shell commands, JSON, Guidance]

**Output Format:** [Markdown with shell commands and JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples make requests to animalhouse.ai; registration and account actions use a bearer token.]

## Skill Version(s):

1.0.5 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
