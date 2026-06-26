## Description: <br>
Complete toolkit for the Cesto platform, covering basket browsing, basket creation, portfolio simulation, market data, token analysis, and analytics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lakshyagarg26](https://clawhub.ai/user/lakshyagarg26) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to interact with Cesto baskets, review market and performance data, analyze token allocations, create public Cesto Labs baskets, and simulate portfolio performance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The third-party skill stores Cesto session tokens locally and can open a browser login flow. <br>
Mitigation: Install and use it only for intentional Cesto tasks, review the skill before installation, and avoid sharing login links or session-related output in logs. <br>
Risk: Authenticated flows can publish public Cesto Labs baskets or send authenticated portfolio simulation requests. <br>
Mitigation: Confirm basket details carefully before publishing and run authenticated actions only after explicit user approval. <br>
Risk: Market and performance analysis could be mistaken for financial advice. <br>
Mitigation: Present the data as informational analysis and remind users that investment decisions require their own judgment. <br>


## Reference(s): <br>
- [Cesto API Reference](references/api-reference.md) <br>
- [Cesto application](https://app.cesto.co) <br>
- [Cesto backend API](https://backend.cesto.co) <br>
- [ClawHub skill page](https://clawhub.ai/lakshyagarg26/cesto-toolkit) <br>
- [Publisher profile](https://clawhub.ai/user/lakshyagarg26) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, API calls, guidance] <br>
**Output Format:** [Markdown summaries, tables, links, and concise command-backed API results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require Cesto authentication for basket creation and portfolio simulation; public browsing and analysis flows do not require login.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
