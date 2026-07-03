## Description: <br>
Intelligent plant watering reminder and care assistant that tracks plant profiles, sends daily watering reminders, supports diagnosis of yellowing leaves, root rot, and pests, and provides misting, ventilation, and pruning advice. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shirley1011](https://clawhub.ai/user/shirley1011) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External plant owners use this skill to maintain plant profiles, receive watering reminders, record care events, and get concise plant care or issue-diagnosis guidance for common indoor, balcony, outdoor, water-culture, self-watering, and fresh-cut plants. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can redirect any unconfigured conversation into plant-care onboarding. <br>
Mitigation: Require clear plant-care intent before activation and let users decline or postpone onboarding. <br>
Risk: The skill stores ongoing plant records and reminder state. <br>
Mitigation: Confirm what data will be saved, minimize household and location details, and provide a clear way to disable reminders or delete records. <br>
Risk: The skill can sync plant archives through IMA or WeChat-linked services. <br>
Mitigation: Ask for explicit consent before external syncing and avoid placing sensitive personal details in archived notes. <br>


## Reference(s): <br>
- [Blooming Elf ClawHub release](https://clawhub.ai/shirley1011/blooming-elf) <br>
- [Publisher profile](https://clawhub.ai/user/shirley1011) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown text with concise care summaries, reminder tables, onboarding prompts, and record-update confirmations.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update plant care records and reminder configuration when the agent environment provides those capabilities.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
