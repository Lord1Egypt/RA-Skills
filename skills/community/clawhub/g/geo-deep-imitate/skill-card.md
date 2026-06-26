## Description: <br>
Geo Deep Imitate fetches reference sources with web_fetch, submits them to the GEO service for deep imitation article generation, exports a ZIP, and reports completion. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chameleon-nexus](https://clawhub.ai/user/chameleon-nexus) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill inside GEO automation workflows to gather source material, generate a deep imitation draft, export the resulting ZIP, and mark the imitation workflow complete. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores a GEO API key in a local plaintext file. <br>
Mitigation: Store the key with restrictive file permissions and remove the local key file when it is no longer needed. <br>
Risk: The skill sends task content, fetched reference content, and task metadata to ai.gaobobo.cn. <br>
Mitigation: Use the skill only when sharing that information with the GEO service is acceptable for the task. <br>
Risk: The skill exports generated ZIP files to the local GEO exports directory. <br>
Mitigation: Review exported files before reuse or distribution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chameleon-nexus/geo-deep-imitate) <br>
- [GEO service](https://ai.gaobobo.cn) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Files, API calls, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated export files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Fetches reference content, sends task metadata to the GEO service, and writes exported ZIP files under the user's local GEO export directory.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
