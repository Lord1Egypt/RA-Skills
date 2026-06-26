## Description: <br>
Provides agent-accessible Aliyun OSS object storage operations, including upload, download, listing, deletion, object metadata lookup, object copy or move, and URL generation through the ali-oss Node.js SDK with ossutil as a documented fallback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aohoyo](https://clawhub.ai/user/aohoyo) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to configure Aliyun OSS credentials and ask an agent to manage bucket objects, inspect stored files, generate public or signed URLs, and automate storage workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist Aliyun cloud credentials and add ALIYUN_* values to shell startup files. <br>
Mitigation: Use least-privilege or temporary credentials, review local shell startup files after setup, and remove any credentials that should not persist. <br>
Risk: Delete operations can remove remote OSS objects without effective interactive safeguards. <br>
Mitigation: Avoid production buckets until deletion confirmation is fixed, restrict credentials to the minimum bucket and actions needed, and review delete commands before execution. <br>
Risk: Generated private object URLs can grant temporary access to bucket objects. <br>
Mitigation: Treat signed URLs as secrets, keep expiration windows short, and avoid sharing them in logs or persistent chat transcripts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aohoyo/aliyun-oss-skill) <br>
- [Aliyun OSS Node.js SDK documentation](https://help.aliyun.com/document_detail/32068.html) <br>
- [Aliyun ossutil documentation](https://help.aliyun.com/document_detail/120075.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and terminal-oriented text with shell commands, JSON configuration, and command output summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate signed private URLs that should be treated as temporary secrets.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
