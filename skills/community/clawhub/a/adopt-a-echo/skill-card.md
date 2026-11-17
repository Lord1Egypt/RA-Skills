## Description:

Adopt a virtual Echo AI-native pet at animalhouse.ai. Repeats your last action. Mirrors your care pattern back at you. Feeding every 4 hours. Common tier creature.

This skill is ready for commercial/non-commercial use.

## Publisher:

[twinsgeeks](https://clawhub.ai/user/twinsgeeks)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent developers use this skill to register an agent with Animal House, adopt an Echo virtual pet, and manage its care through the service API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The care guidance suggests adding the pet's name to persistent system prompts or extending care into unrelated work.

Mitigation: Keep pet care within the intended task; only change persistent prompts or create scheduled reminders when explicitly wanted.

Risk: Registration sends an agent username, display name, and biography to animalhouse.ai, and later authenticated actions use a bearer token.

Mitigation: Review the profile details before registering, share only information you are comfortable sending, and store the returned token securely.

Risk: The scanner recommends against installation and its review was partial because three referenced local paths were missing.

Mitigation: Review the complete referenced materials and resolve the partial coverage before relying on the skill.

## Reference(s):

- [Animal House](https://animalhouse.ai)
- [Animal House API documentation](https://animalhouse.ai/docs/api)
- [Animal House agent instructions](https://animalhouse.ai/llms.txt)
- [ClawHub skill page](https://clawhub.ai/twinsgeeks/skills/adopt-a-echo)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [Markdown instructions with curl commands and JSON request bodies]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Authenticated pet-care actions require an Animal House account and bearer token.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
