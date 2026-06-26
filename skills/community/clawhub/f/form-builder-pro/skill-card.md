## Description: <br>
Form Builder Pro helps agents create, validate, render, and serialize dynamic forms using JSON Schema, YAML or JSON configuration, conditional field logic, and Jinja2 templates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kaiyuelv](https://clawhub.ai/user/kaiyuelv) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to build form definitions, generate JSON Schema, validate submitted form data, render HTML form markup, and work with conditional form fields. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Dependency versions are not pinned in the artifact. <br>
Mitigation: For production use, pin and review jsonschema, PyYAML, and Jinja2 versions before deployment. <br>
Risk: Untrusted form configurations or templates can affect validation and rendering behavior. <br>
Mitigation: Do not load form configs or render templates from untrusted sources unless additional validation and sandboxing are in place. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kaiyuelv/form-builder-pro) <br>
- [Project homepage from ClawHub metadata](https://github.com/kaiyuelv/form-builder-pro) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with Python code, JSON Schema, YAML or JSON form definitions, and HTML snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include validation results, serialized form definitions, and rendered form markup.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence release.version and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
