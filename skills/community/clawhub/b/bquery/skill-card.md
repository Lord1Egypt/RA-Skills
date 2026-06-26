## Description: <br>
Use this skill when working with @bquery/bquery, bQuery apps, or the bQuery ecosystem. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[josunlp](https://clawhub.ai/user/josunlp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to produce idiomatic bQuery guidance and code, including module selection, targeted imports, DOM work, reactivity, Web Components, routing, forms, accessibility, security, testing, and SSR patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Using the bQuery view module in a strict CSP environment may require unsafe-eval. <br>
Mitigation: Review CSP requirements before recommending the view module, and call out unsafe-eval implications when it is used. <br>
Risk: Dynamic HTML guidance can lead to unsafe rendering if untrusted content is inserted without sanitization. <br>
Mitigation: Use bQuery security helpers such as sanitizeHtml, trusted, and safeHtml for dynamic HTML, and keep sanitization guidance explicit in generated code. <br>


## Reference(s): <br>
- [bQuery homepage](https://bquery.flausch-code.de/) <br>
- [ClawHub skill page](https://clawhub.ai/josunlp/bquery) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Configuration] <br>
**Output Format:** [Markdown with TypeScript, JavaScript, HTML, and configuration examples where relevant] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only coding helper; no executable files or hidden system access are included in the artifact.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
