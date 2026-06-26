## Description: <br>
Automated form generation from roadflow.rf_form with similarity-based copying for HTML templates, dynamic forms, client-side validation, and multi-step wizard forms. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ericyang1234](https://clawhub.ai/user/ericyang1234) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to generate accessible, responsive HTML forms, JSON-backed form definitions, client-side validation logic, and RoadFlow rf_form-based form variants from existing similar forms. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The artifact exposes a database password and database connection details. <br>
Mitigation: Remove the exposed secret, rotate the password before any use, move credentials to secure runtime configuration, and use a least-privilege database account. <br>
Risk: The skill describes writing generated forms into roadflow.rf_form. <br>
Mitigation: Require explicit user confirmation and human review before any insert or update, especially when operating against a real RoadFlow database. <br>
Risk: Generated client-side validators can improve usability but are not sufficient for security-sensitive validation. <br>
Mitigation: Enforce equivalent server-side validation for submitted form data, uploaded files, and authorization-dependent fields. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ericyang1234/form-builder) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with HTML, JavaScript, and JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include similarity match summaries and generated form configuration for RoadFlow rf_form workflows.] <br>

## Skill Version(s): <br>
2.0.0 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
