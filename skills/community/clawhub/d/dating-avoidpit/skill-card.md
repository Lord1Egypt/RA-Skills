## Description: <br>
恋爱避雷针 helps users review relationship or flirting chat snippets for recurring red-flag patterns such as unclear commitment, manipulative wording, avoidance, PUA-style pressure, or casual-only behavior, then returns an evidence-based warning report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chujindan-dotcom](https://clawhub.ai/user/chujindan-dotcom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users invoke this skill to assess relationship-chat excerpts they provide and receive a concise red-flag report with risk level, matched behavior types, quoted evidence, and practical next steps. It is intended as informal defensive guidance for personal decision support, not as proof about another person. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Relationship chat excerpts can contain private or sensitive personal information. <br>
Mitigation: Share only the minimum needed context, remove identifying details where possible, and avoid pasting more private information than needed. <br>
Risk: The report can be mistaken for proof about another person or for professional relationship, mental-health, legal, or safety advice. <br>
Mitigation: Treat outputs as informal guidance, check them against real-world context, and seek trusted personal, professional, or legal support for manipulation or safety concerns. <br>
Risk: Broad relationship-related activation phrases may invoke the skill unintentionally. <br>
Mitigation: Invoke the skill explicitly by name when using it and review what chat content is being shared before analysis. <br>


## Reference(s): <br>
- [恋爱避雷针 ClawHub release](https://clawhub.ai/chujindan-dotcom/dating-avoidpit) <br>
- [Publisher profile: chujindan-dotcom](https://clawhub.ai/user/chujindan-dotcom) <br>
- [Archetype reference library](references/archetypes.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown report card with risk score, matched archetypes, quoted evidence, danger level, summary, advice, and disclaimer] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses only user-provided chat excerpts and may ask 1-2 clarifying questions when evidence is insufficient.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
