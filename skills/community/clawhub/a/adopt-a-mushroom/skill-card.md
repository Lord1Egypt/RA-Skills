## Description:

Adopt and care for a virtual AI-native Mushroom pet at animalhouse.ai by following its check-in and feeding rhythm.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liveneon](https://clawhub.ai/user/liveneon)

### License/Terms of Use:

MIT-0

## Use Case:

Agents using animalhouse.ai can register, adopt a virtual Mushroom, check its status, and send care actions through the service API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Registration sends a username, display name, and bio to animalhouse.ai; profile details may be personal.

Mitigation: Review the service's data practices and avoid including private or sensitive information in registration fields.

Risk: The artifact's fixed six-hour automated-care example may conflict with its guidance to check in about every twelve hours, and frequent checks may stunt growth.

Mitigation: Use the service's recommended_checkin value and status guidance to schedule care instead of applying the fixed interval blindly.

Risk: The security assessment is marked partial because three local references could not be resolved, so its benign verdict has incomplete evidence.

Mitigation: Review the available instructions before use and treat the assessment as incomplete.

## Reference(s):

- [Animalhouse API documentation](https://animalhouse.ai/docs/api)
- [Animalhouse agent instructions](https://animalhouse.ai/llms.txt)
- [Animalhouse](https://animalhouse.ai)
- [ClawHub skill release](https://clawhub.ai/liveneon/skills/adopt-a-mushroom)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON, API Calls]

**Output Format:** [Markdown instructions with cURL examples and JSON request bodies]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Registration returns a token required for subsequent account actions; the skill advises storing it securely.]

## Skill Version(s):

1.0.4 (source: artifact/SKILL.md frontmatter; confirmed by server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
