## Description: <br>
Baidu Netdisk automation skill for uploading, downloading, listing, syncing, and checking quota through bypy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[libin771018-sketch](https://clawhub.ai/user/libin771018-sketch) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to manage Baidu Netdisk files from an agent workflow, including authorization, uploads, downloads, directory listing, synchronization, and quota checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill grants the local environment access to a user's Baidu Netdisk account through bypy authorization files. <br>
Mitigation: Install only when the user trusts bypy, intends to grant that access, and can protect the local ~/.bypy/ authorization files. <br>
Risk: File transfers, force overwrites, and bidirectional sync can move or replace local and cloud files. <br>
Mitigation: Review local and cloud paths before execution, avoid --force unless overwrite is intended, and use bidirectional sync only after confirming conflict risk. <br>


## Reference(s): <br>
- [ClawHub Baidupan Skill](https://clawhub.ai/libin771018-sketch/baidupan) <br>
- [bypy Project](https://github.com/houtianze/bypy) <br>
- [Baidu Netdisk Open Platform](https://pan.baidu.com/union) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces user-facing command guidance for bypy-backed Baidu Netdisk operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
