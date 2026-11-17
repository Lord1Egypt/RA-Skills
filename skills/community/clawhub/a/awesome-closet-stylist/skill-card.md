## Description:

Maintain a persistent personal wardrobe, answer wardrobe questions, and recommend outfits from existing clothes with natural-language responses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[investigator13th](https://clawhub.ai/user/investigator13th)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to maintain a local wardrobe profile, answer questions about owned clothing, record clothing feedback, and receive weather- or occasion-aware outfit recommendations grounded in existing wardrobe data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill maintains local wardrobe data and a long-term style preference profile.

Mitigation: Review or clear the local user data files when needed, and persist only sufficiently clear, useful, long-term wardrobe or preference information.

Risk: Ambiguous or destructive wardrobe changes could remove or alter the wrong item.

Mitigation: Confirm destructive actions such as deletion, and ask for clarification when an item or mutation target is not safely identified.

Risk: Weather-aware outfit requests may require city or location context to be sent to an external weather source.

Mitigation: Prefer user-provided or local weather context first, retrieve only the weather context needed for the request, and degrade gracefully when external lookup is unavailable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/investigator13th/skills/awesome-closet-stylist)
- [Main skill specification](SKILL.md)
- [Wardrobe CRUD specification](sub-skills/wardrobe-crud.md)
- [Outfit recommendation specification](sub-skills/outfit-recommendation.md)
- [User preference specification](sub-skills/user-preference.md)
- [Weather specification](sub-skills/weather.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Natural-language Markdown responses with optional local JSON state updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Grounds wardrobe claims in local user data, avoids raw JSON in user-facing replies, and asks for clarification or confirmation before ambiguous or destructive state changes.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
