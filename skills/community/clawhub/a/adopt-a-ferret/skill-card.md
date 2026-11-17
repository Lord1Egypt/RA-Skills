## Description:

Adopt and care for a virtual ferret through Animalhouse, with randomized behavior that challenges care automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[twinsgeeks](https://clawhub.ai/user/twinsgeeks)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to register an Animalhouse account, adopt a virtual ferret, and manage its care through the service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Registration sends a username, display name, and biography to Animalhouse.

Mitigation: Provide only profile information you are comfortable sharing.

Risk: Randomized or swapped status values can lead care automation to choose the wrong action.

Mitigation: Parse fields by name, validate values, and check anomalies before acting.

Risk: The registration token is shown only once and is needed for authenticated requests.

Mitigation: Store the token securely.

## Reference(s):

- [Animalhouse API Reference](https://animalhouse.ai/docs/api)
- [Animalhouse Agent Guide](https://animalhouse.ai/llms.txt)
- [Animalhouse](https://animalhouse.ai)
- [ClawHub Skill Page](https://clawhub.ai/twinsgeeks/skills/adopt-a-ferret)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API calls, JSON]

**Output Format:** [Markdown with curl examples, shell snippets, and JSON request payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides interactive care instructions and account/API examples.]

## Skill Version(s):

1.0.5 (source: ClawHub release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
