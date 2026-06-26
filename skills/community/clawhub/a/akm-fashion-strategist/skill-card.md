## Description: <br>
AKM implementation for wardrobe and outfit decision workflows. Models body context, scenes, wardrobe assets, and functional constraints before outputting styling decisions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sirsws](https://clawhub.ai/user/sirsws) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to build a reusable fashion profile and produce scene-aware outfit or purchase decisions grounded in body context, wardrobe assets, style preferences, and functional constraints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks for personal wardrobe, body-context, lifestyle, and purchase-preference details that a user may not want persisted or reused. <br>
Mitigation: Provide only details the user is comfortable sharing, and ask the agent to omit or delete the FashionProfile when persistence is not desired. <br>
Risk: The artifact documents an npx installation path in addition to the ClawHub listing. <br>
Mitigation: Install from the ClawHub listing when possible, or review the linked source before using the documented npx command. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/sirsws/akm-fashion-strategist) <br>
- [Publisher profile](https://clawhub.ai/user/sirsws) <br>
- [Fashion sample record](artifact/SAMPLE_RECORD.md) <br>
- [AKM fashion research paper](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6231466) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance, Configuration] <br>
**Output Format:** [Markdown with structured fields such as FashionProfile, SceneJudgment, OutfitRecommendation, GapAnalysis, PurchasePriority, and MissingInputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce partial decisions when required wardrobe, body-context, scene, or functional inputs are missing.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
