## Description: <br>
Search Beepack for reusable API packages before coding. Saves tokens and time by reusing production-tested code instead of writing from scratch. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[actabi](https://clawhub.ai/user/actabi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to search Beepack before writing API clients, integrations, or reusable utilities. It helps agents find existing JavaScript modules, inspect package details and feedback, and decide whether to reuse or suggest improvements to a package. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks the agent to submit feedback, suggestions, reports, and code diffs to Beepack. <br>
Mitigation: Require user approval of exact outgoing content before any POST request, and remove secrets, customer data, internal URLs, and proprietary details. <br>
Risk: The skill encourages reuse of third-party package code discovered through Beepack. <br>
Mitigation: Review package code, license terms, dependencies, and security posture before integrating it into a project. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/actabi/beepack-deprecated) <br>
- [Publisher profile](https://clawhub.ai/user/actabi) <br>
- [Agent-facing skill documentation](SKILL.md) <br>
- [Beepack homepage](https://beepack.ai) <br>
- [Beepack search API](https://beepack.ai/api/v1/search?q=what+you+need) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with HTTP endpoint examples and reusable code selection advice] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Beepack package recommendations, package usage guidance, and proposed feedback or code-diff content for user review.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
