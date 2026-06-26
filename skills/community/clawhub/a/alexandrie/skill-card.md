## Description: <br>
Provides CRUD and search operations for Alexandrie, a self-hosted Markdown note-taking app, through its REST API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Eth3rnit3](https://clawhub.ai/user/Eth3rnit3) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users can use this skill to authenticate to an Alexandrie notes account and list, read, search, create, update, or delete Markdown notes through the service API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read, create, update, and delete Alexandrie notes for the configured account. <br>
Mitigation: Install only for an account you control, and require explicit confirmation before update or delete actions. <br>
Risk: The skill uses a local password configuration and temporary authenticated session cookie. <br>
Mitigation: Protect the ALEXANDRIE_PASSWORD file, log out after use, and remove the temporary cookie when finished. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Eth3rnit3/alexandrie) <br>
- [Publisher profile](https://clawhub.ai/user/Eth3rnit3) <br>
- [Artifact skill documentation](artifact/SKILL.md) <br>
- [Artifact Alexandrie shell client](artifact/alexandrie.sh) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Text, JSON, Configuration] <br>
**Output Format:** [Markdown guidance with bash commands; command responses are JSON formatted by jq.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an Alexandrie password configuration and stores an authenticated cookie in /tmp during use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
