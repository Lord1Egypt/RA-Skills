## Description: <br>
Create robust, accessible web forms with best practices for HTML structure, CSS styling, JavaScript interactivity, form validation, and server-side processing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jhauga](https://clawhub.ai/user/jhauga) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to create accessible, secure, and user-friendly web forms with HTML, CSS, JavaScript, PHP, Python, database integration, APIs, and progressive web app considerations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated forms may handle sensitive credentials, tokens, payment data, or personally identifiable information. <br>
Mitigation: Review generated forms before deployment, keep secrets in environment variables or a secret manager, and prefer hosted payment tokenization over raw payment-data handling. <br>
Risk: Client-side validation, hidden fields, and example code can be bypassed or misused if treated as authoritative controls. <br>
Mitigation: Use server-side validation and authorization for all user-controlled input, and do not trust hidden fields. <br>
Risk: Database-backed form examples can introduce SQL injection if user input is interpolated into queries. <br>
Mitigation: Use prepared statements for all user-controlled SQL. <br>
Risk: Framework or cookie examples can be unsafe in production if debug or cookie settings are left at development defaults. <br>
Mitigation: Disable Flask debug mode in production and configure cookies securely. <br>


## Reference(s): <br>
- [Create Web Form Skill](SKILL.md) <br>
- [Form Basics Reference](references/form-basics.md) <br>
- [HTML Form Elements Reference](references/html-form-elements.md) <br>
- [Form Controls Reference](references/form-controls.md) <br>
- [Web Accessibility Reference](references/accessibility.md) <br>
- [ARIA Form Role Reference](references/aria-form-role.md) <br>
- [CSS Styling Reference](references/css-styling.md) <br>
- [Styling Web Forms Reference](references/styling-web-forms.md) <br>
- [JavaScript Reference](references/javascript.md) <br>
- [Form Data Handling Reference](references/form-data-handling.md) <br>
- [PHP Forms Reference](references/php-forms.md) <br>
- [PHP MySQL Database Reference](references/php-mysql-database.md) <br>
- [Python Contact Form Reference](references/python-contact-form.md) <br>
- [Python Flask Reference](references/python-flask.md) <br>
- [Web Security Reference](references/security.md) <br>
- [Web API Reference](references/web-api.md) <br>
- [Web Performance Reference](references/web-performance.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/jhauga/create-web-form) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, configuration] <br>
**Output Format:** [Markdown guidance with inline code examples and implementation recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include HTML, CSS, JavaScript, PHP, Python, SQL, API, accessibility, security, and performance guidance depending on the form being built.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
