## Description: <br>
Semantic code caching for AI agents. Cache, retrieve, and reuse code from prior agent executions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ryx2](https://clawhub.ai/user/ryx2) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to search, retrieve, upload, and rate reusable code snippets through the Raysurfer API so similar future coding tasks can reuse prior work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected code, task descriptions, and related metadata may be sent to the third-party Raysurfer service. <br>
Mitigation: Use only with code and metadata you are authorized to share; do not upload secrets, credentials, regulated data, or proprietary code unless sharing is approved. <br>
Risk: Retrieved remote code can be written locally and may be unsafe to run without review. <br>
Mitigation: Keep the cache directory isolated, avoid sensitive output paths, and review every downloaded file before executing or integrating it. <br>


## Reference(s): <br>
- [Code Reputation on ClawHub](https://clawhub.ai/ryx2/code-reputation) <br>
- [Raysurfer](https://raysurfer.com) <br>
- [Raysurfer Documentation](https://docs.raysurfer.com) <br>
- [Raysurfer API Keys](https://raysurfer.com/dashboard/api-keys) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, files, configuration, guidance] <br>
**Output Format:** [CLI text output, downloaded code files, and prompt guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires RAYSURFER_API_KEY and may write retrieved code files to a local cache directory.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
