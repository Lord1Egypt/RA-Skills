## Description: <br>
Manages Tencent Cloud COS vector buckets, indexes, vectors, vector search, and bucket policies across the vector storage lifecycle. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jimmyyan](https://clawhub.ai/user/jimmyyan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operators use this skill to administer Tencent Cloud COS vector storage, including vector bucket creation, index management, vector insertion, search, deletion, and bucket policy changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can perform high-impact Tencent Cloud COS operations, including deletes, policy changes, and bulk vector data operations. <br>
Mitigation: Use least-privilege Tencent Cloud credentials and require explicit workflow approval before destructive operations or policy updates. <br>
Risk: The scanner reported that the skill defaults to insecure HTTP. <br>
Mitigation: Set the protocol to HTTPS before using the skill with real credentials or production data. <br>
Risk: Credentials may be exposed if supplied directly on the command line. <br>
Mitigation: Prefer environment variables or a secret manager for COS_VECTORS_SECRET_ID and COS_VECTORS_SECRET_KEY. <br>


## Reference(s): <br>
- [COS Vector Bucket API Reference](artifact/references/api_reference.md) <br>
- [Tencent Cloud COS Vector Bucket API Documentation](https://cloud.tencent.com/document/product/436/127755) <br>
- [Tencent Cloud API Key Management](https://console.cloud.tencent.com/cam/capi) <br>
- [ClawHub Skill Page](https://clawhub.ai/jimmyyan/cos-vectors-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Tencent Cloud COS credentials via COS_VECTORS_SECRET_ID and COS_VECTORS_SECRET_KEY or command-line arguments.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
