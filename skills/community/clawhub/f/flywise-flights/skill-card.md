## Description: <br>
FlyWise helps agents query paid real-time flight prices, 30-day route price history, and buy-or-wait recommendations for student and China-related travel through the FlyWise service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[heyuqiu2023](https://clawhub.ai/user/heyuqiu2023) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill when they want an agent to search one-way flight pricing, compare flight options, review recent route price trends, and present a buy-or-wait recommendation. It is especially focused on mainland China domestic routes and mainland China connections with the United States, United Kingdom, Australia, Canada, Europe, and Southeast Asia. <br>

### Deployment Geography for Use: <br>
Global, with route coverage focused on mainland China domestic routes and mainland China connections with the United States, United Kingdom, Australia, Canada, Europe, and Southeast Asia. <br>

## Known Risks and Mitigations: <br>
Risk: Flight search details are sent to flywise.win. <br>
Mitigation: Confirm the user wants to submit the route, travel date, cabin, and result count before making the request, and avoid adding unnecessary personal details. <br>
Risk: The paid API charges per successful query. <br>
Mitigation: Disclose the per-query payment step, ask the user to confirm payment, and offer the browser-based free option when the user does not want to use the paid API flow. <br>
Risk: Payment-Proof credentials can expose paid access if shared. <br>
Mitigation: Keep the Payment-Proof private and send it only as the request header needed to retrieve the paid FlyWise result. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/heyuqiu2023/flywise-flights) <br>
- [FlyWise Browser Search](https://flywise.win/flights/search) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API Calls, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and flight-search summaries based on JSON responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-confirmed per-query payment and a private Payment-Proof header before paid results are returned.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
