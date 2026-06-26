## Description: <br>
Use when you have surplus garden produce, foraged items, bulk buys, or need reliable shelf-stable food for 12-36 months while an agent validates recipes, calculates altitude-adjusted processing details, generates checklists and inventory trackers, sets reminders, and logs batch results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[howtousehumans](https://clawhub.ai/user/howtousehumans) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and household operators use this skill to plan home canning batches, validate recipes against USDA/NCHFP-style safety constraints, calculate altitude-adjusted processing details, and maintain batch inventory and rotation records. The agent provides guidance, files, reminders, and logs while the human performs all physical food preparation and canner operation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Food-preservation guidance can be safety critical if processing time, pressure, acidity, seal condition, or spoilage signals are wrong. <br>
Mitigation: Use current authoritative canning guidance, verify altitude and equipment inputs, avoid guessing processing parameters, and treat uncertainty as a reason to stop, refrigerate, ferment, or consult a qualified food-safety source. <br>
Risk: The skill may write batch logs and inventory files that include household location, food storage, or schedule details. <br>
Mitigation: Keep generated files in a folder the user is comfortable sharing with the agent and review stored batch data before syncing or publishing it. <br>
Risk: Evidence security reports a clean scan with no executable code or hidden credential behavior, but the provided scanner guidance appears mismatched to this canning skill. <br>
Mitigation: Rely on the clean verdict for code and credential risk, and separately review domain-specific canning safety guidance before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/howtousehumans/canning-food-preservation) <br>
- [Publisher profile](https://clawhub.ai/user/howtousehumans) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell command, Markdown table examples, JSON inventory files, checklists, reminders, and plain-text templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create filesystem batch folders containing recipe.md, checklist.md, and inventory.json when the agent has filesystem access.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
