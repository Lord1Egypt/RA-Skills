## Description: <br>
Baidu Cloud BOS helps an agent manage Baidu Object Storage resources, including file upload, download, deletion, copying, listing, signed URLs, image processing, recursive directory transfer, and synchronization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yangdong2398](https://clawhub.ai/user/yangdong2398) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to let an agent configure Baidu Cloud BOS access and perform storage operations such as object transfer, listing, signed URL generation, image processing, bucket inspection, and directory synchronization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores Baidu Cloud access keys locally for reuse across sessions. <br>
Mitigation: Use dedicated least-privilege or temporary credentials, keep the generated credentials file permission-restricted, and rotate or remove credentials when the skill is no longer needed. <br>
Risk: Delete and synchronization commands can remove objects or mirror unintended changes in BOS buckets. <br>
Mitigation: Verify bucket names, object keys, prefixes, and sync direction before execution, and require explicit confirmation for destructive or --delete operations. <br>
Risk: Broad account keys pasted into shell commands can expose more cloud access than the task requires. <br>
Mitigation: Avoid broad account credentials, prefer scoped credentials or STS tokens, and avoid echoing secrets in command history or logs. <br>


## Reference(s): <br>
- [Baidu Cloud BOS Skill API Reference](references/api_reference.md) <br>
- [Baidu Cloud BOS Node.js SDK Documentation](https://cloud.baidu.com/doc/BOS/s/Djwvyrhiw) <br>
- [Baidu Cloud bcecmd Documentation](https://cloud.baidu.com/doc/BOS/s/kmcn3zrup) <br>
- [ClawHub Release Page](https://clawhub.ai/yangdong2398/baidu-cloud-bos) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown guidance with shell commands; the Node.js helper returns JSON for BOS operations.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Operations can affect cloud storage state, including deletion and synchronization with --delete behavior.] <br>

## Skill Version(s): <br>
1.1.2 (source: release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
