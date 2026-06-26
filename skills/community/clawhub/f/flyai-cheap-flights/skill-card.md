## Description: <br>
Finds low-cost flights between two cities using FlyAI/Fliggy, compares airline fares, and highlights budget-friendly options such as red-eye, connecting, and flexible-date flights. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travelers and travel-planning agents use this skill to collect route constraints, run FlyAI flight searches, compare the lowest fares in Markdown tables, and suggest cheaper alternatives such as flexible dates, red-eye flights, or nearby departure cities. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses FlyAI/Fliggy-backed travel lookup commands and asks for broad runtime authority through a globally installed npm CLI. <br>
Mitigation: Install and run the FlyAI CLI only after explicit approval, avoid sudo, npm, or npx installation steps unless approved, and review generated commands before execution. <br>
Risk: Travel searches may involve personal itinerary, passport, payment, loyalty-account, or other sensitive travel details, while logging and retention behavior is not clearly scoped. <br>
Mitigation: Collect only the minimum details needed for the search and avoid sharing sensitive personal or payment information unless the user explicitly approves it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dingtom336-gif/flyai-cheap-flights) <br>
- [Skill instructions](SKILL.md) <br>
- [Output and parameter templates](references/templates.md) <br>
- [Fallback handling](references/fallbacks.md) <br>
- [Scenario playbooks](references/playbooks.md) <br>
- [Execution logging runbook](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown comparison tables with inline shell commands, booking links, and concise travel guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires origin and destination before search; defaults to price sorting and may add flexible-date, red-eye, nearby-city, or fallback searches.] <br>

## Skill Version(s): <br>
1.0.56052 (source: ClawHub release evidence; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
