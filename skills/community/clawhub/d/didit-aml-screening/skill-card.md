## Description:

Integrates Didit's AML Screening standalone API so agents can help screen people or companies against global watchlists, sanctions lists, PEP data, adverse media, and other high-risk databases.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rosasalberto](https://clawhub.ai/user/rosasalberto)

### License/Terms of Use:


## Use Case:

Compliance developers and operations teams use this skill to add Didit AML screening flows or run command-line checks for people and companies with a DIDIT_API_KEY.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends highly sensitive identity and AML subject data to Didit.

Mitigation: Use it only with the required consent or legal basis, minimize submitted subject data where possible, and confirm the destination service is approved for the workflow.

Risk: AML responses and helper output can expose sensitive subject data or watchlist details in shared logs or agent sessions.

Mitigation: Avoid logged CI or shared sessions unless output is redacted, and restrict access to full responses.

Risk: Retention, saved requests, and continuous monitoring behavior may need explicit compliance controls before routine use.

Mitigation: Add or verify controls for save_api_request, continuous monitoring, and full-response output before operational deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/rosasalberto/skills/didit-aml-screening)
- [Didit Documentation](https://docs.didit.me)
- [Didit AML Screening API Reference](https://docs.didit.me/standalone-apis/aml-screening)
- [Didit AML Screening Feature Guide](https://docs.didit.me/core-technology/aml-screening/overview)
- [Didit AML Risk Score](https://docs.didit.me/core-technology/aml-screening/aml-risk-score)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance with Python, TypeScript, bash examples, and JSON API response shapes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires DIDIT_API_KEY; the helper script can make live requests to Didit's AML endpoint.]

## Skill Version(s):

1.1.0 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
