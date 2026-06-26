## Description: <br>
Semantic code caching for AI agents. Cache, retrieve, and reuse code from prior agent executions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ryx2](https://clawhub.ai/user/ryx2) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use Code Cache to search for, retrieve, upload, and vote on reusable code snippets from prior agent executions through the Raysurfer API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected source files and task descriptions may be sent to Raysurfer. <br>
Mitigation: Use a dedicated API key and avoid uploading secrets or proprietary code unless approved. <br>
Risk: Retrieved code is written locally and may be executed by an agent. <br>
Mitigation: Review cached code before running it and execute it in a constrained sandbox. <br>
Risk: The files command can write retrieved files into a local cache directory. <br>
Mitigation: Use a dedicated cache directory and avoid running the command in sensitive directories until filename and path validation is added. <br>


## Reference(s): <br>
- [Code Cache on ClawHub](https://clawhub.ai/ryx2/code-cache) <br>
- [Raysurfer Website](https://raysurfer.com) <br>
- [Raysurfer Documentation](https://docs.raysurfer.com) <br>
- [Raysurfer API Keys](https://raysurfer.com/dashboard/api-keys) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [CLI text output, Markdown prompt guidance, and retrieved code files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write retrieved code files under the configured cache directory and may upload selected local files to Raysurfer.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
