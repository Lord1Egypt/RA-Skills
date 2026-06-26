## Description: <br>
Audit checkout friction points and prioritize fixes that improve completed purchases without increasing risk. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[Leooooooow](https://clawhub.ai/user/Leooooooow) <br>

### License/Terms of Use: <br>
CC BY-NC-SA 4.0 <br>


## Use Case: <br>
Conversion and ecommerce teams use this skill to inspect checkout flows, map friction points, and prioritize fixes for abandonment, payment, shipping, or trust issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Checkout audits may expose sensitive customer, payment, shipping, or active-session details when live flows are inspected. <br>
Mitigation: Use staging pages, test accounts, screenshots, or sanitized notes where possible, and allow current-browser inspection only when the user intentionally wants that session viewed. <br>
Risk: Friction-reduction recommendations could conflict with platform, payment, trust, or compliance requirements. <br>
Mitigation: Tie recommendations to observed evidence, prioritize reversible low-risk fixes, and review changes against payment and platform policies before implementation. <br>


## Reference(s): <br>
- [Output Template](references/output-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown with executive summary, priority actions, evidence table, and 7-day execution plan] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Recommendations should be tied to observed evidence, ranked by priority, and separated between quick wins and structural fixes.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
