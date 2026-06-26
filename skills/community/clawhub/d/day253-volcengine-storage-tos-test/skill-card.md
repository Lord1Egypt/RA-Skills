## Description: <br>
Minimal TOS smoke tests for validating AK/SK configuration, listing buckets, and uploading and downloading objects with Volcengine TOS using tosutil CLI or tos_manage.py. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[day253](https://clawhub.ai/user/day253) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to smoke-test Volcengine TOS credentials, endpoint configuration, bucket listing, and object upload/download behavior before relying on a storage workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Running storage smoke tests against production or sensitive buckets can expose, overwrite, or leave behind real objects. <br>
Mitigation: Use a dedicated non-production bucket with non-sensitive test objects under a test prefix, and delete test objects after validation. <br>
Risk: Broad or long-lived AK/SK credentials and presigned URLs can grant more access than the smoke test needs. <br>
Mitigation: Use least-privilege temporary credentials and avoid sharing or logging credentials and presigned URLs. <br>
Risk: The workflow depends on external CLI, Python package, or helper-script behavior outside the skill card itself. <br>
Mitigation: Verify tosutil, the tos Python package, and any helper script before running commands in the target environment. <br>


## Reference(s): <br>
- [Volcengine tosutil documentation](https://www.volcengine.com/docs/6349/148772) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-provided Volcengine TOS credentials, endpoint or region settings, and a writable test bucket.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
