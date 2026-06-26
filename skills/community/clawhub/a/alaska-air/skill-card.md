## Description: <br>
Scrape Alaska Airlines award calendar and flight data to check miles, award availability, and prices for single-leg trips on alaskaair.com. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iskWang](https://clawhub.ai/user/iskWang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travelers and booking agents use this skill to query Alaska Airlines one-way award availability for specified routes and months, then receive formatted mileage, price, and booking-link results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search results may be sent automatically through Telegram. <br>
Mitigation: Install only when Telegram forwarding is intended, verify the caller-provided chat destination, or disable external messaging before use. <br>
Risk: Worker agents are instructed to use broad execution, read, and message permissions for parallel searches. <br>
Mitigation: Restrict worker tools to the minimum curl, Python, and message access needed for the specific award search. <br>
Risk: The artifact references Alaska account and token endpoints. <br>
Mitigation: Avoid authenticated account or token endpoints unless separately reviewed and explicitly required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/iskWang/alaska-air) <br>
- [Alaska Airlines award calendar search](https://www.alaskaair.com/search/calendar?O={ORIGIN}&D={DEST}&OD={YYYY-MM-01}&A=1&RT=false&RequestType=Calendar&ShoppingMethod=onlineaward&locale=en-us) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown with inline Bash and Python examples, JSON parser output, and Telegram-ready text results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes route, month, award mileage, cash price, availability status, and direct booking URLs when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
