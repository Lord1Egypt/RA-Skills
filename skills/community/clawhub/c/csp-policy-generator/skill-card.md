## Description: <br>
Generate, validate, and tighten Content Security Policy (CSP) headers for web applications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security engineers use this skill to inspect authorized web applications, draft least-privilege CSP headers, validate existing policies, and plan report-only to enforcement migrations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes commands that fetch web pages and JavaScript assets for CSP analysis. <br>
Mitigation: Use the commands only on sites you own or are authorized to test, and review each host before running network requests. <br>
Risk: A generated CSP can block required resources or leave risky allowances if deployed without validation. <br>
Mitigation: Deploy generated policies in report-only mode first, monitor violations, fix findings, and move to enforcement only after review. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/charlie-morrison/csp-policy-generator) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with CSP header examples, command snippets, and code/configuration blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include report-only and enforcement policies, nonce or hash examples, migration steps, and warnings for weak CSP directives.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
