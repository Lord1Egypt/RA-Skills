## Description:

form2api reverse-engineers login-required web forms by capturing submitted browser requests, analyzing request fields, and producing reusable API documentation and call examples.

This skill is ready for commercial/non-commercial use.

## Publisher:

[longway-code](https://clawhub.ai/user/longway-code)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect authenticated form submissions and generate reusable API documentation, curl examples, and Python call code for automation or bulk operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can capture authenticated browser traffic, API responses, and live cookies.

Mitigation: Use it only on systems and accounts the user is authorized to test, avoid sensitive accounts, and treat generated API docs and cookie values as secrets.

Risk: Captured requests, analyzed API data, and cached cookies may remain in /tmp outputs.

Mitigation: Clear /tmp/form_api_raw.json, /tmp/form_api_analysis.json, and /tmp/form_api_cookies/ after use.

## Reference(s):

- [Output format reference](artifact/references/output_template.md)
- [ClawHub skill page](https://clawhub.ai/longway-code/skills/form2api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown with curl and Python examples plus JSON analysis artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write captured request data, analyzed request candidates, and cached cookies under /tmp.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
