## Description: <br>
Bigyou is a Chinese-language decision-support skill that helps users compare options by defining decision criteria, applying hard filters, scoring weighted preferences, and producing a structured recommendation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jack-xun](https://clawhub.ai/user/jack-xun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers can use this skill when they need structured help choosing between offers, plans, tools, paths, strategies, housing options, or other comparable alternatives. It is intended to turn subjective uncertainty into a criteria-driven comparison with bottom-line filters, weighted scoring, risks, and a recommendation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may activate on broad choice phrases such as "which is better" or "how should I choose," which can make it appear in a wide range of decision contexts. <br>
Mitigation: Confirm the user's actual decision context and available options before applying the scoring framework. <br>
Risk: The scoring framework is heuristic and may be unsuitable as the sole basis for high-stakes career, finance, investment, housing, medical, or similar decisions. <br>
Mitigation: Ask users to verify factual inputs, review the assumptions behind each score, and seek qualified advice for high-stakes decisions. <br>


## Reference(s): <br>
- [Profile Template](references/profile-template.md) <br>
- [Score Matrix](references/score-matrix.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands] <br>
**Output Format:** [Markdown decision report with tables and optional shell command examples for local script execution] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces heuristic scoring and recommendation rationale; users should verify facts before acting on the result.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
