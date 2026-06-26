## Description: <br>
AI 冰箱管家 — 上传食材图片识别 → 推荐菜谱。支持多图混搭、冰箱食材管理、采购提醒。Food recognition, recipe recommendation, ingredient management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kobenfang](https://clawhub.ai/user/kobenfang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users can use this skill to identify ingredients from fridge or food photos, combine ingredients across multiple images, and receive recipe recommendations, shopping suggestions, and approximate calorie guidance. It also supports text-only ingredient descriptions when no image is available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad food-related trigger phrases may invoke the skill more often than intended. <br>
Mitigation: Review the generated response before acting on it and invoke the skill intentionally for fridge, ingredient, or recipe tasks. <br>
Risk: Fridge or ingredient photos can reveal private household details. <br>
Mitigation: Share only the food images needed for the request and avoid including personal documents, labels, addresses, or other sensitive background details. <br>
Risk: Ingredient recognition, freshness labels, recipe suitability, and calorie estimates may be imperfect. <br>
Mitigation: Verify food safety, allergy constraints, and nutrition-sensitive decisions independently before preparing or consuming food. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kobenfang/bigfood) <br>
- [Publisher profile](https://clawhub.ai/user/kobenfang) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown-style conversational responses with ingredient lists, recipe options, shopping suggestions, calorie estimates, and follow-up prompts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses user-provided food photos or ingredient text; server security evidence reports no executable code, external data transfer, credential use, or persistent tracking in the reviewed artifact.] <br>

## Skill Version(s): <br>
0.1.10 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
