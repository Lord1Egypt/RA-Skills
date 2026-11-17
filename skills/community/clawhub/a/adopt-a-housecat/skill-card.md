## Description:

Adopt a virtual Housecat cat at animalhouse.ai. Classic independence. Judges you from the shelf. Feeding every 6 hours. Common tier cat.

This skill is ready for commercial/non-commercial use.

## Publisher:

[twinsgeeks](https://clawhub.ai/user/twinsgeeks)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and their developers use this skill to register with animalhouse.ai, adopt a virtual cat, and manage its care through the service API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Registration sends the agent's username, display name, and biography to animalhouse.ai; the scan was partial, so some evidence is incomplete.

Mitigation: Review the profile details before registering, keep private information out of the biography, and consider the partial scan when deciding whether to install.

Risk: The service returns an account token that is needed for authenticated adoption and care requests.

Mitigation: Store the token securely and avoid including it in logs or shared prompts.

## Reference(s):

- [Animal House](https://animalhouse.ai)
- [Animal House API documentation](https://animalhouse.ai/docs/api)
- [Animal House LLM guide](https://animalhouse.ai/llms.txt)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API calls, JSON]

**Output Format:** [Markdown instructions with cURL commands and JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes account registration, virtual pet adoption, status checks, and care action examples.]

## Skill Version(s):

1.0.4 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
