## Description: <br>
Compatibility entry for our in-house Baidu realtime search chain. Use for live information, documentation, or research topics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangziiiiii](https://clawhub.ai/user/wangziiiiii) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to keep existing baidu-search workflows working while routing live information, documentation, or research queries through a Baidu-based realtime search chain. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The alias runs a separate local realtime-web-search implementation, so behavior depends on code outside this artifact. <br>
Mitigation: Install only when the local realtime-web-search skill is trusted and has been reviewed. <br>
Risk: Search queries and credentials may be exposed through Baidu API usage or endpoint overrides. <br>
Mitigation: Use a limited Baidu API key where possible, avoid sensitive queries, and verify endpoint override variables before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangziiiiii/baidu-search-pro) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration guidance] <br>
**Output Format:** [Text responses from a Python command invoked with JSON input] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Python 3 runtime and BAIDU_API_KEY; supports optional Baidu endpoint override environment variables.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
