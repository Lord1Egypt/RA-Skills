## Description: <br>
Package directories into distributable bundles with manifests. Use when creating release packages, verifying contents, or generating checksums. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xueyetianya](https://clawhub.ai/user/xueyetianya) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and release engineers use this skill to package directories, inspect bundle contents, verify checksums, and prepare distributable archives. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The extract command unpacks tar.gz archives into a local directory. <br>
Mitigation: Extract only trusted bundles, choose a scratch destination, and inspect archive contents before unpacking into important paths. <br>
Risk: Documented command examples may not match the shell script's positional argument handling. <br>
Mitigation: Test each command on disposable sample directories before using it for release packaging. <br>
Risk: Create, extract, and data-directory initialization write files on the local filesystem. <br>
Mitigation: Run the skill only on intended directories and review generated archives, manifests, and checksum files before distribution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xueyetianya/bundle) <br>
- [Publisher profile](https://clawhub.ai/user/xueyetianya) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, files, guidance] <br>
**Output Format:** [Markdown with inline bash commands and generated archive, manifest, and checksum files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands operate on local directories and tar.gz bundles.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
