## Description: <br>
Maintain a persistent personal wardrobe, answer wardrobe questions, and recommend outfits from existing clothes with natural-language responses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[investigator13th](https://clawhub.ai/user/investigator13th) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to maintain a local wardrobe record, ask wardrobe questions, and receive outfit recommendations grounded in clothing they already own, with optional weather and preference context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill keeps wardrobe items, fit, style, color, occasion preferences, notes, and optional weather configuration locally over time. <br>
Mitigation: Review or clear the user JSON files when that history should not be retained, and avoid adding weather configuration if location privacy is a concern. <br>
Risk: Wardrobe recommendations can be incomplete or misleading if the local wardrobe record is sparse, stale, or ambiguous. <br>
Mitigation: Review recommendations against actual wardrobe contents and update or clarify wardrobe facts before relying on state-changing recommendations. <br>
Risk: The skill can make persistent local wardrobe or preference changes when the user asks to add, update, or remember information. <br>
Mitigation: Confirm destructive or ambiguous changes before applying them, and keep temporary preferences session-only unless long-term intent is clear. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/investigator13th/awesome-closet-stylist) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Guidance] <br>
**Output Format:** [Natural-language Markdown responses with local JSON file updates when wardrobe or preference state changes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read and update local wardrobe, preference, and weather configuration JSON files.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
