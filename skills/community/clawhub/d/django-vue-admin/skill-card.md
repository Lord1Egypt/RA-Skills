## Description: <br>
Generates django-vue-admin style CRUD scaffolding for Django models, serializers, viewsets, URLs, Vue API modules, and Vue pages from a requested module description. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jpzhengcn](https://clawhub.ai/user/jpzhengcn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to scaffold Django REST Framework and Vue CRUD modules for django-vue-admin projects. It is most useful when a module description or existing Django model should be turned into backend API code and frontend admin UI code quickly. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated admin templates may include unsafe permission patterns, including object-permission behavior and RBAC maps that need review. <br>
Mitigation: Audit and test object permissions, RBAC mappings, queryset scoping, serializers, and update/delete paths before using generated code. <br>
Risk: Template examples include a default password value of 0000 for created users. <br>
Mitigation: Remove the default password pattern and require secure password setup or reset flows before deployment. <br>
Risk: The generator writes over common project files such as serializers.py, views.py, urls.py, and frontend API modules. <br>
Mitigation: Run the generator only on a backed-up branch and review diffs before merging generated files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jpzhengcn/django-vue-admin) <br>
- [Publisher profile](https://clawhub.ai/user/jpzhengcn) <br>
- [Skill usage and examples](artifact/SKILL.md) <br>
- [Core module templates](artifact/templates/CORE_MODULES.md) <br>
- [Business logic reference](artifact/templates/BUSINESS_LOGIC.md) <br>
- [Logic flow reference](artifact/templates/LOGIC_FLOW.md) <br>
- [Field template reference](artifact/templates/FIELD_TEMPLATE.md) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown explanations with Python, JavaScript, Vue, and shell code blocks; generator script output writes code files when run.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated files may include serializers.py, views.py, urls.py, and src/api/<module>.js; review before applying to a project.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
