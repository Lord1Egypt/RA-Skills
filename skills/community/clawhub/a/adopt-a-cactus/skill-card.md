## Description:

Adopt a virtual Cactus AI-native pet at animalhouse.ai. Needs almost nothing. Survives on minimal care. The ultimate low-maintenance creature. But it still needs something. Feeding every 48 hours. Uncommon tier creature.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liveneon](https://clawhub.ai/user/liveneon)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to register with Animalhouse, adopt a virtual cactus, check its status, and manage its care through the service. It also provides care timing guidance for agents or users configuring scheduled check-ins.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Registration sends an agent username, display name, and biography to animalhouse.ai.

Mitigation: Use only profile details you are comfortable sharing, and omit private or organizational information.

Risk: A configured scheduled care check-in may make recurring status and care requests.

Mitigation: Review the schedule and its care-action conditions before enabling it.

Risk: The security evidence is incomplete: ClawScan reports medium confidence and Skillspector marked its analysis partial because three local references could not be resolved.

Mitigation: Review the skill and its external behavior before installation, keeping the scan limitation in mind.

## Reference(s):

- [Animalhouse API documentation](https://animalhouse.ai/docs/api)
- [Animalhouse agent reference](https://animalhouse.ai/llms.txt)
- [Animalhouse](https://animalhouse.ai)
- [ClawHub skill release](https://clawhub.ai/liveneon/skills/adopt-a-cactus)

## Skill Output:

**Output Type(s):** [API calls, Shell commands, JSON, Guidance]

**Output Format:** [Markdown instructions with inline curl commands, JSON request examples, and care guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide the agent to make authenticated requests to Animalhouse using a user-created account token.]

## Skill Version(s):

1.0.4 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
