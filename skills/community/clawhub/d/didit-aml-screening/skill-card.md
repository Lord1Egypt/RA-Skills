## Description: <br>
Integrate Didit AML Screening standalone API to screen individuals or companies against global watchlists, check sanctions and PEP status, detect adverse media, calculate risk scores, and support anti-money laundering workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rosasalberto](https://clawhub.ai/user/rosasalberto) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, compliance teams, and agents use this skill to run Didit AML screening for people or companies, interpret match and risk scores, and decide when manual compliance review is needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends AML screening details about people or companies to Didit. <br>
Mitigation: Use it only when you intend to use Didit for AML screening and have a valid legal basis or consent for the screening subject. <br>
Risk: A DIDIT_API_KEY is required and could expose account access if mishandled. <br>
Mitigation: Store the key in environment variables or a secrets manager and avoid committing or sharing it. <br>
Risk: Optional identifiers such as document numbers can increase privacy impact. <br>
Mitigation: Minimize optional identifiers to what is necessary for the compliance workflow. <br>
Risk: Didit request-saving, retention, billing, and continuous-monitoring settings affect operational and compliance exposure. <br>
Mitigation: Review those Didit settings before using the skill with real people or companies. <br>


## Reference(s): <br>
- [Didit Documentation](https://docs.didit.me) <br>
- [Didit AML Screening API Reference](https://docs.didit.me/standalone-apis/aml-screening) <br>
- [Didit AML Screening Feature Guide](https://docs.didit.me/core-technology/aml-screening/overview) <br>
- [Didit AML Risk Score](https://docs.didit.me/core-technology/aml-screening/aml-risk-score) <br>
- [ClawHub Skill Page](https://clawhub.ai/rosasalberto/didit-aml-screening) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown guidance with code examples, shell commands, configuration notes, and JSON API response examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires DIDIT_API_KEY and sends user-provided AML screening subjects to Didit.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
