## Description: <br>
Validate and lint PHP Composer composer.json files for structure, dependencies, autoload, and best practices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect PHP Composer composer.json files, catch dependency and autoload issues, and produce text, JSON, or Markdown validation reports for local review or CI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Validation output may be used to fail CI or guide dependency changes. <br>
Mitigation: Review findings before relying on them in automation, and use --strict only when warning-level findings should fail the build. <br>
Risk: The bundled Python script reads user-selected Composer files. <br>
Mitigation: Run it only against files you intend to inspect; evidence.security reports no network access, credential use, persistence, or file mutation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/charlie-morrison/composer-json-validator) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Text, JSON, or Markdown reports with command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local file analysis only; strict mode can make warning-level findings fail automation.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
