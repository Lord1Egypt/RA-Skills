## Description: <br>
Manages Baidu Netdisk files by listing directories, searching files, and creating folders through the Baidu Netdisk REST API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[382108113](https://clawhub.ai/user/382108113) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to inspect and manage Baidu Netdisk contents after configuring a Baidu App ID and OAuth access token. It supports listing paths, searching filenames, and creating directories in a connected cloud storage account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad trigger phrases could cause the agent to access or change Baidu Netdisk content when the user did not clearly intend it. <br>
Mitigation: Invoke the skill only for explicit Baidu Netdisk requests, confirm exact paths before directory creation, and use the least-privileged Baidu OAuth token available. <br>
Risk: Listing and search results can expose sensitive filenames or folder structure. <br>
Mitigation: Review prompts and outputs before sharing them, and avoid using tokens tied to accounts that contain sensitive cloud storage contents. <br>


## Reference(s): <br>
- [Baidu Netdisk Open Platform Documentation](https://pan.baidu.com/union/doc/) <br>
- [ClawHub Skill Page](https://clawhub.ai/382108113/baidu-netdisk-eva) <br>
- [Publisher Profile](https://clawhub.ai/user/382108113) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration guidance] <br>
**Output Format:** [Plain text command output with Markdown configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires BAIDU_APP_ID and BAIDU_NETDISK_TOKEN environment variables and sends requests to the Baidu Netdisk API.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence.release.version and artifact/skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
