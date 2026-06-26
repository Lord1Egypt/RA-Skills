## Description: <br>
Check if your environment is ready to run a skill by verifying that required environment variables are set and required CLI binaries are on PATH. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mirni](https://clawhub.ai/user/mirni) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use Envcheck as a local pre-flight readiness check before running a skill, confirming whether required environment variables and command-line tools are present without disclosing secret values. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The service can reveal whether specific environment variable names and binaries exist on the host. <br>
Mitigation: Bind the uvicorn service to localhost or place it behind appropriate access controls. <br>
Risk: The skill is useful only when a local readiness check is desired. <br>
Mitigation: Install and run it only for local pre-flight environment verification workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mirni/gh-envcheck) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/mirni) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The runtime endpoint returns JSON readiness results with ready, present_env, missing_env, present_bins, and missing_bins fields.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
