## Description: <br>
输入视频主题、关键词和产品信息，生成面向 FridayParts 维修科普视频的 5 分钟双语分镜脚本，并内置技术准确性和安全表述规范。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhuxirui677](https://clawhub.ai/user/zhuxirui677) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing and operations teams use this skill to turn a repair-video topic, required keywords, and product information into a structured YouTube script for North American heavy-equipment audiences. Technical or operations staff should still review repair details, product fit, and safety guidance before publishing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated repair scripts could contain inaccurate technical explanations, unsafe steps, or product-fit assumptions if published without review. <br>
Mitigation: Have qualified operations or technical staff verify repair logic, safety warnings, and product/model details before filming or publishing. <br>
Risk: The prompt is specialized for FridayParts heavy-equipment repair content and may steer generic YouTube script requests toward that brand and domain. <br>
Mitigation: Confirm the repair-video context before use, or narrow invocation triggers when deploying alongside general script-writing skills. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhuxirui677/skills/fp-youtube-script) <br>
- [README](artifact/README.md) <br>
- [GetClawHub import guide](artifact/docs/如何导入GetClawHub.md) <br>
- [Example water pump and thermostat script](artifact/examples/example_water_pump_thermostat.md) <br>
- [Manual validation checklist](artifact/reference/人工验证checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown table-style script with bilingual dialogue, image-generation prompts, and production notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs follow HOOK, BODY, SUMMARY, and ENDING sections and include human-review checkpoints for technical accuracy and safety.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
