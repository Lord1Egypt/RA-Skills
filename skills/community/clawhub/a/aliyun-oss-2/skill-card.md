## Description: <br>
Manage Aliyun OSS buckets in Python with upload, download, list, read, delete, copy, and move operations supporting authenticated and anonymous access. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangyendt](https://clawhub.ai/user/wangyendt) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to manage Aliyun OSS buckets from Python, including object upload, download, listing, metadata checks, deletion, copy, move, and prefix-based directory workflows. It is suitable for agents that need concise OSS usage guidance and code examples. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: OSS credentials can permit write, delete, copy, or move operations across a bucket. <br>
Mitigation: Use least-privilege Aliyun credentials limited to the intended bucket and required operations. <br>
Risk: Prefix-based delete, move, or bulk download guidance can affect many objects if the prefix is too broad. <br>
Mitigation: List matching keys first and require explicit confirmation before delete, move, or prefix-based bulk actions. <br>
Risk: The skill relies on the external pywayne package for OSS operations. <br>
Mitigation: Verify the pywayne package source and version before relying on it in production workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangyendt/aliyun-oss-2) <br>
- [Publisher profile](https://clawhub.ai/user/wangyendt) <br>
- [Skill usage documentation](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python code examples and configuration parameters for Aliyun OSS access.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance covers authenticated read/write access and anonymous read-only access; actual OSS operations require appropriate credentials and network access.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
