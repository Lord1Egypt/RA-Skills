## Description: <br>
Crisp Grocery helps agents use a user's authorized Crisp account data to plan groceries, compare promotions, inspect delivery details, fetch images, and prepare supervised basket changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zeflow](https://clawhub.ai/user/zeflow) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users and their agents use this skill for Crisp grocery planning, promotion comparison, delivery-slot review, meal planning from authorized account history, and basket-change preparation that remains under user confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive Crisp account tokens and private account data. <br>
Mitigation: Store tokens only in a private environment variable or user-controlled token file, avoid printing secrets or raw account payloads, and save responses only when needed. <br>
Risk: Custom API bases or full URLs could send authorized requests to unexpected destinations. <br>
Mitigation: Use the default Crisp API base unless the user has a clear reason to override it, and review any custom base or full URL before making requests. <br>
Risk: Basket mutations can change the user's grocery basket. <br>
Mitigation: Keep workflows read-only by default, show the exact proposed basket diff, and require action-specific user confirmation before any mutation. <br>


## Reference(s): <br>
- [Crisp Grocery on ClawHub](https://clawhub.ai/zeflow/crisp-grocery) <br>
- [zeflow publisher profile](https://clawhub.ai/user/zeflow) <br>
- [Crisp API Map](artifact/references/api-map.md) <br>
- [Planning Rules](artifact/references/planning-rules.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and optional JSON summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save API responses when explicitly requested; summaries should avoid secrets and basket changes require user confirmation.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
