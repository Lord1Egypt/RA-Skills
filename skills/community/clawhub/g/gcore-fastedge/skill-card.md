## Description: <br>
Build and deploy WebAssembly applications to Gcore FastEdge edge computing platform. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[geri4](https://clawhub.ai/user/geri4) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to create Rust-based FastEdge HTTP applications, build them as WebAssembly, and deploy or update them on Gcore FastEdge. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires GCORE_API_KEY and can make authenticated deployment requests to Gcore FastEdge. <br>
Mitigation: Use a scoped or temporary API key where possible, keep it out of shared shells and logs, and rotate it after sensitive deployment work. <br>
Risk: Build and deployment commands can publish or update remote FastEdge applications. <br>
Mitigation: Review the WebAssembly artifact, target app name, binary ID, and app ID before running upload, create, or update commands. <br>


## Reference(s): <br>
- [Gcore FastEdge documentation](https://gcore.com/docs/fastedge) <br>
- [Gcore API tokens](https://accounts.gcore.com/account-settings/api-tokens) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/geri4) <br>
- [ClawHub skill page](https://clawhub.ai/geri4/gcore-fastedge) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash, TOML, and Rust code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include deployment commands that require GCORE_API_KEY and calls to Gcore FastEdge APIs.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
