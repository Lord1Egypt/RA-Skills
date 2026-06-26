## Description: <br>
Fridge Keeper helps users record fridge inventory, track expiration dates, surface near-expiry items, and recommend recipes from available ingredients. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lz6060788](https://clawhub.ai/user/lz6060788) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Household users and assistants use this skill to maintain a fridge inventory, configure local or database storage, check expiring food, and get recipe suggestions that prioritize food that should be used soon. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Household food inventory data may reveal personal routines or preferences when stored locally or in a database. <br>
Mitigation: Prefer local storage unless database access is needed, and store only the food records required for the workflow. <br>
Risk: Database mode requires user-provided connection details and could expose broader data if over-privileged credentials are reused. <br>
Mitigation: Use a dedicated low-privilege database user and avoid reusing important passwords. <br>
Risk: Expiry dates and recipe suggestions rely on user-provided shelf-life values or general AI food knowledge. <br>
Mitigation: Ask users to confirm uncertain shelf-life values and treat food-safety decisions as user-verified guidance. <br>


## Reference(s): <br>
- [Food expiry storage notes](references/food_expiry.md) <br>
- [ClawHub skill page](https://clawhub.ai/lz6060788/fridge-keeper) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown or plain text responses, with JSON configuration and inventory records when storage is used] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local fridge inventory and configuration files, or connect to a user-provided MySQL, PostgreSQL, or MongoDB database.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
